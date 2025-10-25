"""
Azure DevOps REST API client.
"""

import base64
import json
from typing import Any, Dict, List, Optional
from urllib.parse import quote

import requests

from .config import Config, get_config


class AzureDevOpsClient:
    """Client for interacting with Azure DevOps REST API."""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the Azure DevOps client.
        
        Args:
            config: Optional Config instance. If not provided, will load from environment.
        """
        self.config = config or get_config()
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create an authenticated requests session."""
        session = requests.Session()
        
        # Encode PAT for basic auth
        credentials = f":{self.config.pat}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        session.headers.update({
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json-patch+json",
            "Accept": "application/json",
        })
        
        return session
    
    def _get_url(self, path: str, use_project: bool = True) -> str:
        """
        Construct full API URL.
        
        Args:
            path: API path
            use_project: Whether to include project in URL
            
        Returns:
            Full URL
        """
        base = self.config.base_url
        project = quote(str(self.config.project))
        api_version = self.config.api_version
        
        if use_project:
            return f"{base}/{project}/_apis/{path}?api-version={api_version}"
        else:
            return f"{base}/_apis/{path}?api-version={api_version}"
    
    def create_work_item(
        self,
        work_item_type: str,
        fields: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Create a new work item.
        
        Args:
            work_item_type: Type of work item (e.g., "Product Backlog Item", "Bug")
            fields: Dictionary of field values
            
        Returns:
            Created work item data
            
        Raises:
            requests.HTTPError: If the request fails
        """
        url = self._get_url(f"wit/workitems/$" + quote(work_item_type))
        
        # Build patch document
        operations = []
        for field, value in fields.items():
            operations.append({
                "op": "add",
                "path": f"/fields/{field}",
                "value": value,
            })
        
        response = self.session.post(url, json=operations)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            # Add response body to error message for debugging
            error_detail = response.text if response.text else "No error details"
            raise requests.HTTPError(
                f"{e}. Response: {error_detail}", 
                response=response
            )
        
        return response.json()
    
    def get_work_item(
        self,
        work_item_id: int,
        fields: Optional[List[str]] = None,
        expand: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get a work item by ID.
        
        Args:
            work_item_id: Work item ID
            fields: Optional list of specific fields to retrieve
            expand: Optional expansion parameter (e.g., "relations", "all")
            
        Returns:
            Work item data
            
        Raises:
            requests.HTTPError: If the request fails
        """
        url = self._get_url(f"wit/workitems/{work_item_id}", use_project=False)
        
        params = {}
        if fields:
            params["fields"] = ",".join(fields)
        if expand:
            params["$expand"] = expand
        
        if params:
            url += "&" + "&".join(f"{k}={v}" for k, v in params.items())
        
        response = self.session.get(url)
        response.raise_for_status()
        
        return response.json()
    
    def update_work_item(
        self,
        work_item_id: int,
        updates: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Update a work item.
        
        Args:
            work_item_id: Work item ID
            updates: Dictionary of field updates
            
        Returns:
            Updated work item data
            
        Raises:
            requests.HTTPError: If the request fails
        """
        url = self._get_url(f"wit/workitems/{work_item_id}", use_project=False)
        
        # Build patch document
        operations = []
        for field, value in updates.items():
            operations.append({
                "op": "add",
                "path": f"/fields/{field}",
                "value": value,
            })
        
        response = self.session.patch(url, json=operations)
        response.raise_for_status()
        
        return response.json()
    
    def delete_work_item(self, work_item_id: int, destroy: bool = False) -> None:
        """
        Delete a work item.
        
        Args:
            work_item_id: Work item ID
            destroy: If True, permanently delete. If False, move to recycle bin.
            
        Raises:
            requests.HTTPError: If the request fails
        """
        url = self._get_url(f"wit/workitems/{work_item_id}", use_project=False)
        if destroy:
            url += "&destroy=true"
        
        response = self.session.delete(url)
        response.raise_for_status()
    
    def add_comment(self, work_item_id: int, comment_text: str) -> Dict[str, Any]:
        """
        Add a comment to a work item.
        
        Args:
            work_item_id: Work item ID
            comment_text: Comment text
            
        Returns:
            Comment data
            
        Raises:
            requests.HTTPError: If the request fails
        """
        # Use the History field instead of comments API for better compatibility
        return self.update_work_item(
            work_item_id,
            {"System.History": comment_text}
        )
    
    def get_work_item_types(self) -> List[Dict[str, Any]]:
        """
        Get all work item types for the project.
        
        Returns:
            List of work item type definitions
            
        Raises:
            requests.HTTPError: If the request fails
        """
        from .cache import get_cache
        cache = get_cache()
        cache_key = f"work_item_types:{self.config.organization}:{self.config.project}"
        
        def fetch():
            url = self._get_url("wit/workitemtypes")
            response = self.session.get(url)
            response.raise_for_status()
            return response.json().get("value", [])
        
        return cache.get_or_fetch(cache_key, fetch)
    
    def get_work_item_type_definition(self, work_item_type: str) -> Dict[str, Any]:
        """
        Get detailed definition for a specific work item type including states, fields, and transitions.
        
        Args:
            work_item_type: Work item type name (e.g., "User Story", "Bug", "Task")
            
        Returns:
            Work item type definition with states, fields, transitions
            
        Raises:
            requests.HTTPError: If the request fails
        """
        from .cache import get_cache
        cache = get_cache()
        cache_key = f"work_item_type_def:{self.config.organization}:{self.config.project}:{work_item_type}"
        
        def fetch():
            # URL encode the work item type name
            encoded_type = quote(work_item_type)
            url = self._get_url(f"wit/workitemtypes/{encoded_type}")
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        
        return cache.get_or_fetch(cache_key, fetch)
    
    def get_work_item_type_states(self, work_item_type: str) -> List[Dict[str, Any]]:
        """
        Get available states for a specific work item type.
        
        Args:
            work_item_type: Work item type name (e.g., "User Story", "Bug", "Task")
            
        Returns:
            List of state definitions with name, color, and category
            
        Raises:
            requests.HTTPError: If the request fails
        """
        definition = self.get_work_item_type_definition(work_item_type)
        return definition.get("states", [])
    
    def get_work_item_fields(self) -> List[Dict[str, Any]]:
        """
        Get all available fields in the project.
        
        Returns:
            List of field definitions with name, referenceName, type, etc.
            
        Raises:
            requests.HTTPError: If the request fails
        """
        from .cache import get_cache
        cache = get_cache()
        cache_key = f"work_item_fields:{self.config.organization}"
        
        def fetch():
            url = self._get_url("wit/fields", use_project=False)
            response = self.session.get(url)
            response.raise_for_status()
            return response.json().get("value", [])
        
        return cache.get_or_fetch(cache_key, fetch)
    
    def get_work_item_type_fields(self, work_item_type: str) -> List[Dict[str, Any]]:
        """
        Get fields for a specific work item type.
        
        Args:
            work_item_type: Work item type name (e.g., "User Story", "Bug", "Task")
            
        Returns:
            List of field definitions specific to this type
            
        Raises:
            requests.HTTPError: If the request fails
        """
        definition = self.get_work_item_type_definition(work_item_type)
        return definition.get("fields", [])
    
    def add_parent_link(
        self,
        child_id: int,
        parent_id: int,
        link_type: str = "System.LinkTypes.Hierarchy-Reverse",
    ) -> Dict[str, Any]:
        """
        Add a parent link to a work item.
        
        Args:
            child_id: Child work item ID
            parent_id: Parent work item ID
            link_type: Link type (default: parent link)
            
        Returns:
            Updated work item data
            
        Raises:
            requests.HTTPError: If the request fails
        """
        url = self._get_url(f"wit/workitems/{child_id}", use_project=False)
        
        operations = [{
            "op": "add",
            "path": "/relations/-",
            "value": {
                "rel": link_type,
                "url": f"{self.config.base_url}/_apis/wit/workitems/{parent_id}",
            }
        }]
        
        response = self.session.patch(url, json=operations)
        response.raise_for_status()
        
        return response.json()

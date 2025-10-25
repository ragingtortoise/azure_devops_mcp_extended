"""
Configuration management for Azure DevOps connection.
Reads from environment variables and .env file.
"""

import os
from typing import Optional
from pathlib import Path


# Auto-load .env file when module is imported
def _load_dotenv():
    """Load .env file from the package root directory."""
    try:
        # Find .env file in the package root directory
        package_root = Path(__file__).parent.parent
        env_file = package_root / ".env"
        
        if env_file.exists():
            # Read and parse .env file
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse KEY=VALUE format
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        
                        # Only set if not already in environment (env vars take precedence)
                        if key and not os.getenv(key):
                            os.environ[key] = value
    except Exception:
        # Silently fail - if .env loading fails, fall back to system env vars
        pass


# Load .env file when config module is imported
_load_dotenv()


class Config:
    """Azure DevOps configuration from environment variables."""
    
    def __init__(self):
        self.organization = os.getenv("AZDO_ORGANIZATION")
        self.project = os.getenv("AZDO_PROJECT")
        self.pat = os.getenv("AZDO_PAT")
        
        # Optional settings with defaults
        self.api_version = os.getenv("AZDO_API_VERSION", "7.1")
        
    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Validate that all required configuration is present.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.organization:
            return False, "AZDO_ORGANIZATION environment variable is not set"
        
        if not self.project:
            return False, "AZDO_PROJECT environment variable is not set"
        
        if not self.pat:
            return False, "AZDO_PAT environment variable is not set"
        
        return True, None
    
    @property
    def base_url(self) -> str:
        """Get the base URL for Azure DevOps API."""
        return f"https://dev.azure.com/{self.organization}"
    
    def __repr__(self) -> str:
        return (
            f"Config(organization={self.organization}, "
            f"project={self.project}, "
            f"pat={'***' if self.pat else None})"
        )


def get_config() -> Config:
    """
    Get validated configuration.
    
    Returns:
        Config instance
        
    Raises:
        ValueError: If configuration is invalid
    """
    config = Config()
    is_valid, error_message = config.validate()
    
    if not is_valid:
        raise ValueError(
            f"Invalid configuration: {error_message}\n"
            "Please set the following environment variables:\n"
            "  - AZDO_ORGANIZATION: Your Azure DevOps organization name\n"
            "  - AZDO_PROJECT: Your project name\n"
            "  - AZDO_PAT: Your Personal Access Token"
        )
    
    return config

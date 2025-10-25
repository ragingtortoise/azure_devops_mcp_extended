"""
Quick validation script to check if the package is properly set up.
Run this to validate configuration and imports.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def check_imports():
    """Check if all modules can be imported."""
    print("🔍 Checking imports...")
    
    try:
        from devops_extended import (
            AzureDevOpsClient,
            create_pbi,
            create_bug,
            create_task,
            create_feature,
            create_epic,
            get_work_item,
            delete_work_item,
            update_work_item,
            update_title,
            update_description,
            assign_work_item,
            add_comment,
            transition_to_new,
            transition_to_active,
            transition_to_resolved,
            transition_to_closed,
            transition_to_removed,
            get_available_states,
        )
        print("   ✅ All imports successful")
        return True
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        return False


def check_config():
    """Check configuration setup."""
    print("\n🔍 Checking configuration...")
    
    try:
        from devops_extended.config import get_config
        
        config = get_config()
        print(f"   ✅ Configuration loaded")
        print(f"      Organization: {config.organization}")
        print(f"      Project: {config.project}")
        print(f"      PAT: {'*' * 20 if config.pat else 'NOT SET'}")
        print(f"      Base URL: {config.base_url}")
        return True
        
    except ValueError as e:
        print(f"   ⚠️  Configuration incomplete: {e}")
        print("\n   Please set the following environment variables:")
        print("      AZDO_ORGANIZATION - Your Azure DevOps organization name")
        print("      AZDO_PROJECT - Your project name")
        print("      AZDO_PAT - Your Personal Access Token")
        return False
    except Exception as e:
        print(f"   ❌ Configuration error: {e}")
        return False


def check_cli():
    """Check if CLI module is available."""
    print("\n🔍 Checking CLI module...")
    
    try:
        from devops_extended import cli
        print("   ✅ CLI module available")
        print("   Run with: python -m devops_extended --help")
        return True
    except ImportError as e:
        print(f"   ❌ CLI import failed: {e}")
        return False


def check_dependencies():
    """Check if required dependencies are installed."""
    print("\n🔍 Checking dependencies...")
    
    dependencies = {
        "requests": "requests",
    }
    
    all_ok = True
    for name, import_name in dependencies.items():
        try:
            __import__(import_name)
            print(f"   ✅ {name} installed")
        except ImportError:
            print(f"   ❌ {name} NOT installed")
            all_ok = False
    
    if not all_ok:
        print("\n   Install missing dependencies:")
        print("      pip install -r requirements.txt")
    
    return all_ok


def test_basic_functionality():
    """Test basic package functionality."""
    print("\n🔍 Testing basic functionality...")
    
    try:
        from devops_extended.config import Config
        
        # Test config creation (won't validate if env vars not set)
        config = Config()
        print(f"   ✅ Config object created")
        
        # Test validation
        is_valid, error = config.validate()
        if is_valid:
            print(f"   ✅ Configuration is valid")
            print(f"   ℹ️  Ready to create work items!")
        else:
            print(f"   ⚠️  Configuration invalid: {error}")
            print(f"   ℹ️  Set environment variables to enable full functionality")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Functionality test failed: {e}")
        return False


def main():
    """Run all validation checks."""
    print("=" * 70)
    print("Azure DevOps Extended - Validation Script")
    print("=" * 70)
    
    results = {
        "Imports": check_imports(),
        "Dependencies": check_dependencies(),
        "Configuration": check_config(),
        "CLI": check_cli(),
        "Functionality": test_basic_functionality(),
    }
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    for check, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {check}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 70)
    
    if all_passed:
        print("🎉 All checks passed! Package is ready to use.")
        print("\nNext steps:")
        print("  1. Set environment variables (if not already set)")
        print("  2. Try: python -m devops_extended --help")
        print("  3. Create a work item: python -m devops_extended create-pbi \"Test\"")
    else:
        print("⚠️  Some checks failed. Please review the output above.")
        print("\nCommon fixes:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Set environment variables: AZDO_ORGANIZATION, AZDO_PROJECT, AZDO_PAT")
    
    print("=" * 70)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

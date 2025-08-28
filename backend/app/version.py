"""
Module for dynamic project version management.
Extracts the latest version from CHANGELOG.md automatically.
"""

import re
from pathlib import Path
from typing import Optional

def get_version_from_changelog() -> str:
    """
    Extracts the latest version from CHANGELOG.md.
    
    Returns:
        str: Version in X.Y.Z format or default version if not found
    """
    try:
        # Path to CHANGELOG.md in project root
        project_root = Path(__file__).parent.parent.parent
        changelog_path = project_root / "CHANGELOG.md"
        
        if not changelog_path.exists():
            return "0.0.0"
        
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Search for pattern ## [X.Y.Z] - YYYY-MM-DD
        version_pattern = r'## \[(\d+\.\d+\.\d+)\] - \d{4}-\d{2}-\d{2}'
        match = re.search(version_pattern, content)
        
        if match:
            return match.group(1)
        else:
            return "0.0.0"
            
    except Exception:
        # If any error occurs, return default version
        return "0.0.0"

def get_project_info() -> dict:
    """
    Returns complete project information including version.
    
    Returns:
        dict: Dictionary with project information
    """
    version = get_version_from_changelog()
    
    return {
        "name": "Bellum Astrum",
        "version": version,
        "api_title": "Space Battle Game API",
        "description": "API for managing game resources like Ships and Users with enhanced database management.",
        "author": "FilipePacheco73"
    }

# Version cache to avoid multiple file reads
_cached_version: Optional[str] = None

def get_cached_version() -> str:
    """
    Returns the version using cache for better performance.
    
    Returns:
        str: Project version
    """
    global _cached_version
    
    if _cached_version is None:
        _cached_version = get_version_from_changelog()
    
    return _cached_version

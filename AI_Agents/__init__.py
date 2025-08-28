"""
AI Agents - Autonomous AI players for Bellum Astrum
"""

import re
from pathlib import Path

def _get_version_from_changelog() -> str:
    """Extracts the version from CHANGELOG.md"""
    try:
        project_root = Path(__file__).parent.parent
        changelog_path = project_root / "CHANGELOG.md"
        
        if not changelog_path.exists():
            return "1.0.0"
        
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Search for pattern ## [X.Y.Z] - YYYY-MM-DD
        version_pattern = r'## \[(\d+\.\d+\.\d+)\] - \d{4}-\d{2}-\d{2}'
        match = re.search(version_pattern, content)
        
        if match:
            return match.group(1)
        else:
            return "1.0.0"
            
    except Exception:
        return "1.0.0"

__version__ = _get_version_from_changelog()

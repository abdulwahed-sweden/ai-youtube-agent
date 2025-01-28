# utils.py

import os
import json
import re
from datetime import datetime
from typing import Dict, Any, Union
from pydantic import BaseModel

def save_output_to_markdown(data: Dict[str, Any], filename: str = None) -> str:
    """
    Save analysis results to a Markdown file with proper formatting
    
    Args:
        data: Dictionary containing analysis results
        filename: Output filename (optional)
        
    Returns:
        Path to the generated Markdown file
        
    Example:
        >>> save_output_to_markdown({"summary": "Great creator"}, "report.md")
        'reports/report_20230801.md'
    """
    try:
        # Create default filename if not provided
        if not filename:
            os.makedirs("reports", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d%H%M")
            filename = f"reports/creator_report_{timestamp}.md"

        # Create directory structure if needed
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Generate Markdown content
        content = ["# Content Creator Analysis Report\n"]
        
        def process_section(key: str, value: Any, level: int = 2):
            """Recursive function to process nested data"""
            nonlocal content
            header = "#" * level
            if isinstance(value, dict):
                content.append(f"\n{header} {key.title().replace('_', ' ')}\n")
                for k, v in value.items():
                    process_section(k, v, level + 1)
            elif isinstance(value, list):
                content.append(f"\n{header} {key.title().replace('_', ' ')}\n")
                for item in value:
                    if isinstance(item, dict):
                        process_section("", item, level + 1)
                    else:
                        content.append(f"- {str(item)}\n")
            else:
                content.append(f"**{key.title()}:** {value}\n\n")

        for section, details in data.items():
            process_section(section, details)

        # Write to file
        with open(filename, "w", encoding="utf-8") as f:
            f.writelines(content)

        return os.path.abspath(filename)

    except Exception as e:
        raise RuntimeError(f"Failed to save Markdown: {str(e)}") from e

def merge_content_creator_info(source1: Dict[str, Any], 
                              source2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge two content creator information dictionaries
    
    Args:
        source1: Primary data source
        source2: Secondary data source
        
    Returns:
        Merged dictionary with combined information
        
    Example:
        >>> merge_content_creator_info(
            {"values": [{"name": "Honesty"}]},
            {"values": [{"name": "Quality"}], "challenges": [...]}
        )
    """
    merged = source1.copy()
    
    def recursive_merge(base: Any, update: Any):
        if isinstance(base, dict) and isinstance(update, dict):
            for key, val in update.items():
                if key in base:
                    base[key] = recursive_merge(base[key], val)
                else:
                    base[key] = val
            return base
        if isinstance(base, list) and isinstance(update, list):
            return base + update
        return update
    
    return recursive_merge(merged, source2)

def ensure_dict(data: Union[BaseModel, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Convert Pydantic models to dictionaries while handling raw dicts
    
    Args:
        data: Input data (either Pydantic model or dictionary)
        
    Returns:
        Dictionary representation of the input
        
    Example:
        >>> ensure_dict(ContentCreatorInfo(...))
        {personal_info: {...}, ...}
    """
    if isinstance(data, BaseModel):
        return data.dict()
    if isinstance(data, dict):
        return data
    raise ValueError("Input must be Pydantic model or dictionary")

def validate_youtube_url(url: str) -> bool:
    """
    Validate YouTube channel/Video URL format
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid YouTube URL, False otherwise
        
    Example:
        >>> validate_youtube_url("https://youtube.com/@channel")
        True
    """
    patterns = [
        r"(https?://)?(www\.)?youtube\.com/(channel/|@|user/)[\w-]+",
        r"(https?://)?(www\.)?youtu\.be/[\w-]+"
    ]
    return any(re.match(pattern, url) for pattern in patterns)

def calculate_career_duration(start_year: int) -> int:
    """
    Calculate career duration in years
    
    Args:
        start_year: Year the channel was created
        
    Returns:
        Number of years active
        
    Example:
        >>> calculate_career_duration(2018)
        5
    """
    current_year = datetime.now().year
    return max(current_year - start_year, 0)

def datetime_converter(obj):
    """
    JSON serializer for datetime objects
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    """
    Load project configuration from JSON file
    
    Args:
        config_path: Path to config file
        
    Returns:
        Dictionary with configuration settings
    """
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in config file")
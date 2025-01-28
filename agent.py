# agent.py

import os
from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

# Local imports
from models import (
    ContentCreatorInfo,
    ValueObject,
    ChallengeObject,
    AchievementObject,
    LifeEventObject,
    BusinessObject
)
from utils import save_output_to_markdown, merge_content_creator_info, ensure_dict

class AgentConfig(BaseModel):
    """
    Configuration model for the analysis agent
    
    Attributes:
        name: Name of the agent
        role: Description of the agent's purpose
        last_active: Timestamp of last activity
    """
    name: str = Field(..., description="Name of the analysis agent")
    role: str = Field(..., description="Agent's purpose and capabilities")
    last_active: Optional[datetime] = None

class ContentAnalysisAgent:
    """
    AI Agent for analyzing YouTube content creator data
    
    Capabilities:
    - Merges data from multiple sources
    - Performs comprehensive analysis
    - Generates structured reports
    - Maintains activity tracking
    """
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.last_active = datetime.now()
        self.analysis_history = []

    def update_activity(self):
        """Update agent's last activity timestamp"""
        self.last_active = datetime.now()

    def analyze_creator(self, creator_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of content creator data
        
        Args:
            creator_data: Raw creator data from multiple sources
            
        Returns:
            Dictionary containing structured analysis results
        """
        self.update_activity()
        
        # Convert to dict if Pydantic model
        data = ensure_dict(creator_data)
        
        # Perform analysis
        analysis = {
            "basic_stats": self._calculate_basic_stats(data),
            "business_analysis": self._analyze_business(data),
            "values_assessment": self._assess_values(data),
            "timeline_analysis": self._analyze_timelines(data)
        }
        
        self.analysis_history.append(analysis)
        return analysis

    def _calculate_basic_stats(self, data: Dict) -> Dict:
        """Calculate basic statistics from creator data"""
        return {
            "total_life_events": len(data.get("life_events", [])),
            "total_challenges": len(data.get("challenges", [])),
            "total_achievements": len(data.get("achievements", [])),
            "business_count": len(data.get("businesses", []))
        }

    def _analyze_business(self, data: Dict) -> Dict:
        """Analyze business ventures and financial aspects"""
        businesses = data.get("businesses", [])
        return {
            "total_businesses": len(businesses),
            "active_businesses": sum(1 for b in businesses if b.get("is_active", False)),
            "average_revenue": sum(b.get("revenue", 0) for b in businesses) / len(businesses) if businesses else 0
        }

    def _assess_values(self, data: Dict) -> Dict:
        """Evaluate and score creator's core values"""
        values = data.get("values", [])
        return {
            "core_values": [v["name"] for v in values],
            "value_consistency_score": len(values) / 10  # Simplified scoring
        }

    def _analyze_timelines(self, data: Dict) -> Dict:
        """Analyze temporal patterns in creator's career"""
        events = sorted(data.get("life_events", []), 
                       key=lambda x: x.get("year", 0))
        return {
            "career_start": events[0]["year"] if events else None,
            "milestone_frequency": len(events) / (datetime.now().year - events[0]["year"]) if events else 0
        }

    def generate_report(self, analysis: Dict, format: str = "markdown") -> str:
        """
        Generate formatted report from analysis results
        
        Args:
            analysis: Analysis dictionary from analyze_creator
            format: Output format (markdown/json)
            
        Returns:
            Path to generated report file
        """
        self.update_activity()
        
        filename = f"creator_report_{datetime.now().strftime('%Y%m%d%H%M')}.{format}"
        
        if format == "markdown":
            save_output_to_markdown(analysis, filename)
        elif format == "json":
            with open(filename, "w") as f:
                json.dump(analysis, f)
        else:
            raise ValueError("Unsupported format. Use 'markdown' or 'json'")
            
        return os.path.abspath(filename)

    def merge_data_sources(self, *sources: Dict) -> Dict:
        """
        Merge multiple data sources into unified format
        
        Args:
            sources: Multiple creator data dictionaries
            
        Returns:
            Merged and normalized creator data
        """
        self.update_activity()
        
        merged = {}
        for source in sources:
            merged = merge_content_creator_info(merged, ensure_dict(source))
            
        return merged

if __name__ == "__main__":
    # Example usage
    config = AgentConfig(
        name="CreatorAnalyzer v1.0",
        role="Comprehensive analysis of YouTube content creators"
    )
    
    agent = ContentAnalysisAgent(config)
    
    # Sample data
    source1 = {
        "life_events": [
            {"name": "Channel Launch", "year": 2018, "impact": "High"}
        ],
        "businesses": [
            {"name": "Merch Store", "revenue": 5000, "is_active": True}
        ]
    }
    
    source2 = {
        "values": [
            {"name": "Authenticity", "origin": "Personal Philosophy"}
        ],
        "achievements": [
            {"description": "100k Subscribers", "year": 2020}
        ]
    }
    
    # Merge and analyze
    merged_data = agent.merge_data_sources(source1, source2)
    analysis = agent.analyze_creator(merged_data)
    
    # Generate report
    report_path = agent.generate_report(analysis)
    print(f"Report generated at: {report_path}")

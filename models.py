# models.py

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from datetime import datetime

class ValueObject(BaseModel):
    """
    Represents a core value of a content creator
    
    Attributes:
        name: Name of the value (e.g., "Authenticity")
        origin: Where this value originated from
        impact_today: How this value influences current work
        description: Detailed explanation of the value
    """
    name: str = Field(..., min_length=2, max_length=50)
    origin: str = Field("Personal belief", description="Source of this value")
    impact_today: str = Field(..., description="Current impact on content creation")
    description: Optional[str] = Field(None, max_length=500)

class ChallengeObject(BaseModel):
    """
    Represents a significant challenge faced by the creator
    
    Attributes:
        description: Brief description of the challenge
        year: Year the challenge occurred
        learnings: Key takeaways from overcoming the challenge
        duration: How long the challenge lasted (months)
    """
    description: str = Field(..., min_length=10, max_length=200)
    year: int = Field(..., ge=2005, le=datetime.now().year)
    learnings: str = Field(..., min_length=10, max_length=500)
    duration: Optional[int] = Field(None, ge=1, le=120)

class AchievementObject(BaseModel):
    """
    Represents a notable achievement of the content creator
    
    Attributes:
        description: Description of the achievement
        year: Year achieved
        impact: How this achievement affected their career
        metrics: Quantitative measures of success
    """
    description: str = Field(..., min_length=10, max_length=200)
    year: int = Field(..., ge=2005, le=datetime.now().year)
    impact: str = Field(..., min_length=10, max_length=500)
    metrics: Dict[str, float] = Field(
        default_factory=dict,
        example={"subscribers_gained": 100000, "revenue_increase": 45.5}
    )

class LifeEventObject(BaseModel):
    """
    Represents a significant life event affecting the creator's career
    
    Attributes:
        name: Name/Title of the event
        year: Year of occurrence
        description: Detailed description of the event
        impact: How it influenced their content creation
    """
    name: str = Field(..., min_length=2, max_length=100)
    year: int = Field(..., ge=1900, le=datetime.now().year)
    description: str = Field(..., min_length=10, max_length=500)
    impact: str = Field(..., min_length=10, max_length=500)
    category: Optional[str] = Field(None, pattern="^(personal|professional|financial)$")

class BusinessObject(BaseModel):
    """
    Represents a business venture associated with the creator
    
    Attributes:
        name: Business name
        description: Brief description of the business
        year_started: Launch year
        annual_revenue: Estimated yearly revenue (USD)
        business_type: Type of business
        status: Current operational status
    """
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=10, max_length=500)
    year_started: int = Field(..., ge=2005, le=datetime.now().year)
    annual_revenue: Optional[float] = Field(None, ge=0)
    business_type: str = Field(
        ...,
        pattern="^(merchandise|courses|sponsorships|production|other)$"
    )
    status: str = Field("active", pattern="^(active|inactive|sold|acquired)$")

    @field_validator('year_started')
    def validate_year_started(cls, value):
        if value > datetime.now().year:
            raise ValueError("Business cannot start in the future")
        return value

class PersonalInfo(BaseModel):
    """
    Core personal information about the content creator
    
    Attributes:
        full_name: Creator's full name
        channel_name: YouTube channel name
        channel_url: YouTube channel URL
        niche: Primary content category
        start_year: Year channel was created
        country: Base country
        team_size: Number of people in production team
    """
    full_name: str = Field(..., min_length=2, max_length=100)
    channel_name: str = Field(..., min_length=2, max_length=100)
    channel_url: str = Field(..., pattern=r"^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+")
    niche: str = Field(..., min_length=2, max_length=50)
    start_year: int = Field(..., ge=2005, le=datetime.now().year)
    country: Optional[str] = Field(None, min_length=2, max_length=56)
    team_size: int = Field(1, ge=1, le=1000)


class ContentCreatorInfo(BaseModel):
    """
    Comprehensive model representing all information about a content creator
    
    Attributes:
        personal_info: Core personal/channel information
        values: List of core values
        challenges: List of faced challenges
        achievements: List of career achievements
        life_events: Significant personal/professional events
        businesses: Associated business ventures
        analysis_metadata: Technical metadata about the analysis
    """
    personal_info: PersonalInfo
    values: List[ValueObject] = Field(default_factory=list)
    challenges: List[ChallengeObject] = Field(default_factory=list)
    achievements: List[AchievementObject] = Field(default_factory=list)
    life_events: List[LifeEventObject] = Field(default_factory=list)
    businesses: List[BusinessObject] = Field(default_factory=list)
    analysis_metadata: Dict[str, Any] = Field(
        default_factory=lambda: {
            "last_updated": datetime.now().isoformat(),
            "analysis_version": "1.0"
        }
    )

    class Config:
        schema_extra = {
            "example": {
                "personal_info": {
                    "full_name": "John Creator",
                    "channel_name": "Tech Innovators",
                    "channel_url": "https://youtube.com/techinnovators",
                    "niche": "Technology",
                    "start_year": 2018,
                    "country": "United States",
                    "team_size": 5
                },
                "values": [{
                    "name": "Transparency",
                    "origin": "Community feedback",
                    "impact_today": "Drives open communication with audience",
                    "description": "Commitment to honest content creation"
                }]
            }
        }

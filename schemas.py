from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


# ── Event ──────────────────────────────────────────────────────────────────

class EventCategory(str, Enum):
    workshopE    = "workshopE"
    seminarE     = "seminarE"
    competitionE = "competitionE"
    sportsE      = "sportsE"
    culturalE    = "culturalE"
    internshipE  = "internshipE"


class EventSchema(BaseModel):
    title:                str            = Field(description="Title of the event")
    description:          str            = Field(description="Detailed description of the event")
    date:                 Optional[str]  = Field(None, description="Event date in YYYY-MM-DD format")
    time:                 Optional[str]  = Field(None, description="Event time e.g. 10:00 AM")
    location:             Optional[str]  = Field(None, description="Venue or location, use 'DTU Campus' if not mentioned")
    category:             EventCategory  = Field(description="Category: workshopE, seminarE, competitionE, sportsE, culturalE, internshipE")
    registrationLink:     str            = Field(description="Registration link URL, use '#' if not available")
    registrationDeadline: Optional[str]  = Field(None, description="Registration deadline in YYYY-MM-DD format")
    organizer:            Optional[str]  = Field(None, description="Organizing body, use 'DTU' if not mentioned")
    featured:             bool           = Field(False, description="Whether this is a featured event")


# ── Society ────────────────────────────────────────────────────────────────

class SocietyCategory(str, Enum):
    culturalS  = "culturalS"
    technicalS = "technicalS"
    sportsS    = "sportsS"
    academicS  = "academicS"
    socialS    = "socialS"
    creativeS  = "creativeS"
    businessS  = "businessS"


class ContactSchema(BaseModel):
    whatsappLink: Optional[str] = None
    phone:        Optional[str] = None


class SocialMediaSchema(BaseModel):
    discord:   Optional[str] = None
    instagram: Optional[str] = None
    linkedin:  Optional[str] = None


class SocietySchema(BaseModel):
    name:                 str                      = Field(description="Name of the society")
    description:          str                      = Field(description="Short description of the society")
    fullDescription:      Optional[str]            = Field(None, description="Detailed description")
    category:             SocietyCategory          = Field(description="Category: culturalS, technicalS, sportsS, academicS, socialS, creativeS, businessS")
    seats:                Optional[int]            = Field(None, description="Number of available seats")
    featured:             bool                     = Field(False, description="Whether this is a featured society")
    registrationOpen:     bool                     = Field(True, description="Whether registration is open")
    registrationDeadline: Optional[str]            = Field(None, description="Deadline in YYYY-MM-DD format")
    registrationLink:     Optional[str]            = Field(None, description="Registration link URL")
    location:             Optional[str]            = Field(None, description="Meeting location")
    contact:              Optional[ContactSchema]  = Field(None, description="Contact details")
    requirements:         Optional[str]            = Field(None, description="Requirements to join")
    socialMedia:          Optional[SocialMediaSchema] = Field(None, description="Social media links")

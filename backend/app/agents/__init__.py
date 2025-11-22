"""
Stellar AI Mentor Agent System

This module contains the gold-standard pedagogical AI mentor agents:
- Supervisor: Routes conversations to appropriate subject mentors
- 8 Specialized Mentors: Each with unique subject expertise and teaching style

All agents follow research-backed pedagogical principles and Socratic communication patterns.
"""
from .personas import MENTOR_PERSONAS, get_mentor_by_id, get_supervisor
from .mentor_engine import MentorEngine
from .supervisor import SupervisorAgent

__all__ = [
    "MENTOR_PERSONAS",
    "get_mentor_by_id",
    "get_supervisor",
    "MentorEngine",
    "SupervisorAgent",
]

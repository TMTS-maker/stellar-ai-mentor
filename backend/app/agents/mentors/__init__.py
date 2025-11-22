"""
Mentor Agents Package

All 8 AI mentor agents for different subjects
"""
from app.agents.mentors.stella import StellaMentor
from app.agents.mentors.max import MaxMentor
from app.agents.mentors.nova import NovaMentor
from app.agents.mentors.darwin import DarwinMentor
from app.agents.mentors.lexis import LexisMentor
from app.agents.mentors.neo import NeoMentor
from app.agents.mentors.luna import LunaMentor
from app.agents.mentors.atlas import AtlasMentor

__all__ = [
    "StellaMentor",
    "MaxMentor",
    "NovaMentor",
    "DarwinMentor",
    "LexisMentor",
    "NeoMentor",
    "LunaMentor",
    "AtlasMentor",
]

# Mentor registry for easy access
MENTOR_REGISTRY = {
    "stella": StellaMentor,
    "max": MaxMentor,
    "nova": NovaMentor,
    "darwin": DarwinMentor,
    "lexis": LexisMentor,
    "neo": NeoMentor,
    "luna": LunaMentor,
    "atlas": AtlasMentor,
}


def get_mentor(mentor_id: str):
    """
    Get mentor instance by ID

    Args:
        mentor_id: ID of mentor ('stella', 'max', etc.)

    Returns:
        Mentor instance

    Raises:
        KeyError: If mentor_id not found
    """
    if mentor_id not in MENTOR_REGISTRY:
        raise KeyError(f"Unknown mentor: {mentor_id}")

    MentorClass = MENTOR_REGISTRY[mentor_id]
    return MentorClass()


def list_mentors():
    """
    List all available mentors

    Returns:
        List of mentor info dicts
    """
    mentors = []
    for mentor_id, MentorClass in MENTOR_REGISTRY.items():
        mentor = MentorClass()
        mentors.append(mentor.get_agent_info())
    return mentors

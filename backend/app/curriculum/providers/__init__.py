"""
Curriculum Providers

Provider implementations for different curriculum sources:
- Indian provider (CBSE, ICSE)
- UK provider (National Curriculum, IGCSE)
- US provider (Common Core)
"""

from .base import BaseCurriculumProvider, CurriculumData
from .indian import IndianCurriculumProvider
from .uk import UKCurriculumProvider
from .us import USCurriculumProvider

__all__ = [
    "BaseCurriculumProvider",
    "CurriculumData",
    "IndianCurriculumProvider",
    "UKCurriculumProvider",
    "USCurriculumProvider",
]

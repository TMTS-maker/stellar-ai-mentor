"""
Curriculum Integration Module

Provides multi-curriculum support for:
- Indian curricula (CBSE, ICSE)
- UK curricula (National Curriculum, IGCSE, A-level)
- US curricula (Common Core State Standards)

Features:
- Provider abstraction for API/MCP/static data ingestion
- Curriculum mapping to grades, subjects, units, topics, learning objectives
- Integration with Stellecta agents, LVO, H-PEM, LCT
"""

from .service import CurriculumService
from .providers.base import BaseCurriculumProvider, CurriculumData

__all__ = ["CurriculumService", "BaseCurriculumProvider", "CurriculumData"]

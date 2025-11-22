"""
LCT - Learning Competency Trajectories

Tracks student progression through curriculum learning objectives.
Integrates with:
- Curriculum learning objectives
- LVO phases (Learn-Verify-Own)
- H-PEM strategies (History-Practice-Evaluation-Metacognition)
- Competency records

Features:
- Track competency progression
- Identify learning gaps
- Recommend next objectives
- Predict mastery timelines
- Spaced repetition for practice
"""

from .trajectories import LCTEngine

__all__ = ["LCTEngine"]

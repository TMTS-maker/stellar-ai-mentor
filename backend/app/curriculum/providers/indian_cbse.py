"""
Indian CBSE Curriculum Provider

Implements curriculum objectives for CBSE (Central Board of Secondary Education)
"""

from typing import List, Optional
from app.curriculum.base_provider import BaseCurriculumProvider, CurriculumObjectiveData


class IndianCBSEProvider(BaseCurriculumProvider):
    """
    Indian CBSE Curriculum Provider

    Covers grades 1-12 across all subjects
    """

    def __init__(self):
        super().__init__(
            curriculum_type="INDIAN_CBSE",
            curriculum_name="CBSE (Central Board of Secondary Education)",
            country="India",
            board="CBSE",
        )
        self._initialize_objectives()

    def _initialize_objectives(self):
        """Initialize CBSE curriculum objectives"""
        self.objectives = {}

        # Sample CBSE Math Grade 10 objectives
        # In production, this would load from a comprehensive curriculum database
        self.objectives.update(self._get_grade_10_math_objectives())
        self.objectives.update(self._get_grade_10_physics_objectives())
        self.objectives.update(self._get_grade_10_chemistry_objectives())
        # ... other subjects and grades would be added

    def _get_grade_10_math_objectives(self) -> dict:
        """Grade 10 Mathematics objectives"""
        return {
            "CBSE_MATH_10_ALG_001": CurriculumObjectiveData(
                objective_code="CBSE_MATH_10_ALG_001",
                objective_text="Solve quadratic equations using factorization, completing the square, and quadratic formula",
                subject="MATH",
                grade_level=10,
                topic="Algebra",
                subtopic="Quadratic Equations",
                difficulty_level=5,
                blooms_level="Apply",
                description="Students will learn to solve quadratic equations using multiple methods including factorization, completing the square, and the quadratic formula.",
                example_questions=[
                    "Solve: x² + 5x + 6 = 0",
                    "Find roots of: 2x² - 7x + 3 = 0 using quadratic formula",
                    "Complete the square: x² + 6x + 5 = 0",
                ],
                prerequisite_codes=["CBSE_MATH_9_ALG_003", "CBSE_MATH_9_ALG_005"],
            ),
            "CBSE_MATH_10_GEO_001": CurriculumObjectiveData(
                objective_code="CBSE_MATH_10_GEO_001",
                objective_text="Apply theorems related to circles including tangent properties and chord theorems",
                subject="MATH",
                grade_level=10,
                topic="Geometry",
                subtopic="Circles",
                difficulty_level=6,
                blooms_level="Apply",
                description="Study properties of circles, tangents, chords, and their theorems.",
                example_questions=[
                    "Prove that the tangent at any point of a circle is perpendicular to the radius",
                    "Find the length of tangent from an external point",
                ],
                prerequisite_codes=["CBSE_MATH_9_GEO_002"],
            ),
            "CBSE_MATH_10_TRIG_001": CurriculumObjectiveData(
                objective_code="CBSE_MATH_10_TRIG_001",
                objective_text="Understand and apply trigonometric ratios of acute angles",
                subject="MATH",
                grade_level=10,
                topic="Trigonometry",
                subtopic="Trigonometric Ratios",
                difficulty_level=5,
                blooms_level="Understand",
                description="Learn sin, cos, tan, cot, sec, cosec and their relationships.",
                example_questions=[
                    "Find sin(30°), cos(45°), tan(60°)",
                    "If sin A = 3/5, find cos A and tan A",
                ],
                prerequisite_codes=["CBSE_MATH_9_GEO_001"],
            ),
            "CBSE_MATH_10_STAT_001": CurriculumObjectiveData(
                objective_code="CBSE_MATH_10_STAT_001",
                objective_text="Calculate mean, median, mode for grouped and ungrouped data",
                subject="MATH",
                grade_level=10,
                topic="Statistics",
                subtopic="Measures of Central Tendency",
                difficulty_level=4,
                blooms_level="Apply",
                description="Learn to calculate and interpret mean, median, and mode for different data sets.",
                example_questions=[
                    "Find the mean of the frequency distribution",
                    "Calculate median for grouped data",
                ],
                prerequisite_codes=["CBSE_MATH_9_STAT_001"],
            ),
        }

    def _get_grade_10_physics_objectives(self) -> dict:
        """Grade 10 Physics objectives"""
        return {
            "CBSE_PHY_10_LIGHT_001": CurriculumObjectiveData(
                objective_code="CBSE_PHY_10_LIGHT_001",
                objective_text="Understand laws of reflection and refraction of light",
                subject="PHYSICS",
                grade_level=10,
                topic="Light - Reflection and Refraction",
                subtopic="Laws of Reflection",
                difficulty_level=4,
                blooms_level="Understand",
                description="Study reflection of light from plane and spherical mirrors, and refraction through different media.",
                example_questions=["State the laws of reflection", "Derive the mirror formula"],
                prerequisite_codes=["CBSE_PHY_9_LIGHT_001"],
            ),
            "CBSE_PHY_10_ELEC_001": CurriculumObjectiveData(
                objective_code="CBSE_PHY_10_ELEC_001",
                objective_text="Apply Ohm's law and understand series and parallel circuits",
                subject="PHYSICS",
                grade_level=10,
                topic="Electricity",
                subtopic="Electric Current and Circuits",
                difficulty_level=5,
                blooms_level="Apply",
                description="Learn electric current, potential difference, resistance, Ohm's law, and circuit analysis.",
                example_questions=[
                    "Calculate resistance using Ohm's law",
                    "Find equivalent resistance in series and parallel",
                ],
                prerequisite_codes=["CBSE_PHY_9_ELEC_001"],
            ),
        }

    def _get_grade_10_chemistry_objectives(self) -> dict:
        """Grade 10 Chemistry objectives"""
        return {
            "CBSE_CHEM_10_ACID_001": CurriculumObjectiveData(
                objective_code="CBSE_CHEM_10_ACID_001",
                objective_text="Understand properties of acids, bases, and salts",
                subject="CHEMISTRY",
                grade_level=10,
                topic="Acids, Bases and Salts",
                subtopic="Chemical Properties",
                difficulty_level=4,
                blooms_level="Understand",
                description="Study chemical properties of acids, bases, pH scale, and salt formation.",
                example_questions=[
                    "What happens when acid reacts with base?",
                    "Explain pH scale and its importance",
                ],
                prerequisite_codes=["CBSE_CHEM_9_MATTER_001"],
            ),
        }

    def get_objectives_for_grade_subject(
        self, grade_level: int, subject: str
    ) -> List[CurriculumObjectiveData]:
        """Get all objectives for grade and subject"""
        return [
            obj
            for obj in self.objectives.values()
            if obj.grade_level == grade_level and obj.subject == subject
        ]

    def get_objective_by_code(self, objective_code: str) -> Optional[CurriculumObjectiveData]:
        """Get specific objective by code"""
        return self.objectives.get(objective_code)

    def get_prerequisite_chain(self, objective_code: str) -> List[str]:
        """Get prerequisite chain"""
        obj = self.objectives.get(objective_code)
        if not obj:
            return []

        chain = []
        for prereq in obj.prerequisite_codes:
            chain.append(prereq)
            # Recursively get prerequisites of prerequisites
            chain.extend(self.get_prerequisite_chain(prereq))

        return list(dict.fromkeys(chain))  # Remove duplicates while preserving order

    def get_next_objectives(self, objective_code: str) -> List[str]:
        """Get objectives that build on this one"""
        next_objs = []
        for code, obj in self.objectives.items():
            if objective_code in obj.prerequisite_codes:
                next_objs.append(code)
        return next_objs

    def search_objectives(
        self, query: str, subject: Optional[str] = None, grade_level: Optional[int] = None
    ) -> List[CurriculumObjectiveData]:
        """Search objectives by query"""
        query_lower = query.lower()
        results = []

        for obj in self.objectives.values():
            # Apply filters
            if subject and obj.subject != subject:
                continue
            if grade_level and obj.grade_level != grade_level:
                continue

            # Search in text fields
            if (
                query_lower in obj.objective_text.lower()
                or query_lower in obj.topic.lower()
                or (obj.subtopic and query_lower in obj.subtopic.lower())
                or (obj.description and query_lower in obj.description.lower())
            ):
                results.append(obj)

        return results

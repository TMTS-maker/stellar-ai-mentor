"""
UK National Curriculum Provider

Implements curriculum objectives for UK National Curriculum and IGCSE
"""
from typing import List, Optional
from app.curriculum.base_provider import BaseCurriculumProvider, CurriculumObjectiveData


class UKNationalProvider(BaseCurriculumProvider):
    """
    UK National Curriculum & IGCSE Provider

    Covers Key Stages 1-4 (roughly ages 5-16)
    """

    def __init__(self, variant: str = "NATIONAL"):
        """
        Args:
            variant: "NATIONAL" or "IGCSE"
        """
        curriculum_type = f"UK_{variant}"
        curriculum_name = f"UK {'National Curriculum' if variant == 'NATIONAL' else 'IGCSE'}"

        super().__init__(
            curriculum_type=curriculum_type,
            curriculum_name=curriculum_name,
            country="United Kingdom",
            board="Edexcel" if variant == "IGCSE" else None
        )
        self.variant = variant
        self._initialize_objectives()

    def _initialize_objectives(self):
        """Initialize UK curriculum objectives"""
        self.objectives = {}

        # Sample objectives for Year 10 (Key Stage 4)
        self.objectives.update(self._get_year_10_math_objectives())
        self.objectives.update(self._get_year_10_science_objectives())

    def _get_year_10_math_objectives(self) -> dict:
        """Year 10 Mathematics objectives"""
        prefix = "UKNAT" if self.variant == "NATIONAL" else "UKIGCSE"

        return {
            f"{prefix}_MATH_10_NUM_001": CurriculumObjectiveData(
                objective_code=f"{prefix}_MATH_10_NUM_001",
                objective_text="Use standard form to represent very large and very small numbers",
                subject="MATH",
                grade_level=10,
                topic="Number",
                subtopic="Standard Form",
                difficulty_level=5,
                blooms_level="Apply",
                description="Convert between ordinary numbers and standard form, and perform calculations.",
                example_questions=[
                    "Write 0.000045 in standard form",
                    "Calculate (3 × 10⁵) × (2 × 10⁻³)"
                ],
                prerequisite_codes=[f"{prefix}_MATH_9_NUM_002"]
            ),
            f"{prefix}_MATH_10_ALG_001": CurriculumObjectiveData(
                objective_code=f"{prefix}_MATH_10_ALG_001",
                objective_text="Solve simultaneous equations algebraically and graphically",
                subject="MATH",
                grade_level=10,
                topic="Algebra",
                subtopic="Simultaneous Equations",
                difficulty_level=6,
                blooms_level="Apply",
                description="Solve pairs of simultaneous linear equations using elimination, substitution, and graphical methods.",
                example_questions=[
                    "Solve: 2x + 3y = 12 and x - y = 1",
                    "Find the point of intersection graphically"
                ],
                prerequisite_codes=[f"{prefix}_MATH_9_ALG_001"]
            ),
            f"{prefix}_MATH_10_GEOM_001": CurriculumObjectiveData(
                objective_code=f"{prefix}_MATH_10_GEOM_001",
                objective_text="Apply circle theorems to solve geometric problems",
                subject="MATH",
                grade_level=10,
                topic="Geometry",
                subtopic="Circle Theorems",
                difficulty_level=7,
                blooms_level="Analyze",
                description="Use circle theorems including angles at centre, cyclic quadrilaterals, and tangents.",
                example_questions=[
                    "Prove that angles in the same segment are equal",
                    "Calculate missing angles using circle theorems"
                ],
                prerequisite_codes=[f"{prefix}_MATH_9_GEOM_001"]
            ),
        }

    def _get_year_10_science_objectives(self) -> dict:
        """Year 10 Science objectives"""
        prefix = "UKNAT" if self.variant == "NATIONAL" else "UKIGCSE"

        return {
            f"{prefix}_PHYS_10_FORCES_001": CurriculumObjectiveData(
                objective_code=f"{prefix}_PHYS_10_FORCES_001",
                objective_text="Calculate work done, force, and distance using equations",
                subject="PHYSICS",
                grade_level=10,
                topic="Forces",
                subtopic="Work and Energy",
                difficulty_level=5,
                blooms_level="Apply",
                description="Understand work done as energy transfer and apply W = Fd equation.",
                example_questions=[
                    "Calculate work done when a 50N force moves an object 10m",
                    "How much energy is transferred when pushing a box?"
                ],
                prerequisite_codes=[f"{prefix}_PHYS_9_FORCES_001"]
            ),
            f"{prefix}_CHEM_10_ATOMIC_001": CurriculumObjectiveData(
                objective_code=f"{prefix}_CHEM_10_ATOMIC_001",
                objective_text="Understand atomic structure and the periodic table",
                subject="CHEMISTRY",
                grade_level=10,
                topic="Atomic Structure",
                subtopic="Atoms and Elements",
                difficulty_level=4,
                blooms_level="Understand",
                description="Learn about protons, neutrons, electrons, and how elements are arranged in the periodic table.",
                example_questions=[
                    "Describe the structure of an atom",
                    "Explain why elements are arranged in groups"
                ],
                prerequisite_codes=[f"{prefix}_CHEM_9_MATTER_001"]
            ),
        }

    def get_objectives_for_grade_subject(
        self,
        grade_level: int,
        subject: str
    ) -> List[CurriculumObjectiveData]:
        """Get all objectives for grade and subject"""
        return [
            obj for obj in self.objectives.values()
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
            chain.extend(self.get_prerequisite_chain(prereq))

        return list(dict.fromkeys(chain))

    def get_next_objectives(self, objective_code: str) -> List[str]:
        """Get objectives that build on this one"""
        next_objs = []
        for code, obj in self.objectives.items():
            if objective_code in obj.prerequisite_codes:
                next_objs.append(code)
        return next_objs

    def search_objectives(
        self,
        query: str,
        subject: Optional[str] = None,
        grade_level: Optional[int] = None
    ) -> List[CurriculumObjectiveData]:
        """Search objectives by query"""
        query_lower = query.lower()
        results = []

        for obj in self.objectives.values():
            if subject and obj.subject != subject:
                continue
            if grade_level and obj.grade_level != grade_level:
                continue

            if (query_lower in obj.objective_text.lower() or
                query_lower in obj.topic.lower() or
                (obj.subtopic and query_lower in obj.subtopic.lower())):
                results.append(obj)

        return results

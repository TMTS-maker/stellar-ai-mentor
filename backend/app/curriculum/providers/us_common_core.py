"""
US Common Core Curriculum Provider

Implements curriculum objectives for US Common Core State Standards
"""

from typing import List, Optional
from app.curriculum.base_provider import BaseCurriculumProvider, CurriculumObjectiveData


class USCommonCoreProvider(BaseCurriculumProvider):
    """
    US Common Core State Standards Provider

    Covers grades K-12
    """

    def __init__(self):
        super().__init__(
            curriculum_type="US_COMMON_CORE",
            curriculum_name="Common Core State Standards",
            country="United States",
            board="Common Core",
        )
        self._initialize_objectives()

    def _initialize_objectives(self):
        """Initialize Common Core curriculum objectives"""
        self.objectives = {}

        # Sample objectives for Grade 10
        self.objectives.update(self._get_grade_10_math_objectives())
        self.objectives.update(self._get_grade_10_science_objectives())
        self.objectives.update(self._get_grade_10_english_objectives())

    def _get_grade_10_math_objectives(self) -> dict:
        """Grade 10 Mathematics objectives (Algebra II, Geometry)"""
        return {
            "CCSS_MATH_10_ALG_001": CurriculumObjectiveData(
                objective_code="CCSS_MATH_10_ALG_001",
                objective_text="Create equations and inequalities in one variable and use them to solve problems",
                subject="MATH",
                grade_level=10,
                topic="Algebra",
                subtopic="Creating Equations",
                difficulty_level=6,
                blooms_level="Create",
                description="Create equations in one variable and use them to solve problems. Include equations arising from linear and quadratic functions.",
                example_questions=[
                    "Write an equation to model a real-world problem",
                    "Solve problems using linear inequalities",
                ],
                prerequisite_codes=["CCSS_MATH_9_ALG_002"],
            ),
            "CCSS_MATH_10_GEOM_001": CurriculumObjectiveData(
                objective_code="CCSS_MATH_10_GEOM_001",
                objective_text="Prove theorems about triangles using geometric methods",
                subject="MATH",
                grade_level=10,
                topic="Geometry",
                subtopic="Congruence and Similarity",
                difficulty_level=7,
                blooms_level="Analyze",
                description="Prove theorems about triangles. Theorems include: measures of interior angles of a triangle sum to 180°; base angles of isosceles triangles are congruent.",
                example_questions=[
                    "Prove that the angles of a triangle sum to 180°",
                    "Prove properties of isosceles triangles",
                ],
                prerequisite_codes=["CCSS_MATH_9_GEOM_001"],
            ),
            "CCSS_MATH_10_FUNC_001": CurriculumObjectiveData(
                objective_code="CCSS_MATH_10_FUNC_001",
                objective_text="Interpret functions that arise in applications in terms of context",
                subject="MATH",
                grade_level=10,
                topic="Functions",
                subtopic="Function Interpretation",
                difficulty_level=6,
                blooms_level="Analyze",
                description="For a function that models a relationship between two quantities, interpret key features of graphs and tables in terms of the quantities.",
                example_questions=[
                    "Interpret the slope and intercept of a linear function",
                    "Analyze the graph of a quadratic function",
                ],
                prerequisite_codes=["CCSS_MATH_9_FUNC_001"],
            ),
        }

    def _get_grade_10_science_objectives(self) -> dict:
        """Grade 10 Science objectives (typically Biology or Chemistry)"""
        return {
            "NGSS_BIO_10_EVOL_001": CurriculumObjectiveData(
                objective_code="NGSS_BIO_10_EVOL_001",
                objective_text="Construct an explanation based on evidence that natural selection leads to adaptation",
                subject="BIOLOGY",
                grade_level=10,
                topic="Evolution",
                subtopic="Natural Selection",
                difficulty_level=6,
                blooms_level="Create",
                description="Construct an explanation based on evidence that the process of evolution primarily results from genetic variation, natural selection, and adaptation.",
                example_questions=[
                    "Explain how natural selection drives evolution",
                    "Give examples of adaptations in organisms",
                ],
                prerequisite_codes=["NGSS_BIO_9_CELLS_001"],
            ),
            "NGSS_CHEM_10_REACT_001": CurriculumObjectiveData(
                objective_code="NGSS_CHEM_10_REACT_001",
                objective_text="Develop models to illustrate changes in composition of the nucleus of atoms",
                subject="CHEMISTRY",
                grade_level=10,
                topic="Chemical Reactions",
                subtopic="Atomic Structure",
                difficulty_level=5,
                blooms_level="Create",
                description="Develop models to illustrate the changes in the composition of the nucleus of the atom and the energy released during radioactive decay.",
                example_questions=[
                    "Model atomic structure showing protons, neutrons, electrons",
                    "Explain radioactive decay processes",
                ],
                prerequisite_codes=["NGSS_CHEM_9_MATTER_001"],
            ),
        }

    def _get_grade_10_english_objectives(self) -> dict:
        """Grade 10 English Language Arts objectives"""
        return {
            "CCSS_ELA_10_READ_001": CurriculumObjectiveData(
                objective_code="CCSS_ELA_10_READ_001",
                objective_text="Cite strong and thorough textual evidence to support analysis of what the text says explicitly",
                subject="LANGUAGE",
                grade_level=10,
                topic="Reading",
                subtopic="Text Analysis",
                difficulty_level=6,
                blooms_level="Analyze",
                description="Cite strong and thorough textual evidence to support analysis of what the text says explicitly as well as inferences drawn from the text.",
                example_questions=[
                    "Analyze a passage and cite textual evidence",
                    "Draw inferences from text with support",
                ],
                prerequisite_codes=["CCSS_ELA_9_READ_001"],
            ),
            "CCSS_ELA_10_WRITE_001": CurriculumObjectiveData(
                objective_code="CCSS_ELA_10_WRITE_001",
                objective_text="Write arguments to support claims with clear reasons and relevant evidence",
                subject="LANGUAGE",
                grade_level=10,
                topic="Writing",
                subtopic="Argumentative Writing",
                difficulty_level=7,
                blooms_level="Create",
                description="Write arguments to support claims in an analysis of substantive topics or texts, using valid reasoning and relevant evidence.",
                example_questions=[
                    "Write an argumentative essay on a given topic",
                    "Construct a thesis statement with supporting evidence",
                ],
                prerequisite_codes=["CCSS_ELA_9_WRITE_001"],
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
        self, query: str, subject: Optional[str] = None, grade_level: Optional[int] = None
    ) -> List[CurriculumObjectiveData]:
        """Search objectives by query"""
        query_lower = query.lower()
        results = []

        for obj in self.objectives.values():
            if subject and obj.subject != subject:
                continue
            if grade_level and obj.grade_level != grade_level:
                continue

            if (
                query_lower in obj.objective_text.lower()
                or query_lower in obj.topic.lower()
                or (obj.subtopic and query_lower in obj.subtopic.lower())
            ):
                results.append(obj)

        return results

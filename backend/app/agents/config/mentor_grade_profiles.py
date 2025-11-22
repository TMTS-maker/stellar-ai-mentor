"""
Mentor Grade-Based Profiles

Defines grade band support, topic scope, and didactic strategies for each mentor
across Grades 1-12.

Grade Bands:
- G1-2: Early Elementary (ages 6-7)
- G3-4: Upper Elementary (ages 8-9)
- G5-8: Middle School (ages 10-13)
- G9-12: High School (ages 14-17)
"""
from typing import Dict, List, Optional


# ==============================================================================
# GRADE BAND DEFINITIONS
# ==============================================================================

GRADE_BANDS = {
    "G1-2": {"name": "Early Elementary", "grades": [1, 2], "age_range": "6-7"},
    "G3-4": {"name": "Upper Elementary", "grades": [3, 4], "age_range": "8-9"},
    "G5-8": {"name": "Middle School", "grades": [5, 6, 7, 8], "age_range": "10-13"},
    "G9-12": {"name": "High School", "grades": [9, 10, 11, 12], "age_range": "14-17"}
}


# ==============================================================================
# MENTOR GRADE PROFILES
# ==============================================================================

GRADE_BAND_PROFILES = {
    # ==========================================================================
    # STELLA - Mathematics
    # ==========================================================================
    "stella": {
        "supported_grades": range(1, 13),  # Grades 1-12
        "grade_bands": {
            "G1-2": {
                "topics": [
                    "Counting and number recognition (0-100)",
                    "Basic addition and subtraction (within 20)",
                    "Place value (ones, tens)",
                    "Simple shapes and patterns",
                    "Measuring length and time"
                ],
                "difficulty": "foundational",
                "didactic_notes": (
                    "Use concrete manipulatives language (blocks, counters). "
                    "Very simple vocabulary. Lots of visual examples and encouragement. "
                    "Short, focused sessions. Celebrate every small success."
                )
            },
            "G3-4": {
                "topics": [
                    "Multiplication and division (basic facts and strategies)",
                    "Fractions (halves, thirds, fourths; simple operations)",
                    "Place value to thousands",
                    "Area and perimeter",
                    "Basic graphs and data interpretation"
                ],
                "difficulty": "elementary",
                "didactic_notes": (
                    "Introduce abstract concepts gradually with visual models. "
                    "Use relatable word problems. Build on concrete understanding. "
                    "More scaffolding, step-by-step guidance."
                )
            },
            "G5-8": {
                "topics": [
                    "Fractions, decimals, and percentages",
                    "Ratios and proportions",
                    "Algebra basics (variables, expressions, simple equations)",
                    "Geometry (angles, area, volume)",
                    "Basic statistics and probability"
                ],
                "difficulty": "intermediate",
                "didactic_notes": (
                    "Transition to more abstract thinking. "
                    "Encourage multiple solution strategies. "
                    "Connect math to real-world applications. "
                    "Introduce formal notation gradually."
                )
            },
            "G9-12": {
                "topics": [
                    "Algebra (linear, quadratic, exponential functions)",
                    "Geometry (proofs, trigonometry)",
                    "Calculus (limits, derivatives, integrals)",
                    "Statistics (data analysis, probability distributions)",
                    "Advanced problem-solving and proofs"
                ],
                "difficulty": "advanced",
                "didactic_notes": (
                    "Focus on conceptual understanding and formal reasoning. "
                    "Challenge with proofs and applications. "
                    "Prepare for standardized tests (SAT, ACT). "
                    "Encourage mathematical communication."
                )
            }
        }
    },

    # ==========================================================================
    # MAX - Physics
    # ==========================================================================
    "max": {
        "supported_grades": range(5, 13),  # Grades 5-12 (physics concepts start in middle school)
        "grade_bands": {
            "G5-8": {
                "topics": [
                    "Forces and motion (Newton's laws, simple machines)",
                    "Energy (kinetic, potential, conservation)",
                    "Simple circuits and electricity basics",
                    "Waves and sound",
                    "Light and optics"
                ],
                "difficulty": "introductory",
                "didactic_notes": (
                    "Focus on intuitive understanding through experiments. "
                    "Use everyday examples (sports, toys, weather). "
                    "Minimize math complexity; emphasize observation. "
                    "Hands-on demonstrations and thought experiments."
                )
            },
            "G9-12": {
                "topics": [
                    "Kinematics and dynamics (with calculus in AP Physics)",
                    "Energy, work, and power",
                    "Electricity and magnetism",
                    "Thermodynamics",
                    "Waves, optics, and modern physics (quantum, relativity)"
                ],
                "difficulty": "advanced",
                "didactic_notes": (
                    "Integrate mathematical modeling (algebra, trigonometry, calculus). "
                    "Problem-solving focus. "
                    "Connect to engineering and real-world applications. "
                    "Prepare for AP Physics or college-level coursework."
                )
            }
        }
    },

    # ==========================================================================
    # NOVA - Chemistry
    # ==========================================================================
    "nova": {
        "supported_grades": range(5, 13),  # Grades 5-12
        "grade_bands": {
            "G5-8": {
                "topics": [
                    "States of matter (solid, liquid, gas)",
                    "Atoms and molecules basics",
                    "Chemical vs. physical changes",
                    "Mixtures and solutions",
                    "Acids and bases (basic concepts)"
                ],
                "difficulty": "introductory",
                "didactic_notes": (
                    "Concrete examples and safe demonstrations. "
                    "Visual models of atoms and molecules. "
                    "Emphasize safety and observation. "
                    "Simple experiments and predictions."
                )
            },
            "G9-12": {
                "topics": [
                    "Periodic table and atomic structure",
                    "Chemical bonding (ionic, covalent, metallic)",
                    "Chemical reactions and stoichiometry",
                    "Thermochemistry and equilibrium",
                    "Organic chemistry and biochemistry"
                ],
                "difficulty": "advanced",
                "didactic_notes": (
                    "Formal notation and equations. "
                    "Lab skills and experimental design. "
                    "Quantitative problem-solving (mole calculations). "
                    "Prepare for AP Chemistry or college coursework."
                )
            }
        }
    },

    # ==========================================================================
    # DARWIN - Biology
    # ==========================================================================
    "darwin": {
        "supported_grades": range(3, 13),  # Grades 3-12
        "grade_bands": {
            "G3-4": {
                "topics": [
                    "Living vs. non-living things",
                    "Plant and animal life cycles",
                    "Basic needs of organisms (food, water, shelter)",
                    "Habitats and ecosystems (simple)",
                    "Human body basics (organs, senses)"
                ],
                "difficulty": "foundational",
                "didactic_notes": (
                    "Use observation and exploration. "
                    "Simple vocabulary, lots of pictures and examples. "
                    "Connect to animals and plants students know. "
                    "Encourage curiosity about nature."
                )
            },
            "G5-8": {
                "topics": [
                    "Cells (plant, animal, microscopy)",
                    "Ecosystems and food chains",
                    "Human body systems (digestive, respiratory, circulatory)",
                    "Genetics basics (traits, heredity)",
                    "Evolution and adaptation (introduction)"
                ],
                "difficulty": "intermediate",
                "didactic_notes": (
                    "Introduce microscopic world and systems thinking. "
                    "Hands-on activities (dissections, models). "
                    "Connect to health and environment. "
                    "Encourage scientific inquiry."
                )
            },
            "G9-12": {
                "topics": [
                    "Cell biology (organelles, cellular respiration, photosynthesis)",
                    "Genetics (DNA, RNA, Mendelian genetics, molecular genetics)",
                    "Evolution (natural selection, speciation, evidence)",
                    "Ecology (populations, energy flow, biomes)",
                    "Human anatomy and physiology (detailed)"
                ],
                "difficulty": "advanced",
                "didactic_notes": (
                    "Detailed molecular and systems-level understanding. "
                    "Lab skills and experimental design. "
                    "Prepare for AP Biology or college coursework. "
                    "Critical thinking about current research."
                )
            }
        }
    },

    # ==========================================================================
    # LEXIS - English & Literature
    # ==========================================================================
    "lexis": {
        "supported_grades": range(1, 13),  # Grades 1-12
        "grade_bands": {
            "G1-2": {
                "topics": [
                    "Phonics and decoding",
                    "Sight words and simple sentences",
                    "Story comprehension (who, what, where)",
                    "Basic punctuation (periods, question marks)",
                    "Simple creative writing (sentences, short stories)"
                ],
                "difficulty": "foundational",
                "didactic_notes": (
                    "Focus on building confidence with reading and writing. "
                    "Simple, supportive language. "
                    "Lots of praise and encouragement. "
                    "Keep activities short and engaging."
                )
            },
            "G3-4": {
                "topics": [
                    "Reading fluency and comprehension",
                    "Vocabulary development",
                    "Paragraph structure (topic sentence, details)",
                    "Grammar basics (nouns, verbs, adjectives)",
                    "Narrative and informational writing"
                ],
                "difficulty": "elementary",
                "didactic_notes": (
                    "Build reading stamina and writing skills. "
                    "Encourage self-expression and creativity. "
                    "Introduce literary elements (characters, setting, plot). "
                    "Scaffolded writing practice."
                )
            },
            "G5-8": {
                "topics": [
                    "Literary analysis (theme, character development, figurative language)",
                    "Essay writing (5-paragraph structure)",
                    "Grammar and mechanics (more advanced)",
                    "Research skills and citing sources",
                    "Persuasive and expository writing"
                ],
                "difficulty": "intermediate",
                "didactic_notes": (
                    "Develop analytical reading skills. "
                    "Formal writing instruction and revision. "
                    "Introduce classic and contemporary literature. "
                    "Peer review and editing."
                )
            },
            "G9-12": {
                "topics": [
                    "Advanced literary analysis (symbolism, tone, style)",
                    "Rhetoric and argumentation",
                    "Research papers and MLA/APA citation",
                    "Creative writing (poetry, fiction, memoir)",
                    "British, American, and world literature"
                ],
                "difficulty": "advanced",
                "didactic_notes": (
                    "College-preparatory reading and writing. "
                    "Critical thinking and interpretation. "
                    "Prepare for AP Literature, AP Language, or college essays. "
                    "Develop personal voice and style."
                )
            }
        }
    },

    # ==========================================================================
    # NEO - AI & Technology
    # ==========================================================================
    "neo": {
        "supported_grades": range(5, 13),  # Grades 5-12 (coding concepts start in upper elementary)
        "grade_bands": {
            "G5-8": {
                "topics": [
                    "Block-based coding (Scratch, Blockly)",
                    "Computational thinking (algorithms, patterns, debugging)",
                    "Introduction to Python (variables, loops, conditionals)",
                    "What is AI? (simple explanations)",
                    "Digital citizenship and online safety"
                ],
                "difficulty": "introductory",
                "didactic_notes": (
                    "Visual and hands-on coding activities. "
                    "Focus on problem-solving and creativity. "
                    "Introduce AI concepts through examples (Siri, recommendations). "
                    "Ethics and responsible technology use."
                )
            },
            "G9-12": {
                "topics": [
                    "Python programming (OOP, data structures, algorithms)",
                    "Machine learning basics (supervised, unsupervised learning)",
                    "Neural networks and deep learning (conceptual)",
                    "AI ethics (bias, privacy, fairness)",
                    "Projects (chatbots, image recognition, game AI)"
                ],
                "difficulty": "advanced",
                "didactic_notes": (
                    "Project-based learning with real applications. "
                    "Introduce mathematical foundations (linear algebra, statistics). "
                    "Discuss ethical implications and societal impact. "
                    "Prepare for AP Computer Science or college CS."
                )
            }
        }
    },

    # ==========================================================================
    # LUNA - Arts & Music
    # ==========================================================================
    "luna": {
        "supported_grades": range(1, 13),  # Grades 1-12
        "grade_bands": {
            "G1-2": {
                "topics": [
                    "Exploring colors, shapes, and lines",
                    "Simple music concepts (rhythm, high/low sounds)",
                    "Creative expression through drawing and painting",
                    "Singing and simple instruments (percussion)",
                    "Storytelling through art"
                ],
                "difficulty": "foundational",
                "didactic_notes": (
                    "Focus on exploration and fun. "
                    "No pressure for perfection—encourage experimentation. "
                    "Simple instructions, lots of positive feedback. "
                    "Hands-on activities and play."
                )
            },
            "G3-4": {
                "topics": [
                    "Basic art techniques (watercolor, collage, sculpture)",
                    "Music notation basics (reading simple rhythms and notes)",
                    "Melody and harmony (simple)",
                    "Art history (introduction to famous artists)",
                    "Creative projects and self-expression"
                ],
                "difficulty": "elementary",
                "didactic_notes": (
                    "Introduce more structured techniques while maintaining creativity. "
                    "Build confidence through skill-building. "
                    "Exposure to different art styles and cultures. "
                    "Encourage personal interpretation."
                )
            },
            "G5-8": {
                "topics": [
                    "Advanced techniques (perspective, shading, mixed media)",
                    "Music theory (scales, chords, key signatures)",
                    "Instrument proficiency (if applicable)",
                    "Art movements and cultural context",
                    "Digital art and music creation tools"
                ],
                "difficulty": "intermediate",
                "didactic_notes": (
                    "Develop technical skills and artistic voice. "
                    "Critique and analysis of artwork. "
                    "Experiment with digital tools. "
                    "Connect art to history and social themes."
                )
            },
            "G9-12": {
                "topics": [
                    "Portfolio development (for college applications)",
                    "Advanced composition and music production",
                    "Art history and criticism",
                    "Specialized techniques (oil painting, digital animation, etc.)",
                    "Performance and exhibition"
                ],
                "difficulty": "advanced",
                "didactic_notes": (
                    "Professional-level skill development. "
                    "Prepare for art school or conservatory. "
                    "Encourage unique style and creative risk-taking. "
                    "Portfolio review and feedback."
                )
            }
        }
    },

    # ==========================================================================
    # ATLAS - History & Geography
    # ==========================================================================
    "atlas": {
        "supported_grades": range(3, 13),  # Grades 3-12
        "grade_bands": {
            "G3-4": {
                "topics": [
                    "Community and local history",
                    "Basic geography (maps, continents, oceans)",
                    "Important historical figures (age-appropriate)",
                    "Holidays and cultural traditions",
                    "Timelines and chronology (simple)"
                ],
                "difficulty": "foundational",
                "didactic_notes": (
                    "Use stories and narratives to engage students. "
                    "Connect to students' own lives and communities. "
                    "Simple maps and visual timelines. "
                    "Celebrate diversity and different perspectives."
                )
            },
            "G5-8": {
                "topics": [
                    "US History (colonization, Revolution, Civil War, etc.)",
                    "World geography (countries, capitals, physical features)",
                    "Ancient civilizations (Egypt, Greece, Rome)",
                    "Geography and culture connections",
                    "Historical cause and effect"
                ],
                "difficulty": "intermediate",
                "didactic_notes": (
                    "Develop historical thinking skills (cause/effect, change over time). "
                    "Map skills and spatial reasoning. "
                    "Compare different cultures and perspectives. "
                    "Primary source analysis (introductory)."
                )
            },
            "G9-12": {
                "topics": [
                    "World History (medieval to modern)",
                    "US History (Reconstruction to present)",
                    "Government and civics",
                    "Economics and globalization",
                    "Historiography and historical debates"
                ],
                "difficulty": "advanced",
                "didactic_notes": (
                    "Critical analysis of sources and evidence. "
                    "Understand multiple perspectives and interpretations. "
                    "Prepare for AP History exams (US, World, European). "
                    "Connect historical events to current issues."
                )
            }
        }
    }
}


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def get_mentor_grade_profile(mentor_id: str) -> Optional[Dict]:
    """
    Get the complete grade profile for a mentor.

    Args:
        mentor_id: Mentor identifier

    Returns:
        Grade profile dictionary or None if not found
    """
    return GRADE_BAND_PROFILES.get(mentor_id)


def get_topics_for_grade_band(mentor_id: str, grade_band: str) -> Optional[List[str]]:
    """
    Get the topic list for a specific mentor and grade band.

    Args:
        mentor_id: Mentor identifier
        grade_band: Grade band (e.g., "G1-2", "G5-8")

    Returns:
        List of topics or None if not found
    """
    profile = get_mentor_grade_profile(mentor_id)
    if not profile:
        return None

    band_info = profile.get("grade_bands", {}).get(grade_band)
    if not band_info:
        return None

    return band_info.get("topics", [])


def get_grade_band_for_grade(grade: int) -> str:
    """
    Map a single grade to its grade band.

    Args:
        grade: Grade level (1-12)

    Returns:
        Grade band string (e.g., "G1-2")
    """
    if grade in [1, 2]:
        return "G1-2"
    elif grade in [3, 4]:
        return "G3-4"
    elif grade in [5, 6, 7, 8]:
        return "G5-8"
    elif grade in [9, 10, 11, 12]:
        return "G9-12"
    else:
        raise ValueError(f"Grade must be between 1 and 12, got {grade}")


def get_recommended_mentors_for_grade(grade: int, subject: Optional[str] = None) -> List[str]:
    """
    Get a list of recommended mentor IDs for a given grade (and optionally subject).

    Prioritizes mentors who are well-suited for younger learners in early grades.

    Args:
        grade: Grade level (1-12)
        subject: Optional subject filter

    Returns:
        List of mentor IDs, ordered by recommendation strength
    """
    recommended = []

    # Early elementary (G1-2): prioritize Luna, Lexis, Stella
    if grade in [1, 2]:
        if not subject or "art" in subject.lower() or "music" in subject.lower():
            recommended.append("luna")
        if not subject or "english" in subject.lower() or "reading" in subject.lower() or "writing" in subject.lower():
            recommended.append("lexis")
        if not subject or "math" in subject.lower():
            recommended.append("stella")

    # Upper elementary (G3-4): add Darwin, Atlas
    elif grade in [3, 4]:
        if not subject or "english" in subject.lower() or "reading" in subject.lower():
            recommended.append("lexis")
        if not subject or "math" in subject.lower():
            recommended.append("stella")
        if not subject or "art" in subject.lower() or "music" in subject.lower():
            recommended.append("luna")
        if not subject or "biology" in subject.lower() or "science" in subject.lower():
            recommended.append("darwin")
        if not subject or "history" in subject.lower() or "geography" in subject.lower() or "social" in subject.lower():
            recommended.append("atlas")

    # Middle school (G5-8): all mentors available
    elif grade in [5, 6, 7, 8]:
        if not subject or "math" in subject.lower():
            recommended.append("stella")
        if not subject or "physics" in subject.lower() or "science" in subject.lower():
            recommended.append("max")
        if not subject or "chemistry" in subject.lower() or "science" in subject.lower():
            recommended.append("nova")
        if not subject or "biology" in subject.lower() or "science" in subject.lower():
            recommended.append("darwin")
        if not subject or "english" in subject.lower() or "reading" in subject.lower():
            recommended.append("lexis")
        if not subject or "tech" in subject.lower() or "coding" in subject.lower() or "ai" in subject.lower():
            recommended.append("neo")
        if not subject or "art" in subject.lower() or "music" in subject.lower():
            recommended.append("luna")
        if not subject or "history" in subject.lower() or "geography" in subject.lower():
            recommended.append("atlas")

    # High school (G9-12): all mentors, prioritize STEM for advanced topics
    elif grade in [9, 10, 11, 12]:
        if not subject or "math" in subject.lower():
            recommended.append("stella")
        if not subject or "physics" in subject.lower():
            recommended.append("max")
        if not subject or "chemistry" in subject.lower():
            recommended.append("nova")
        if not subject or "biology" in subject.lower():
            recommended.append("darwin")
        if not subject or "english" in subject.lower() or "literature" in subject.lower():
            recommended.append("lexis")
        if not subject or "tech" in subject.lower() or "coding" in subject.lower() or "ai" in subject.lower() or "computer" in subject.lower():
            recommended.append("neo")
        if not subject or "art" in subject.lower() or "music" in subject.lower():
            recommended.append("luna")
        if not subject or "history" in subject.lower() or "geography" in subject.lower() or "government" in subject.lower():
            recommended.append("atlas")

    return recommended

"""
Stellar AI Demo Data Seeding Script

Creates a complete, realistic demo dataset for investor presentations and testing:
- School: Dubai Future Academy
- 4 demo users (admin, teacher, student, parent)
- Skills, Learning Paths, Modules, Tasks
- Student progress, verifications, credentials
- Curriculum resources with skill mappings
"""

import asyncio
import uuid
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import AsyncSessionLocal
from app.models import (
    User, School, Teacher, Student, Parent,
    Classroom, Subject, Skill, SkillScore,
    LearningPath, LearningModule, StudentLearningPath, StudentModule,
    Task, StudentTaskProgress, Verification, Credential, OnChainCredential,
    LearningResource, Badge, StudentBadge, XPEvent,
    SkillCategory, PathStatus, ModuleStatus, VerificationSource, VerificationStatus,
    CredentialType, CredentialStatus, ResourceType, SourceType
)
from app.auth import get_password_hash


# Demo credentials
DEMO_CREDENTIALS = {
    "admin": {"email": "admin@stellar-demo.school", "password": "StellarDemo123!"},
    "teacher": {"email": "teacher.sara@stellar-demo.school", "password": "StellarDemo123!"},
    "student": {"email": "amira.student@stellar-demo.school", "password": "StellarDemo123!"},
    "parent": {"email": "parent.hassan@stellar-demo.school", "password": "StellarDemo123!"},
}


async def clear_demo_data(db: AsyncSession):
    """Clear existing demo data (optional - use with caution)"""
    print("⚠️  Clearing existing demo data...")
    # This would require cascading deletes - for now we'll just create fresh data
    # In production, you'd implement proper cleanup logic
    pass


async def seed_school_and_structure(db: AsyncSession):
    """Create school, classes, and subjects"""
    print("\n📚 Creating school structure...")

    # Create school
    school = School(
        id=uuid.uuid4(),
        name="Dubai Future Academy",
        address="Dubai Knowledge Park, Dubai, UAE",
        created_at=datetime.utcnow(),
    )
    db.add(school)
    await db.flush()

    # Create subjects
    english_subject = Subject(
        id=uuid.uuid4(),
        name="English A1",
        description="Foundational English language skills for young learners",
        created_at=datetime.utcnow(),
    )

    math_subject = Subject(
        id=uuid.uuid4(),
        name="Math Basics",
        description="Elementary mathematics for Grade 3",
        created_at=datetime.utcnow(),
    )

    db.add_all([english_subject, math_subject])
    await db.flush()

    # Create classroom
    classroom = Classroom(
        id=uuid.uuid4(),
        name="Grade 3A – English Focus",
        school_id=school.id,
        created_at=datetime.utcnow(),
    )
    db.add(classroom)
    await db.flush()

    print(f"  ✓ School: {school.name}")
    print(f"  ✓ Classroom: {classroom.name}")
    print(f"  ✓ Subjects: {english_subject.name}, {math_subject.name}")

    return school, classroom, english_subject, math_subject


async def seed_users(db: AsyncSession, school, classroom):
    """Create demo users for all roles"""
    print("\n👥 Creating demo users...")

    # School Admin
    admin_user = User(
        id=uuid.uuid4(),
        email=DEMO_CREDENTIALS["admin"]["email"],
        hashed_password=get_password_hash(DEMO_CREDENTIALS["admin"]["password"]),
        full_name="Dr. Ahmed Al-Mansouri",
        role="school_admin",
        is_active=True,
        created_at=datetime.utcnow(),
    )
    db.add(admin_user)

    # Teacher
    teacher_user = User(
        id=uuid.uuid4(),
        email=DEMO_CREDENTIALS["teacher"]["email"],
        hashed_password=get_password_hash(DEMO_CREDENTIALS["teacher"]["password"]),
        full_name="Sara Thompson",
        role="teacher",
        is_active=True,
        created_at=datetime.utcnow(),
    )
    db.add(teacher_user)
    await db.flush()

    teacher = Teacher(
        user_id=teacher_user.id,
        school_id=school.id,
    )
    db.add(teacher)

    # Student
    student_user = User(
        id=uuid.uuid4(),
        email=DEMO_CREDENTIALS["student"]["email"],
        hashed_password=get_password_hash(DEMO_CREDENTIALS["student"]["password"]),
        full_name="Amira Hassan",
        role="student",
        is_active=True,
        created_at=datetime.utcnow(),
    )
    db.add(student_user)
    await db.flush()

    student = Student(
        user_id=student_user.id,
        school_id=school.id,
        grade_level=3,
    )
    db.add(student)

    # Parent
    parent_user = User(
        id=uuid.uuid4(),
        email=DEMO_CREDENTIALS["parent"]["email"],
        hashed_password=get_password_hash(DEMO_CREDENTIALS["parent"]["password"]),
        full_name="Hassan Al-Sharif",
        role="parent",
        is_active=True,
        created_at=datetime.utcnow(),
    )
    db.add(parent_user)
    await db.flush()

    parent = Parent(
        user_id=parent_user.id,
    )
    db.add(parent)
    await db.flush()

    print(f"  ✓ Admin: {admin_user.email}")
    print(f"  ✓ Teacher: {teacher_user.email}")
    print(f"  ✓ Student: {student_user.email}")
    print(f"  ✓ Parent: {parent_user.email}")

    return admin_user, teacher_user, student_user, student, parent_user, parent


async def seed_skills(db: AsyncSession):
    """Create foundational skills"""
    print("\n🎯 Creating skills...")

    skills_data = [
        {
            "name": "Reading A1 – Simple Sentences",
            "description": "Ability to read and understand simple sentences with common words",
            "category": SkillCategory.LANGUAGE,
            "level": "A1 - Beginner",
            "age_group_min": 6,
            "age_group_max": 9,
        },
        {
            "name": "Reading A1 – Main Idea",
            "description": "Identify the main idea in short texts and stories",
            "category": SkillCategory.LANGUAGE,
            "level": "A1 - Beginner",
            "age_group_min": 7,
            "age_group_max": 10,
        },
        {
            "name": "Math – Add to 20",
            "description": "Addition of numbers up to 20 with understanding",
            "category": SkillCategory.MATH,
            "level": "Grade 3",
            "age_group_min": 7,
            "age_group_max": 9,
        },
        {
            "name": "Math – Word Problems (Beginner)",
            "description": "Solve simple word problems involving addition and subtraction",
            "category": SkillCategory.MATH,
            "level": "Grade 3",
            "age_group_min": 7,
            "age_group_max": 10,
        },
        {
            "name": "Critical Thinking – Pattern Recognition",
            "description": "Identify and extend simple patterns",
            "category": SkillCategory.CRITICAL_THINKING,
            "level": "Elementary",
            "age_group_min": 6,
            "age_group_max": 10,
        },
    ]

    skills = []
    for skill_data in skills_data:
        skill = Skill(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            **skill_data
        )
        db.add(skill)
        skills.append(skill)
        print(f"  ✓ {skill.name}")

    await db.flush()
    return skills


async def seed_learning_paths_and_modules(db: AsyncSession, skills):
    """Create learning paths with modules"""
    print("\n🛤️  Creating learning paths and modules...")

    # English A1 Path
    english_path = LearningPath(
        id=uuid.uuid4(),
        name="English A1 – Starter Path",
        description="Foundation English skills for young learners - reading, comprehension, and basic writing",
        recommended_age_min=6,
        recommended_age_max=9,
        estimated_hours=20,
        difficulty="beginner",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(english_path)
    await db.flush()

    # English modules
    english_module_1 = LearningModule(
        id=uuid.uuid4(),
        learning_path_id=english_path.id,
        name="Simple Sentences",
        description="Learn to read simple sentences and common words",
        order=1,
        skill_ids=[str(skills[0].id)],  # Simple Sentences skill
        completion_threshold=70,
        estimated_minutes=300,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    english_module_2 = LearningModule(
        id=uuid.uuid4(),
        learning_path_id=english_path.id,
        name="Short Stories",
        description="Read short stories and identify the main idea",
        order=2,
        skill_ids=[str(skills[1].id)],  # Main Idea skill
        completion_threshold=70,
        estimated_minutes=400,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.add_all([english_module_1, english_module_2])

    # Math Path
    math_path = LearningPath(
        id=uuid.uuid4(),
        name="Math Basics – Grade 3",
        description="Elementary mathematics - addition, subtraction, and problem solving",
        recommended_age_min=7,
        recommended_age_max=9,
        estimated_hours=25,
        difficulty="beginner",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(math_path)
    await db.flush()

    # Math module
    math_module_1 = LearningModule(
        id=uuid.uuid4(),
        learning_path_id=math_path.id,
        name="Addition to 20",
        description="Master addition of numbers up to 20",
        order=1,
        skill_ids=[str(skills[2].id)],  # Add to 20
        completion_threshold=75,
        estimated_minutes=350,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    math_module_2 = LearningModule(
        id=uuid.uuid4(),
        learning_path_id=math_path.id,
        name="Word Problems",
        description="Apply math skills to real-world problems",
        order=2,
        skill_ids=[str(skills[3].id)],  # Word Problems
        completion_threshold=70,
        estimated_minutes=300,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.add_all([math_module_1, math_module_2])
    await db.flush()

    print(f"  ✓ Path: {english_path.name} (2 modules)")
    print(f"  ✓ Path: {math_path.name} (2 modules)")

    return (
        english_path, [english_module_1, english_module_2],
        math_path, [math_module_1, math_module_2]
    )


async def seed_tasks(db: AsyncSession, modules):
    """Create tasks for modules"""
    print("\n📝 Creating tasks...")

    tasks_created = []

    # Tasks for English Module 1 (Simple Sentences)
    task1 = Task(
        id=uuid.uuid4(),
        title="Read 5 Simple Sentences",
        description="Practice reading simple sentences about animals and colors",
        difficulty="easy",
        estimated_minutes=10,
        xp_reward=20,
        created_at=datetime.utcnow(),
    )

    task2 = Task(
        id=uuid.uuid4(),
        title="Match Words to Pictures",
        description="Match simple words to their pictures",
        difficulty="easy",
        estimated_minutes=8,
        xp_reward=15,
        created_at=datetime.utcnow(),
    )

    # Tasks for English Module 2 (Short Stories)
    task3 = Task(
        id=uuid.uuid4(),
        title="Read 'The Lost Kitten'",
        description="Read a short story and answer questions about the main idea",
        difficulty="medium",
        estimated_minutes=15,
        xp_reward=30,
        created_at=datetime.utcnow(),
    )

    # Tasks for Math Module 1 (Addition)
    task4 = Task(
        id=uuid.uuid4(),
        title="Addition Practice (1-10)",
        description="Solve 10 addition problems with numbers 1-10",
        difficulty="easy",
        estimated_minutes=12,
        xp_reward=25,
        created_at=datetime.utcnow(),
    )

    task5 = Task(
        id=uuid.uuid4(),
        title="Addition Practice (11-20)",
        description="Solve 10 addition problems with numbers up to 20",
        difficulty="medium",
        estimated_minutes=15,
        xp_reward=30,
        created_at=datetime.utcnow(),
    )

    db.add_all([task1, task2, task3, task4, task5])
    await db.flush()

    # Update modules with task IDs
    modules[0].task_ids = [str(task1.id), str(task2.id)]
    modules[1].task_ids = [str(task3.id)]
    modules[2].task_ids = [str(task4.id), str(task5.id)]

    print(f"  ✓ Created 5 tasks across modules")

    return [task1, task2, task3, task4, task5]


async def seed_student_progress(db: AsyncSession, student, paths, modules, tasks, skills):
    """Create student progress data"""
    print("\n📊 Creating student progress...")

    english_path, english_modules, math_path, math_modules = paths

    # Assign student to both learning paths
    student_english_path = StudentLearningPath(
        id=uuid.uuid4(),
        student_id=student.user_id,
        learning_path_id=english_path.id,
        status=PathStatus.IN_PROGRESS,
        progress_percentage=35,
        started_at=datetime.utcnow() - timedelta(days=14),
        created_at=datetime.utcnow() - timedelta(days=14),
        updated_at=datetime.utcnow(),
    )

    student_math_path = StudentLearningPath(
        id=uuid.uuid4(),
        student_id=student.user_id,
        learning_path_id=math_path.id,
        status=PathStatus.IN_PROGRESS,
        progress_percentage=20,
        started_at=datetime.utcnow() - timedelta(days=7),
        created_at=datetime.utcnow() - timedelta(days=7),
        updated_at=datetime.utcnow(),
    )

    db.add_all([student_english_path, student_math_path])

    # Module progress
    student_module_1 = StudentModule(
        id=uuid.uuid4(),
        student_id=student.user_id,
        module_id=english_modules[0].id,
        status=ModuleStatus.COMPLETED,
        score=78.0,
        tasks_completed=2,
        tasks_total=2,
        started_at=datetime.utcnow() - timedelta(days=14),
        completed_at=datetime.utcnow() - timedelta(days=10),
        created_at=datetime.utcnow() - timedelta(days=14),
        updated_at=datetime.utcnow() - timedelta(days=10),
    )

    student_module_2 = StudentModule(
        id=uuid.uuid4(),
        student_id=student.user_id,
        module_id=english_modules[1].id,
        status=ModuleStatus.IN_PROGRESS,
        score=45.0,
        tasks_completed=0,
        tasks_total=1,
        started_at=datetime.utcnow() - timedelta(days=3),
        created_at=datetime.utcnow() - timedelta(days=3),
        updated_at=datetime.utcnow(),
    )

    db.add_all([student_module_1, student_module_2])

    # Skill scores
    skill_scores = [
        SkillScore(
            id=uuid.uuid4(),
            student_id=student.user_id,
            skill_id=skills[0].id,  # Simple Sentences
            score=72.0,
            confidence=0.85,
            assessment_count=3,
            last_practiced_at=datetime.utcnow() - timedelta(days=2),
            created_at=datetime.utcnow() - timedelta(days=14),
            updated_at=datetime.utcnow() - timedelta(days=2),
        ),
        SkillScore(
            id=uuid.uuid4(),
            student_id=student.user_id,
            skill_id=skills[1].id,  # Main Idea (WEAK)
            score=45.0,
            confidence=0.60,
            assessment_count=1,
            last_practiced_at=datetime.utcnow() - timedelta(days=3),
            created_at=datetime.utcnow() - timedelta(days=3),
            updated_at=datetime.utcnow() - timedelta(days=3),
        ),
        SkillScore(
            id=uuid.uuid4(),
            student_id=student.user_id,
            skill_id=skills[2].id,  # Add to 20
            score=68.0,
            confidence=0.75,
            assessment_count=2,
            last_practiced_at=datetime.utcnow() - timedelta(days=5),
            created_at=datetime.utcnow() - timedelta(days=7),
            updated_at=datetime.utcnow() - timedelta(days=5),
        ),
    ]

    db.add_all(skill_scores)

    # XP events
    xp_events = [
        XPEvent(
            id=uuid.uuid4(),
            student_id=student.user_id,
            amount=20,
            reason="Completed task: Read 5 Simple Sentences",
            task_id=tasks[0].id,
            created_at=datetime.utcnow() - timedelta(days=12),
        ),
        XPEvent(
            id=uuid.uuid4(),
            student_id=student.user_id,
            amount=15,
            reason="Completed task: Match Words to Pictures",
            task_id=tasks[1].id,
            created_at=datetime.utcnow() - timedelta(days=10),
        ),
        XPEvent(
            id=uuid.uuid4(),
            student_id=student.user_id,
            amount=50,
            reason="Completed module: Simple Sentences",
            created_at=datetime.utcnow() - timedelta(days=10),
        ),
    ]

    db.add_all(xp_events)

    print(f"  ✓ Assigned 2 learning paths")
    print(f"  ✓ Created module progress (1 completed, 1 in progress)")
    print(f"  ✓ Created 3 skill scores (1 weak: Main Idea at 45)")
    print(f"  ✓ Created 3 XP events (total: 85 XP)")

    await db.flush()
    return skill_scores


async def seed_verifications_and_credentials(db: AsyncSession, student, skills, modules):
    """Create verifications and credentials"""
    print("\n✅ Creating verifications and credentials...")

    # Verification for Simple Sentences skill
    verification = Verification(
        id=uuid.uuid4(),
        student_id=student.user_id,
        skill_id=skills[0].id,  # Simple Sentences
        module_id=modules[0].id,
        source=VerificationSource.AI_ASSESSMENT,
        status=VerificationStatus.VERIFIED,
        score=78.0,
        evidence={"tasks_completed": 2, "average_score": 78, "consistency": "high"},
        verified_at=datetime.utcnow() - timedelta(days=10),
        created_at=datetime.utcnow() - timedelta(days=10),
        updated_at=datetime.utcnow() - timedelta(days=10),
    )
    db.add(verification)
    await db.flush()

    # Credential for completing Simple Sentences module
    credential = Credential(
        id=uuid.uuid4(),
        student_id=student.user_id,
        credential_type=CredentialType.MODULE_COMPLETION,
        status=CredentialStatus.ISSUED,
        title="English A1 – Simple Sentences (Bronze)",
        description="Successfully completed the Simple Sentences module with a score of 78%",
        module_id=modules[0].id,
        verification_ids=[str(verification.id)],
        credential_metadata={
            "level": "Bronze",
            "score": 78,
            "skills_verified": ["Reading A1 – Simple Sentences"],
            "completion_date": (datetime.utcnow() - timedelta(days=10)).isoformat(),
        },
        issuer_name="Dubai Future Academy",
        issued_at=datetime.utcnow() - timedelta(days=9),
        created_at=datetime.utcnow() - timedelta(days=9),
        updated_at=datetime.utcnow() - timedelta(days=9),
    )
    db.add(credential)
    await db.flush()

    # Simulated on-chain credential
    on_chain_credential = OnChainCredential(
        id=uuid.uuid4(),
        credential_id=credential.id,
        network="Stellar Testnet",
        transaction_hash=f"0x{uuid.uuid4().hex}",
        contract_address="0xStellarAICredentialContract",
        token_id=str(uuid.uuid4()),
        owner_wallet_address=f"0x{uuid.uuid4().hex[:40]}",
        metadata_uri=f"ipfs://QmDemo{uuid.uuid4().hex[:20]}",
        is_simulated=True,
        minting_successful=True,
        minted_at=datetime.utcnow() - timedelta(days=9),
        created_at=datetime.utcnow() - timedelta(days=9),
        updated_at=datetime.utcnow() - timedelta(days=9),
    )
    db.add(on_chain_credential)

    print(f"  ✓ Created 1 verification (AI-verified)")
    print(f"  ✓ Created 1 credential: {credential.title}")
    print(f"  ✓ Created 1 on-chain credential (simulated)")

    await db.flush()
    return verification, credential


async def seed_curriculum_resources(db: AsyncSession, skills, school):
    """Create curriculum resources"""
    print("\n📚 Creating curriculum resources...")

    resources_data = [
        {
            "title": "Finding the Main Idea - Animated Story",
            "description": "Learn to identify the main idea through fun animated stories about animals and adventures",
            "resource_type": ResourceType.VIDEO,
            "url": "https://demo.stellar-ai.school/videos/main-idea-intro",
            "language": "en",
            "subject": "reading",
            "grade_min": 2,
            "grade_max": 4,
            "age_min": 7,
            "age_max": 10,
            "estimated_minutes": 8,
            "source_type": SourceType.PUBLIC_OPEN_CONTENT,
            "source_attribution": "Open Educational Resources - ReadingRocks",
            "license_type": "CC BY-SA 4.0",
            "school_id": school.id,
            "difficulty_level": "beginner",
            "quality_score": 85,
            "resource_metadata": {
                "keywords": ["main idea", "reading comprehension", "stories"],
                "interactive": False,
                "suitable_for_self_study": True,
            },
            "skills": [skills[1]],  # Main Idea
        },
        {
            "title": "Simple Sentences Practice Worksheet",
            "description": "Printable worksheet with 20 simple sentences to read and understand",
            "resource_type": ResourceType.WORKSHEET,
            "file_path": "/demo-content/worksheets/simple-sentences.pdf",
            "language": "en",
            "subject": "reading",
            "grade_min": 1,
            "grade_max": 3,
            "age_min": 6,
            "age_max": 9,
            "estimated_minutes": 15,
            "source_type": SourceType.TEACHER_UPLOADED,
            "source_attribution": "Created by Sara Thompson, Dubai Future Academy",
            "license_type": "All Rights Reserved",
            "school_id": school.id,
            "difficulty_level": "beginner",
            "quality_score": 90,
            "resource_metadata": {
                "keywords": ["simple sentences", "reading practice", "worksheet"],
                "printable": True,
            },
            "skills": [skills[0]],  # Simple Sentences
        },
        {
            "title": "Add to 20 – Number Line Game",
            "description": "Interactive game where students use a number line to solve addition problems",
            "resource_type": ResourceType.GAME,
            "url": "https://demo.stellar-ai.school/games/number-line-add",
            "language": "en",
            "subject": "math",
            "grade_min": 2,
            "grade_max": 4,
            "age_min": 7,
            "age_max": 9,
            "estimated_minutes": 12,
            "source_type": SourceType.PUBLIC_OPEN_CONTENT,
            "source_attribution": "Math Playground - Open Games",
            "license_type": "CC BY 4.0",
            "school_id": school.id,
            "difficulty_level": "beginner",
            "quality_score": 88,
            "resource_metadata": {
                "keywords": ["addition", "number line", "interactive", "game"],
                "interactive": True,
                "requires_login": False,
            },
            "skills": [skills[2]],  # Add to 20
        },
        {
            "title": "Word Problems for Beginners",
            "description": "Collection of simple word problems about everyday situations",
            "resource_type": ResourceType.INTERACTIVE_EXERCISE,
            "url": "https://demo.stellar-ai.school/exercises/word-problems-1",
            "language": "en",
            "subject": "math",
            "grade_min": 3,
            "grade_max": 4,
            "age_min": 8,
            "age_max": 10,
            "estimated_minutes": 20,
            "source_type": SourceType.STELLAR_AI_GENERATED,
            "source_attribution": "Stellar AI Content Generator",
            "license_type": "Proprietary",
            "school_id": school.id,
            "difficulty_level": "intermediate",
            "quality_score": 82,
            "resource_metadata": {
                "keywords": ["word problems", "real-world math", "problem solving"],
                "interactive": True,
                "adaptive_difficulty": True,
            },
            "skills": [skills[3]],  # Word Problems
        },
    ]

    resources = []
    for resource_data in resources_data:
        skill_list = resource_data.pop("skills")

        resource = LearningResource(
            id=uuid.uuid4(),
            is_active=True,
            is_public=False,
            view_count=0,
            completion_count=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            **resource_data
        )

        # Add skills relationship
        resource.skills = skill_list

        db.add(resource)
        resources.append(resource)
        print(f"  ✓ {resource.title}")

    await db.flush()
    print(f"  ✓ Created {len(resources)} curriculum resources")

    return resources


async def seed_badges(db: AsyncSession, student):
    """Create badges and award to student"""
    print("\n🏅 Creating badges...")

    # Reading badge
    reading_badge = Badge(
        id=uuid.uuid4(),
        name="Reading Rookie",
        description="Completed first reading module",
        icon_url="/badges/reading-rookie.png",
        created_at=datetime.utcnow(),
    )
    db.add(reading_badge)
    await db.flush()

    # Award badge to student
    student_badge = StudentBadge(
        student_id=student.user_id,
        badge_id=reading_badge.id,
        earned_at=datetime.utcnow() - timedelta(days=9),
        created_at=datetime.utcnow() - timedelta(days=9),
    )
    db.add(student_badge)

    print(f"  ✓ Created badge: {reading_badge.name}")
    print(f"  ✓ Awarded to student")

    await db.flush()


async def main():
    """Main seeding function"""
    print("="*70)
    print("🌟 STELLAR AI - DEMO DATA SEEDING")
    print("="*70)

    async with AsyncSessionLocal() as db:
        try:
            # Create all demo data
            school, classroom, english_subject, math_subject = await seed_school_and_structure(db)

            admin, teacher_user, student_user, student, parent_user, parent = await seed_users(
                db, school, classroom
            )

            skills = await seed_skills(db)

            english_path, english_modules, math_path, math_modules = await seed_learning_paths_and_modules(
                db, skills
            )

            all_modules = english_modules + math_modules
            tasks = await seed_tasks(db, all_modules)

            await seed_student_progress(
                db, student,
                (english_path, english_modules, math_path, math_modules),
                all_modules, tasks, skills
            )

            await seed_verifications_and_credentials(db, student, skills, english_modules)

            await seed_curriculum_resources(db, skills, school)

            await seed_badges(db, student)

            # Commit all changes
            await db.commit()

            print("\n" + "="*70)
            print("✅ DEMO DATA SEEDING COMPLETE")
            print("="*70)

            print("\n📋 DEMO LOGIN CREDENTIALS:")
            print("-"*70)
            for role, creds in DEMO_CREDENTIALS.items():
                print(f"\n{role.upper()}:")
                print(f"  Email:    {creds['email']}")
                print(f"  Password: {creds['password']}")

            print("\n" + "="*70)
            print("🚀 Ready for demo!")
            print("="*70)

        except Exception as e:
            await db.rollback()
            print(f"\n❌ Error during seeding: {e}")
            import traceback
            traceback.print_exc()
            raise


if __name__ == "__main__":
    asyncio.run(main())

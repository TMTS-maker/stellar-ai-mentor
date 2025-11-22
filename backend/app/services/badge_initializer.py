"""
Badge Initializer

Creates default badge set for the Stellecta platform
"""

from sqlalchemy.orm import Session
from app.database.models.gamification import Badge
import json


DEFAULT_BADGES = [
    # First Steps Badges
    {
        "name": "First Steps",
        "description": "Sent your first message to an AI mentor",
        "category": "first_message",
        "rarity": "common",
        "icon_url": "🌟",
        "xp_required": None,
        "streak_required": None,
        "condition_json": json.dumps({"type": "first_message"}),
    },
    {
        "name": "Quick Learner",
        "description": "Reached Level 5",
        "category": "level_milestone",
        "rarity": "common",
        "icon_url": "⚡",
        "xp_required": 500,
        "streak_required": None,
        "condition_json": json.dumps({"level": 5}),
    },
    {
        "name": "Rising Star",
        "description": "Reached Level 10",
        "category": "level_milestone",
        "rarity": "rare",
        "icon_url": "⭐",
        "xp_required": 1000,
        "streak_required": None,
        "condition_json": json.dumps({"level": 10}),
    },
    {
        "name": "Scholar",
        "description": "Reached Level 25",
        "category": "level_milestone",
        "rarity": "epic",
        "icon_url": "🎓",
        "xp_required": 2500,
        "streak_required": None,
        "condition_json": json.dumps({"level": 25}),
    },
    {
        "name": "Master",
        "description": "Reached Level 50",
        "category": "level_milestone",
        "rarity": "legendary",
        "icon_url": "👑",
        "xp_required": 5000,
        "streak_required": None,
        "condition_json": json.dumps({"level": 50}),
    },
    # Streak Badges
    {
        "name": "Consistent",
        "description": "Maintained a 3-day learning streak",
        "category": "streak",
        "rarity": "common",
        "icon_url": "🔥",
        "xp_required": None,
        "streak_required": 3,
        "condition_json": None,
    },
    {
        "name": "Week Warrior",
        "description": "Maintained a 7-day learning streak",
        "category": "streak",
        "rarity": "rare",
        "icon_url": "💪",
        "xp_required": None,
        "streak_required": 7,
        "condition_json": None,
    },
    {
        "name": "Month Master",
        "description": "Maintained a 30-day learning streak",
        "category": "streak",
        "rarity": "epic",
        "icon_url": "🏆",
        "xp_required": None,
        "streak_required": 30,
        "condition_json": None,
    },
    {
        "name": "Unstoppable",
        "description": "Maintained a 100-day learning streak",
        "category": "streak",
        "rarity": "legendary",
        "icon_url": "💎",
        "xp_required": None,
        "streak_required": 100,
        "condition_json": None,
    },
    # XP Milestones
    {
        "name": "Novice",
        "description": "Earned 100 XP",
        "category": "xp",
        "rarity": "common",
        "icon_url": "🌱",
        "xp_required": 100,
        "streak_required": None,
        "condition_json": None,
    },
    {
        "name": "Apprentice",
        "description": "Earned 500 XP",
        "category": "xp",
        "rarity": "common",
        "icon_url": "📚",
        "xp_required": 500,
        "streak_required": None,
        "condition_json": None,
    },
    {
        "name": "Expert",
        "description": "Earned 1,000 XP",
        "category": "xp",
        "rarity": "rare",
        "icon_url": "🧠",
        "xp_required": 1000,
        "streak_required": None,
        "condition_json": None,
    },
    {
        "name": "Champion",
        "description": "Earned 5,000 XP",
        "category": "xp",
        "rarity": "epic",
        "icon_url": "🥇",
        "xp_required": 5000,
        "streak_required": None,
        "condition_json": None,
    },
    {
        "name": "Legend",
        "description": "Earned 10,000 XP",
        "category": "xp",
        "rarity": "legendary",
        "icon_url": "🌟",
        "xp_required": 10000,
        "streak_required": None,
        "condition_json": None,
    },
]


def initialize_badges(db: Session) -> int:
    """
    Initialize default badges in the database

    Args:
        db: Database session

    Returns:
        Number of badges created
    """
    created_count = 0

    for badge_data in DEFAULT_BADGES:
        # Check if badge already exists
        existing = db.query(Badge).filter(Badge.name == badge_data["name"]).first()

        if existing:
            continue

        # Create new badge
        badge = Badge(**badge_data)
        db.add(badge)
        created_count += 1

    db.commit()
    return created_count

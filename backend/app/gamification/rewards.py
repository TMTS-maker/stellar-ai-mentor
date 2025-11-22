"""
Gamification Reward System

Handles XP, achievements, streaks, and leveling.

Note: This is a stub implementation. Full gamification logic would include:
- Database integration for persistence
- Complex achievement tracking
- Leaderboards
- Reward algorithms
"""
from typing import Optional, Dict, Any
from datetime import datetime


class RewardSystem:
    """
    Gamification reward manager.

    Calculates XP, tracks achievements, and manages progression.
    """

    # XP values for different actions
    XP_VALUES = {
        "message_sent": 5,
        "problem_solved": 20,
        "concept_mastered": 50,
        "daily_streak": 10,
        "mentor_interaction": 10,
        "challenge_completed": 100
    }

    # Level thresholds (XP needed to reach each level)
    LEVEL_THRESHOLDS = [
        0, 100, 250, 500, 1000, 2000, 3500, 5500, 8000, 11000, 15000
    ]

    @staticmethod
    def calculate_xp(action: str, bonus_multiplier: float = 1.0) -> int:
        """
        Calculate XP for a specific action.

        Args:
            action: Action type
            bonus_multiplier: Multiplier for bonuses (e.g., streaks)

        Returns:
            XP earned
        """
        base_xp = RewardSystem.XP_VALUES.get(action, 0)
        return int(base_xp * bonus_multiplier)

    @staticmethod
    def get_level(total_xp: int) -> int:
        """
        Get the current level based on total XP.

        Args:
            total_xp: Total XP earned

        Returns:
            Current level (1-indexed)
        """
        level = 1
        for threshold in RewardSystem.LEVEL_THRESHOLDS:
            if total_xp >= threshold:
                level += 1
            else:
                break
        return min(level - 1, len(RewardSystem.LEVEL_THRESHOLDS))

    @staticmethod
    def xp_to_next_level(total_xp: int) -> int:
        """
        Calculate XP needed to reach the next level.

        Args:
            total_xp: Current total XP

        Returns:
            XP needed for next level
        """
        current_level = RewardSystem.get_level(total_xp)
        if current_level >= len(RewardSystem.LEVEL_THRESHOLDS):
            return 0  # Max level reached

        next_threshold = RewardSystem.LEVEL_THRESHOLDS[current_level]
        return next_threshold - total_xp

    @staticmethod
    def check_achievement(action: str, count: int) -> Optional[str]:
        """
        Check if an achievement is unlocked.

        Args:
            action: Action type
            count: Number of times action performed

        Returns:
            Achievement name if unlocked, None otherwise
        """
        # Stub implementation - would integrate with database
        achievements = {
            ("problem_solved", 1): "First Steps",
            ("problem_solved", 10): "Problem Solver",
            ("problem_solved", 50): "Math Ninja",
            ("daily_streak", 7): "Week Warrior",
            ("daily_streak", 30): "Monthly Master",
        }

        return achievements.get((action, count))

    @staticmethod
    def build_reward_message(xp_earned: int, achievement: Optional[str] = None) -> str:
        """
        Build a friendly reward message.

        Args:
            xp_earned: XP earned
            achievement: Achievement unlocked (if any)

        Returns:
            Reward message string
        """
        message = f"🌟 +{xp_earned} XP earned!"

        if achievement:
            message += f" 🏆 Achievement unlocked: {achievement}!"

        return message

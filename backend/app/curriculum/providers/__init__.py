"""
Curriculum Providers

All curriculum providers for different education systems
"""

from app.curriculum.providers.indian_cbse import IndianCBSEProvider
from app.curriculum.providers.uk_national import UKNationalProvider
from app.curriculum.providers.us_common_core import USCommonCoreProvider
from app.curriculum.base_provider import BaseCurriculumProvider

# Curriculum Provider Registry
CURRICULUM_PROVIDERS = {
    "INDIAN_CBSE": IndianCBSEProvider,
    "UK_NATIONAL": lambda: UKNationalProvider(variant="NATIONAL"),
    "UK_IGCSE": lambda: UKNationalProvider(variant="IGCSE"),
    "US_COMMON_CORE": USCommonCoreProvider,
}


def get_curriculum_provider(curriculum_type: str) -> BaseCurriculumProvider:
    """
    Get curriculum provider instance by type

    Args:
        curriculum_type: Type of curriculum (INDIAN_CBSE, UK_NATIONAL, etc.)

    Returns:
        Curriculum provider instance

    Raises:
        KeyError: If curriculum type not found
    """
    if curriculum_type not in CURRICULUM_PROVIDERS:
        raise KeyError(f"Unknown curriculum type: {curriculum_type}")

    provider_class = CURRICULUM_PROVIDERS[curriculum_type]
    return provider_class()


def list_available_curricula() -> list:
    """
    List all available curriculum types

    Returns:
        List of curriculum type identifiers
    """
    return list(CURRICULUM_PROVIDERS.keys())


__all__ = [
    "IndianCBSEProvider",
    "UKNationalProvider",
    "USCommonCoreProvider",
    "get_curriculum_provider",
    "list_available_curricula",
    "CURRICULUM_PROVIDERS",
]

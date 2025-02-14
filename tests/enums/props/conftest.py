from typing import List
import pytest


@pytest.fixture(scope="function", name="property_variant_generator")
def property_variant_generator():
    """Fixture providing a function to generate property name variants."""

    def _generate_variants(aliases: List[str] = None) -> List[str]:
        variants = []
        for alias in aliases:
            variants.extend([alias.lower(), alias.title(), alias.swapcase()])
        return variants

    return _generate_variants


@pytest.fixture(scope="function", name="property_variant_test_params")
def property_variant_test_params(property_test_cases):
    """Fixture that generates the test parameters for parametrize test."""
    return [
        (prop, value)
        for prop, values in property_test_cases.items()
        for value in values
    ]

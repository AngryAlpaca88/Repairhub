"""Pricing service for profit validation."""
from decimal import Decimal
from typing import Optional

from app.schemas import PricingValidation


def validate_ticket_pricing(
    total_parts_cost: Decimal,
    total_labor: Decimal,
    total_price: Decimal,
    minimum_profit: Decimal,
) -> PricingValidation:
    """
    Validate that a ticket meets the minimum pure profit requirement.

    Pure profit is calculated as:
    total_price - total_parts_cost

    This represents the margin on parts used. Labor is considered
    pure profit by default.

    Args:
        total_parts_cost: Total cost of parts used
        total_labor: Total labor charges
        total_price: Total price charged to customer
        minimum_profit: Minimum required pure profit

    Returns:
        PricingValidation with validation result and details
    """
    # Calculate pure profit (price minus cost of parts)
    pure_profit = total_price - total_parts_cost

    # Check if meets minimum
    is_valid = pure_profit >= minimum_profit
    requires_override = not is_valid

    message: Optional[str] = None
    if requires_override:
        shortfall = minimum_profit - pure_profit
        message = (
            f"Pure profit (${pure_profit:.2f}) is below minimum (${minimum_profit:.2f}). "
            f"Increase price by at least ${shortfall:.2f} or obtain manager/owner override."
        )

    return PricingValidation(
        is_valid=is_valid,
        total_parts_cost=total_parts_cost,
        total_labor=total_labor,
        total_price=total_price,
        pure_profit=pure_profit,
        minimum_required_profit=minimum_profit,
        requires_override=requires_override,
        message=message,
    )


def calculate_suggested_price(
    total_parts_cost: Decimal,
    total_labor: Decimal,
    minimum_profit: Decimal,
) -> Decimal:
    """
    Calculate the minimum suggested price to meet profit requirements.

    Args:
        total_parts_cost: Total cost of parts used
        total_labor: Total labor charges
        minimum_profit: Minimum required pure profit

    Returns:
        Minimum price that would satisfy profit requirements
    """
    # Minimum price = parts cost + minimum profit
    # Labor is added on top
    return total_parts_cost + minimum_profit

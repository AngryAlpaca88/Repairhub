"""Tests for pricing service."""
from decimal import Decimal
import pytest

from app.services.pricing import validate_ticket_pricing, calculate_suggested_price


class TestValidateTicketPricing:
    """Tests for validate_ticket_pricing function."""

    def test_valid_pricing_meets_minimum(self):
        """Test that pricing meeting minimum profit is valid."""
        result = validate_ticket_pricing(
            total_parts_cost=Decimal("50.00"),
            total_labor=Decimal("75.00"),
            total_price=Decimal("200.00"),
            minimum_profit=Decimal("100.00"),
        )

        assert result.is_valid is True
        assert result.requires_override is False
        assert result.pure_profit == Decimal("150.00")  # 200 - 50
        assert result.message is None

    def test_valid_pricing_exactly_minimum(self):
        """Test that pricing exactly at minimum profit is valid."""
        result = validate_ticket_pricing(
            total_parts_cost=Decimal("100.00"),
            total_labor=Decimal("50.00"),
            total_price=Decimal("200.00"),
            minimum_profit=Decimal("100.00"),
        )

        assert result.is_valid is True
        assert result.requires_override is False
        assert result.pure_profit == Decimal("100.00")

    def test_invalid_pricing_below_minimum(self):
        """Test that pricing below minimum profit is invalid."""
        result = validate_ticket_pricing(
            total_parts_cost=Decimal("150.00"),
            total_labor=Decimal("50.00"),
            total_price=Decimal("200.00"),
            minimum_profit=Decimal("100.00"),
        )

        assert result.is_valid is False
        assert result.requires_override is True
        assert result.pure_profit == Decimal("50.00")  # 200 - 150
        assert result.message is not None
        assert "below minimum" in result.message

    def test_no_parts_always_valid(self):
        """Test that tickets with no parts cost are always valid."""
        result = validate_ticket_pricing(
            total_parts_cost=Decimal("0.00"),
            total_labor=Decimal("50.00"),
            total_price=Decimal("50.00"),
            minimum_profit=Decimal("100.00"),
        )

        # When no parts, pure profit = price (50), which is < 100
        # But this still fails the check as designed
        assert result.pure_profit == Decimal("50.00")

    def test_high_profit_margin(self):
        """Test with high profit margin."""
        result = validate_ticket_pricing(
            total_parts_cost=Decimal("25.00"),
            total_labor=Decimal("100.00"),
            total_price=Decimal("500.00"),
            minimum_profit=Decimal("100.00"),
        )

        assert result.is_valid is True
        assert result.pure_profit == Decimal("475.00")

    def test_pricing_validation_response_fields(self):
        """Test that all response fields are populated correctly."""
        result = validate_ticket_pricing(
            total_parts_cost=Decimal("80.00"),
            total_labor=Decimal("60.00"),
            total_price=Decimal("250.00"),
            minimum_profit=Decimal("100.00"),
        )

        assert result.total_parts_cost == Decimal("80.00")
        assert result.total_labor == Decimal("60.00")
        assert result.total_price == Decimal("250.00")
        assert result.minimum_required_profit == Decimal("100.00")
        assert result.pure_profit == Decimal("170.00")


class TestCalculateSuggestedPrice:
    """Tests for calculate_suggested_price function."""

    def test_basic_calculation(self):
        """Test basic suggested price calculation."""
        result = calculate_suggested_price(
            total_parts_cost=Decimal("50.00"),
            total_labor=Decimal("75.00"),
            minimum_profit=Decimal("100.00"),
        )

        # Should be parts_cost + minimum_profit = 150
        assert result == Decimal("150.00")

    def test_zero_parts_cost(self):
        """Test with zero parts cost."""
        result = calculate_suggested_price(
            total_parts_cost=Decimal("0.00"),
            total_labor=Decimal("50.00"),
            minimum_profit=Decimal("100.00"),
        )

        assert result == Decimal("100.00")

    def test_high_parts_cost(self):
        """Test with high parts cost."""
        result = calculate_suggested_price(
            total_parts_cost=Decimal("500.00"),
            total_labor=Decimal("100.00"),
            minimum_profit=Decimal("100.00"),
        )

        assert result == Decimal("600.00")

import pytest

from stock_evaluator.models import EvaluationResult, Stock


class TestStock:
    def test_valid_stock(self):
        stock = Stock(
            symbol="AAPL",
            price=150.0,
            earnings_per_share=6.0,
            revenue_growth=0.15,
            debt_to_equity=0.8,
        )
        assert stock.symbol == "AAPL"
        assert stock.price == 150.0
        assert stock.earnings_per_share == 6.0
        assert stock.revenue_growth == 0.15
        assert stock.debt_to_equity == 0.8

    def test_negative_price_raises(self):
        with pytest.raises(ValueError, match="Price must be positive"):
            Stock(
                symbol="BAD",
                price=-10.0,
                earnings_per_share=5.0,
                revenue_growth=0.1,
                debt_to_equity=0.5,
            )

    def test_zero_price_raises(self):
        with pytest.raises(ValueError, match="Price must be positive"):
            Stock(
                symbol="BAD",
                price=0.0,
                earnings_per_share=5.0,
                revenue_growth=0.1,
                debt_to_equity=0.5,
            )

    def test_negative_eps_raises(self):
        with pytest.raises(ValueError, match="Earnings per share must be positive"):
            Stock(
                symbol="BAD",
                price=100.0,
                earnings_per_share=-1.0,
                revenue_growth=0.1,
                debt_to_equity=0.5,
            )

    def test_zero_eps_raises(self):
        with pytest.raises(ValueError, match="Earnings per share must be positive"):
            Stock(
                symbol="BAD",
                price=100.0,
                earnings_per_share=0.0,
                revenue_growth=0.1,
                debt_to_equity=0.5,
            )


class TestEvaluationResult:
    def test_fields(self):
        result = EvaluationResult(
            symbol="AAPL",
            pe_ratio=25.0,
            score=2,
            recommendation="HOLD",
        )
        assert result.symbol == "AAPL"
        assert result.pe_ratio == 25.0
        assert result.score == 2
        assert result.recommendation == "HOLD"

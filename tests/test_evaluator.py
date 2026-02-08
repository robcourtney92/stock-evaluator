import pytest

from stock_evaluator.evaluator import (
    DEFAULT_DEBT_THRESHOLD,
    DEFAULT_GROWTH_THRESHOLD,
    DEFAULT_PE_THRESHOLD,
    StockEvaluator,
)
from stock_evaluator.models import Stock


def _make_stock(
    price: float = 100.0,
    eps: float = 10.0,
    growth: float = 0.15,
    debt: float = 0.5,
) -> Stock:
    return Stock(
        symbol="TEST",
        price=price,
        earnings_per_share=eps,
        revenue_growth=growth,
        debt_to_equity=debt,
    )


class TestPeRatio:
    def test_basic(self):
        evaluator = StockEvaluator()
        stock = _make_stock(price=150.0, eps=10.0)
        assert evaluator.pe_ratio(stock) == 15.0

    def test_fractional(self):
        evaluator = StockEvaluator()
        stock = _make_stock(price=100.0, eps=3.0)
        assert evaluator.pe_ratio(stock) == pytest.approx(33.333, rel=1e-2)


class TestScore:
    def test_all_criteria_met(self):
        evaluator = StockEvaluator()
        stock = _make_stock(price=100.0, eps=10.0, growth=0.15, debt=0.5)
        assert evaluator._score(stock) == 3

    def test_no_criteria_met(self):
        evaluator = StockEvaluator()
        stock = _make_stock(price=200.0, eps=1.0, growth=0.05, debt=2.0)
        assert evaluator._score(stock) == 0

    def test_only_pe_met(self):
        evaluator = StockEvaluator()
        stock = _make_stock(price=100.0, eps=10.0, growth=0.05, debt=2.0)
        assert evaluator._score(stock) == 1

    def test_only_growth_met(self):
        evaluator = StockEvaluator()
        stock = _make_stock(price=200.0, eps=1.0, growth=0.15, debt=2.0)
        assert evaluator._score(stock) == 1

    def test_only_debt_met(self):
        evaluator = StockEvaluator()
        stock = _make_stock(price=200.0, eps=1.0, growth=0.05, debt=0.5)
        assert evaluator._score(stock) == 1

    def test_boundary_pe_at_threshold(self):
        evaluator = StockEvaluator()
        stock = _make_stock(price=150.0, eps=10.0)
        assert evaluator._score(stock) < 3

    def test_boundary_growth_at_threshold(self):
        evaluator = StockEvaluator()
        stock = _make_stock(growth=0.10)
        assert evaluator._score(stock) == 2

    def test_boundary_debt_at_threshold(self):
        evaluator = StockEvaluator()
        stock = _make_stock(debt=1.0)
        assert evaluator._score(stock) == 2


class TestRecommend:
    def test_buy(self):
        evaluator = StockEvaluator()
        assert evaluator._recommend(3) == "BUY"

    def test_hold(self):
        evaluator = StockEvaluator()
        assert evaluator._recommend(2) == "HOLD"

    def test_avoid_one(self):
        evaluator = StockEvaluator()
        assert evaluator._recommend(1) == "AVOID"

    def test_avoid_zero(self):
        evaluator = StockEvaluator()
        assert evaluator._recommend(0) == "AVOID"


class TestEvaluate:
    def test_buy_recommendation(self):
        evaluator = StockEvaluator()
        stock = _make_stock(price=100.0, eps=10.0, growth=0.15, debt=0.5)
        result = evaluator.evaluate(stock)
        assert result.recommendation == "BUY"
        assert result.score == 3
        assert result.pe_ratio == 10.0
        assert result.symbol == "TEST"

    def test_hold_recommendation(self):
        evaluator = StockEvaluator()
        stock = _make_stock(price=200.0, eps=1.0, growth=0.15, debt=0.5)
        result = evaluator.evaluate(stock)
        assert result.recommendation == "HOLD"
        assert result.score == 2

    def test_avoid_recommendation(self):
        evaluator = StockEvaluator()
        stock = _make_stock(price=200.0, eps=1.0, growth=0.05, debt=2.0)
        result = evaluator.evaluate(stock)
        assert result.recommendation == "AVOID"
        assert result.score == 0

    def test_pe_ratio_rounded(self):
        evaluator = StockEvaluator()
        stock = _make_stock(price=100.0, eps=3.0)
        result = evaluator.evaluate(stock)
        assert result.pe_ratio == 33.33


class TestCustomThresholds:
    def test_custom_pe_threshold(self):
        evaluator = StockEvaluator(pe_threshold=20.0)
        stock = _make_stock(price=180.0, eps=10.0, growth=0.15, debt=0.5)
        assert evaluator._score(stock) == 3

    def test_custom_growth_threshold(self):
        evaluator = StockEvaluator(growth_threshold=0.05)
        stock = _make_stock(price=100.0, eps=10.0, growth=0.07, debt=0.5)
        assert evaluator._score(stock) == 3

    def test_custom_debt_threshold(self):
        evaluator = StockEvaluator(debt_threshold=2.0)
        stock = _make_stock(price=100.0, eps=10.0, growth=0.15, debt=1.5)
        assert evaluator._score(stock) == 3

    def test_defaults_match_constants(self):
        evaluator = StockEvaluator()
        assert evaluator.pe_threshold == DEFAULT_PE_THRESHOLD
        assert evaluator.growth_threshold == DEFAULT_GROWTH_THRESHOLD
        assert evaluator.debt_threshold == DEFAULT_DEBT_THRESHOLD

from stock_evaluator.models import EvaluationResult, Stock

DEFAULT_PE_THRESHOLD = 15.0
DEFAULT_GROWTH_THRESHOLD = 0.10
DEFAULT_DEBT_THRESHOLD = 1.0


class StockEvaluator:
    def __init__(
        self,
        pe_threshold: float = DEFAULT_PE_THRESHOLD,
        growth_threshold: float = DEFAULT_GROWTH_THRESHOLD,
        debt_threshold: float = DEFAULT_DEBT_THRESHOLD,
    ):
        self.pe_threshold = pe_threshold
        self.growth_threshold = growth_threshold
        self.debt_threshold = debt_threshold

    def pe_ratio(self, stock: Stock) -> float:
        return stock.price / stock.earnings_per_share

    def _score(self, stock: Stock) -> int:
        pe = self.pe_ratio(stock)
        score = 0
        if pe < self.pe_threshold:
            score += 1
        if stock.revenue_growth > self.growth_threshold:
            score += 1
        if stock.debt_to_equity < self.debt_threshold:
            score += 1
        return score

    def _recommend(self, score: int) -> str:
        if score >= 3:
            return "BUY"
        elif score == 2:
            return "HOLD"
        return "AVOID"

    def evaluate(self, stock: Stock) -> EvaluationResult:
        pe = self.pe_ratio(stock)
        score = self._score(stock)
        recommendation = self._recommend(score)
        return EvaluationResult(
            symbol=stock.symbol,
            pe_ratio=round(pe, 2),
            score=score,
            recommendation=recommendation,
        )

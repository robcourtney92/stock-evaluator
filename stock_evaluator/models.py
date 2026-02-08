from dataclasses import dataclass


@dataclass
class Stock:
    symbol: str
    price: float
    earnings_per_share: float
    revenue_growth: float
    debt_to_equity: float

    def __post_init__(self):
        if self.price <= 0:
            raise ValueError("Price must be positive")
        if self.earnings_per_share <= 0:
            raise ValueError("Earnings per share must be positive")


@dataclass
class EvaluationResult:
    symbol: str
    pe_ratio: float
    score: int
    recommendation: str

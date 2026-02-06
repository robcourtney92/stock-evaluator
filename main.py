stock-evaluator/
├── README.md
├── stock_evaluator/
│   ├── __init__.py
│   ├── models.py
│   ├── evaluator.py
│   └── cli.py
└── main.py
from dataclasses import dataclass


@dataclass
class Stock:
    symbol: str
    price: float
    earnings_per_share: float
    revenue_growth: float
    debt_to_equity: float
from .models import Stock


class StockEvaluator:
    def pe_ratio(self, stock: Stock) -> float:
        if stock.earnings_per_share <= 0:
            raise ValueError("EPS must be positive")
        return stock.price / stock.earnings_per_share

    def evaluate(self, stock: Stock) -> dict:
        pe = self.pe_ratio(stock)

        score = 0
        if pe < 15:
            score += 1
        if stock.revenue_growth > 0.10:
            score += 1
        if stock.debt_to_equity < 1:
            score += 1

        if score >= 3:
            recommendation = "BUY"
        elif score == 2:
            recommendation = "HOLD"
        else:
            recommendation = "AVOID"

        return {
            "symbol": stock.symbol,
            "pe_ratio": round(pe, 2),
            "score": score,
            "recommendation": recommendation,
from .models import Stock
from .evaluator import StockEvaluator


def run_cli():
    print("Simple Stock Evaluator")

    symbol = input("Stock symbol: ")
    price = float(input("Stock price: "))
    eps = float(input("Earnings per share: "))
    growth = float(input("Revenue growth (e.g. 0.12): "))
    debt = float(input("Debt-to-equity ratio: "))

    stock = Stock(
        symbol=symbol,
        price=price,
        earnings_per_share=eps,
        revenue_growth=growth,
        debt_to_equity=debt,
    )

    evaluator = StockEvaluator()
    result = evaluator.evaluate(stock)

    print("\nEvaluation Result")
    for k, v in result.items():
        print(f"{k}: {v}")
from stock_evaluator.cli import run_cli

if __name__ == "__main__":
    run_cli()

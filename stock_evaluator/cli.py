from stock_evaluator.auth import authenticate, is_auth_configured
from stock_evaluator.evaluator import StockEvaluator
from stock_evaluator.models import Stock

MAX_AUTH_ATTEMPTS = 3


def _prompt_float(label: str) -> float:
    while True:
        try:
            return float(input(label))
        except ValueError:
            print("Please enter a valid number.")


def run_cli():
    print("Simple Stock Evaluator")

    if is_auth_configured():
        for attempt in range(MAX_AUTH_ATTEMPTS):
            if authenticate():
                break
            remaining = MAX_AUTH_ATTEMPTS - attempt - 1
            if remaining > 0:
                print(f"Authentication failed. {remaining} attempt(s) remaining.")
            else:
                print("Authentication failed. Access denied.")
                return

    symbol = input("Stock symbol: ")
    price = _prompt_float("Stock price: ")
    eps = _prompt_float("Earnings per share: ")
    growth = _prompt_float("Revenue growth (e.g. 0.12): ")
    debt = _prompt_float("Debt-to-equity ratio: ")

    try:
        stock = Stock(
            symbol=symbol,
            price=price,
            earnings_per_share=eps,
            revenue_growth=growth,
            debt_to_equity=debt,
        )
    except ValueError as e:
        print(f"Invalid input: {e}")
        return

    evaluator = StockEvaluator()
    result = evaluator.evaluate(stock)

    print("\nEvaluation Result")
    print(f"symbol: {result.symbol}")
    print(f"pe_ratio: {result.pe_ratio}")
    print(f"score: {result.score}")
    print(f"recommendation: {result.recommendation}")

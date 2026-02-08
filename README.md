# stock-evaluator

A command-line stock evaluation tool that calculates PE ratios and provides investment recommendations (BUY / HOLD / AVOID) based on fundamental financial metrics.

## Installation

Requires Python 3.10+.

```bash
pip install -e .
```

## Usage

Run the evaluator interactively:

```bash
python main.py
```

You will be prompted for:

| Field | Description | Example |
|-------|-------------|---------|
| Stock symbol | Ticker identifier | `AAPL` |
| Stock price | Current share price | `150.0` |
| Earnings per share | Company EPS | `6.0` |
| Revenue growth | Decimal growth rate | `0.12` |
| Debt-to-equity ratio | Leverage ratio | `0.8` |

## Scoring Criteria

Each stock is scored 0-3 based on these thresholds (configurable via `StockEvaluator`):

| Criterion | Default Threshold | Points |
|-----------|-------------------|--------|
| PE ratio | < 15 | +1 |
| Revenue growth | > 10% | +1 |
| Debt-to-equity | < 1.0 | +1 |

**Recommendations:** 3 = BUY, 2 = HOLD, 0-1 = AVOID

## Project Structure

```
stock-evaluator/
├── main.py                  # Entry point
├── pyproject.toml           # Project configuration
├── stock_evaluator/
│   ├── __init__.py
│   ├── models.py            # Stock and EvaluationResult dataclasses
│   ├── evaluator.py         # Scoring and recommendation logic
│   └── cli.py               # Interactive CLI interface
└── tests/
    ├── test_models.py
    ├── test_evaluator.py
    └── test_cli.py
```

## Running Tests

```bash
pytest
```

from unittest.mock import patch

from stock_evaluator.cli import run_cli


class TestRunCli:
    @patch("builtins.input", side_effect=["AAPL", "100", "10", "0.15", "0.5"])
    @patch("builtins.print")
    def test_successful_evaluation(self, mock_print, mock_input):
        run_cli()
        printed = [str(args[0]) for args, _ in mock_print.call_args_list]
        assert any("BUY" in line for line in printed)

    @patch("builtins.input", side_effect=["BAD", "-10", "100", "5", "0.15", "0.5"])
    @patch("builtins.print")
    def test_negative_price_shows_error(self, mock_print, mock_input):
        run_cli()
        printed = [str(args[0]) for args, _ in mock_print.call_args_list]
        assert any("Invalid input" in line for line in printed)

    @patch("builtins.input", side_effect=["BAD", "100", "-5", "50", "5", "0.15", "0.5"])
    @patch("builtins.print")
    def test_negative_eps_shows_error(self, mock_print, mock_input):
        run_cli()
        printed = [str(args[0]) for args, _ in mock_print.call_args_list]
        assert any("Invalid input" in line for line in printed)

    @patch("builtins.input", side_effect=["AAPL", "abc", "100", "10", "0.15", "0.5"])
    @patch("builtins.print")
    def test_invalid_float_retries(self, mock_print, mock_input):
        run_cli()
        printed = [str(args[0]) for args, _ in mock_print.call_args_list]
        assert any("Please enter a valid number" in line for line in printed)
        assert any("BUY" in line for line in printed)

from unittest.mock import patch

from stock_evaluator.cli import run_cli

NO_AUTH = {"stock_evaluator.cli.is_auth_configured": lambda: False}


class TestRunCliNoAuth:
    @patch("stock_evaluator.cli.is_auth_configured", return_value=False)
    @patch("builtins.input", side_effect=["AAPL", "100", "10", "0.15", "0.5"])
    @patch("builtins.print")
    def test_successful_evaluation(self, mock_print, mock_input, _mock_auth):
        run_cli()
        printed = [str(args[0]) for args, _ in mock_print.call_args_list]
        assert any("BUY" in line for line in printed)

    @patch("stock_evaluator.cli.is_auth_configured", return_value=False)
    @patch("builtins.input", side_effect=["BAD", "-10", "100", "5", "0.15", "0.5"])
    @patch("builtins.print")
    def test_negative_price_shows_error(self, mock_print, mock_input, _mock_auth):
        run_cli()
        printed = [str(args[0]) for args, _ in mock_print.call_args_list]
        assert any("Invalid input" in line for line in printed)

    @patch("stock_evaluator.cli.is_auth_configured", return_value=False)
    @patch("builtins.input", side_effect=["BAD", "100", "-5", "50", "5", "0.15", "0.5"])
    @patch("builtins.print")
    def test_negative_eps_shows_error(self, mock_print, mock_input, _mock_auth):
        run_cli()
        printed = [str(args[0]) for args, _ in mock_print.call_args_list]
        assert any("Invalid input" in line for line in printed)

    @patch("stock_evaluator.cli.is_auth_configured", return_value=False)
    @patch("builtins.input", side_effect=["AAPL", "abc", "100", "10", "0.15", "0.5"])
    @patch("builtins.print")
    def test_invalid_float_retries(self, mock_print, mock_input, _mock_auth):
        run_cli()
        printed = [str(args[0]) for args, _ in mock_print.call_args_list]
        assert any("Please enter a valid number" in line for line in printed)
        assert any("BUY" in line for line in printed)


class TestRunCliWithAuth:
    @patch("stock_evaluator.cli.is_auth_configured", return_value=True)
    @patch("stock_evaluator.cli.authenticate", return_value=True)
    @patch("builtins.input", side_effect=["AAPL", "100", "10", "0.15", "0.5"])
    @patch("builtins.print")
    def test_auth_success_proceeds(self, mock_print, mock_input, _mock_auth, _mock_cfg):
        run_cli()
        printed = [str(args[0]) for args, _ in mock_print.call_args_list]
        assert any("BUY" in line for line in printed)

    @patch("stock_evaluator.cli.is_auth_configured", return_value=True)
    @patch("stock_evaluator.cli.authenticate", return_value=False)
    @patch("builtins.print")
    def test_auth_failure_denies_access(self, mock_print, _mock_auth, _mock_cfg):
        run_cli()
        printed = [str(args[0]) for args, _ in mock_print.call_args_list]
        assert any("Access denied" in line for line in printed)
        assert not any("Evaluation Result" in line for line in printed)

    @patch("stock_evaluator.cli.is_auth_configured", return_value=True)
    @patch("stock_evaluator.cli.authenticate", side_effect=[False, True])
    @patch("builtins.input", side_effect=["AAPL", "100", "10", "0.15", "0.5"])
    @patch("builtins.print")
    def test_auth_retry_then_success(self, mock_print, mock_input, _mock_auth, _mock_cfg):
        run_cli()
        printed = [str(args[0]) for args, _ in mock_print.call_args_list]
        assert any("2 attempt(s) remaining" in line for line in printed)
        assert any("BUY" in line for line in printed)

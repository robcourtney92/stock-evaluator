import hashlib
from unittest.mock import patch

from stock_evaluator.auth import _hash_password, authenticate, is_auth_configured


class TestHashPassword:
    def test_returns_sha256_hex(self):
        result = _hash_password("secret")
        expected = hashlib.sha256(b"secret").hexdigest()
        assert result == expected

    def test_different_passwords_differ(self):
        assert _hash_password("a") != _hash_password("b")


class TestIsAuthConfigured:
    def test_both_set(self):
        env = {"STOCK_EVAL_USER": "admin", "STOCK_EVAL_PASS_HASH": "abc123"}
        with patch.dict("os.environ", env, clear=False):
            assert is_auth_configured() is True

    def test_missing_user(self):
        env = {"STOCK_EVAL_PASS_HASH": "abc123"}
        with patch.dict("os.environ", env, clear=False):
            with patch.dict("os.environ", {"STOCK_EVAL_USER": ""}, clear=False):
                assert is_auth_configured() is False

    def test_missing_hash(self):
        env = {"STOCK_EVAL_USER": "admin"}
        with patch.dict("os.environ", env, clear=False):
            with patch.dict("os.environ", {"STOCK_EVAL_PASS_HASH": ""}, clear=False):
                assert is_auth_configured() is False

    def test_neither_set(self):
        with patch.dict("os.environ", {}, clear=True):
            assert is_auth_configured() is False


class TestAuthenticate:
    def test_correct_credentials(self):
        password_hash = _hash_password("secret")
        env = {"STOCK_EVAL_USER": "admin", "STOCK_EVAL_PASS_HASH": password_hash}
        with patch.dict("os.environ", env, clear=False):
            with patch("builtins.input", return_value="admin"):
                with patch("getpass.getpass", return_value="secret"):
                    assert authenticate() is True

    def test_wrong_password(self):
        password_hash = _hash_password("secret")
        env = {"STOCK_EVAL_USER": "admin", "STOCK_EVAL_PASS_HASH": password_hash}
        with patch.dict("os.environ", env, clear=False):
            with patch("builtins.input", return_value="admin"):
                with patch("getpass.getpass", return_value="wrong"):
                    assert authenticate() is False

    def test_wrong_username(self):
        password_hash = _hash_password("secret")
        env = {"STOCK_EVAL_USER": "admin", "STOCK_EVAL_PASS_HASH": password_hash}
        with patch.dict("os.environ", env, clear=False):
            with patch("builtins.input", return_value="hacker"):
                with patch("getpass.getpass", return_value="secret"):
                    assert authenticate() is False

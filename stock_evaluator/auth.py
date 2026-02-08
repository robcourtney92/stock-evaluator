import getpass
import hashlib
import os


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def is_auth_configured() -> bool:
    return bool(os.environ.get("STOCK_EVAL_USER") and os.environ.get("STOCK_EVAL_PASS_HASH"))


def authenticate() -> bool:
    expected_user = os.environ.get("STOCK_EVAL_USER", "")
    expected_hash = os.environ.get("STOCK_EVAL_PASS_HASH", "")

    username = input("Username: ")
    password = getpass.getpass("Password: ")

    return username == expected_user and _hash_password(password) == expected_hash

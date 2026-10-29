import bcrypt

# bcrypt only looks at the first 72 bytes of a password.
MAX_PASSWORD_BYTES = 72


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    if len(password.encode("utf-8")) > MAX_PASSWORD_BYTES:
        return False
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

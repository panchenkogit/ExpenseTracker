import bcrypt


def hash_password(password: str) -> str:
    hash_pass = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12))
    return hash_pass.decode("utf-8")


def check_password(password: str, hashed_pass: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_pass.encode("utf-8"))
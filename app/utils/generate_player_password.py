import random


def generate_password() -> str:
    return f"ao{random.randint(1000, 9999)}"

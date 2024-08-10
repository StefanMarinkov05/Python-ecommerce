import hashlib


def main():
    hash_password_sha256(input("Password: "))


def hash_password_sha256(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


if __name__ == "__main__":
    main()

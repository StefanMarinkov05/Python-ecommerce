from sqlalchemy.orm import sessionmaker
from crud.create_tables import engine, User
import os, pyfiglet, time
from support_functions.hashing_password import hash_password_sha256
from support_functions.get_ip import get_ipv4
from support_functions.datetime_format import get_current_time
from .login import log_in
from validator_collection import checkers
from .allocate_privilege_panel import allocate

Session = sessionmaker(bind=engine)


def register(session):

    os.system("cls" if os.name == "nt" else "clear")

    font = pyfiglet.Figlet(font="roman")
    print("\n\n" + font.renderText("Register"))

    _first_name = input("First name: ")
    _last_name = input("Last name: ")
    _email = input("Email: ")

    while not checkers.is_email(_email):
        _email = input("Invalid email! Please try again: ")

    existing_user = session.query(User).filter_by(email=_email).first()

    if existing_user is not None:
        print("Email already in use. Redirecting to login...")
        time.sleep(3)
        session.close()
        log_in(session)
        return

    _password = input("Password: ")
    _password2 = input("Password (again): ")

    while _password != _password2:
        print("Passwords do not match. Please try again.\n")
        _password = input("Password: ")
        _password2 = input("Password (again): ")
        return

    _balance = 0

    new_user = User(
        first_name=_first_name,
        last_name=_last_name,
        email=_email,
        password=hash_password_sha256(_password),
        ip_address=get_ipv4(),
        last_used=get_current_time(),  # In case of application crash
        is_admin=_email.endswith("@admin.com"),
        balance=_balance,
    )
    session.add(new_user)
    session.commit()

    new_user = session.query(User).filter_by(email=_email).first()
    allocate(new_user, session)

    # session.close()


if __name__ == "__main__":
    register()

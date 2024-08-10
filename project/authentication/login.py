from sqlalchemy.orm import sessionmaker
from crud.create_tables import engine, User
import os, sys
import pyfiglet, questionary
from support_functions.hashing_password import hash_password_sha256
from support_functions.get_ip import get_ipv4
from support_functions.datetime_format import get_current_time
from .allocate_privilege_panel import allocate

Session = sessionmaker(bind=engine)


def log_in(session):
    """
    Handle user login by verifying credentials and allocating the user to the appropriate panel.
    """
    os.system("cls" if os.name == "nt" else "clear")

    font = pyfiglet.Figlet(font="roman")
    print("\n\n" + font.renderText("Log in"))

    email = input("Email: ")
    password = input("Password: ")

    hashed_password = hash_password_sha256(password)

    # session = Session()
    existing_user = (
        session.query(User).filter_by(email=email, password=hashed_password).first()
    )

    if existing_user:
        existing_user.ip_address = get_ipv4()
        existing_user.is_signed_out = False  # In case of application crash
        existing_user.last_used = get_current_time()
        session.commit()

        allocate(existing_user, session)
        # session.close()

        return existing_user
    else:
        print("Invalid email or password. Please try again or register.")
        answer = questionary.select(
            "Main Menu", choices=["Try again", "Register", "Exit"]
        ).ask()

        match answer:
            case "Try again":
                log_in()
            case "Register":
                from .register import register

                register()
            case "Exit":
                sys.exit()


def log_out(current_user: User, session):
    """
    Log out the current user by setting the is_signed_out flag and closing the session.
    """
    # session = Session()
    current_user.is_signed_out = True
    current_user.last_used = get_current_time()
    session.commit()
    # session.close()
    from project import start_menu

    start_menu(session)

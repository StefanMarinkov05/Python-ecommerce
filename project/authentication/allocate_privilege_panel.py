from sqlalchemy.orm import sessionmaker
from crud.create_tables import engine, User
import sys, os
from getpass import getpass
from support_functions.datetime_format import get_current_time
from support_functions.hashing_password import hash_password_sha256


Session = sessionmaker(bind=engine)


def allocate(current_user: User, session):
    current_user.is_signed_out = False
    session.commit()

    from project import logged_panel

    logged_panel(current_user, session)


def quit_app(current_user: User, session):
    current_user.is_signed_out = False
    current_user.last_used = get_current_time()
    session.commit()
    session.close()
    sys.exit()


def authorize(current_user: User):
    """
    Prompt the user to enter their password and verify it against the stored password.

    This function prompts the user to enter their password and compares it with the
    hashed password stored in the `current_user` object. If the entered password does not
    match, the user is informed with an error message and prompted to try again. The function
    continues to prompt the user until the correct password is provided or the user presses Enter
    without entering a password, which causes the prompt to restart.

    :param current_user: The `User` object representing the currently logged-in user.
                         This object contains the stored hashed password.
    :type current_user: User
    :return: None
    :rtype: None

    :raises: None
    """
    user_password = getpass("Enter user password: ")
    while hash_password_sha256(user_password) != current_user.password:
        user_password = getpass("\n\33[91mWrong password!\33[0m\n\nPress Enter to go back\nEnter user password: ")
        if user_password == "":
            continue

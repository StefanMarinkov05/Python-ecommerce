import os
import sys
import pyfiglet
import questionary
from sqlalchemy import inspect, text
from sqlalchemy.orm import sessionmaker
from crud.create_tables import engine, User
from authentication import log_in, register, log_out, authorize, quit_app
from crud import (
    print_users,
    print_cars,
    print_brands_models,
    print_orders,
    drop_db,
    regenerate_db,
    deposit,
    withdraw,
)
from support_functions import get_ipv4
from support_functions.datetime_format import get_current_time
from nicegui import ui
from GUI import start_page

Session = sessionmaker(bind=engine)


def main():
    session = Session()
    try:
        start_application(session)
    except KeyboardInterrupt:
        os.system("cls" if os.name == "nt" else "clear")
        print("\33[1mProgram closed!\n\33[0m")
        pass


def start_menu(session):
    logged_user = (
        session.query(User)
        .filter_by(ip_address=get_ipv4(), is_signed_out=False)
        .order_by(User.last_used.desc())
        .first()
    )
    if logged_user is not None:
        logged_user.last_used = get_current_time()  # In case of application crash
        logged_panel(logged_user, session)

    else:
        os.system("cls" if os.name == "nt" else "clear")
        font = pyfiglet.Figlet(font="roman")
        print("\n\n" + font.renderText("BuyCar"))

        answer = questionary.select(
            "Main Menu",
            choices=["Log in", "Register", "View all brands", "View all cars", "Exit"],
        ).ask()

        match answer:
            case "Log in":
                log_in(session)
            case "Register":
                register(session)
            case "View all brands":
                print_brands_models()
            case "View all cars":
                print_cars()
            case "Exit":
                sys.exit()

        input("Press Enter to continue...")
        start_menu(session)


def is_database_empty(session):
    """
    Checks if the database has tables and if those tables have any data.

    :param session: SQLAlchemy session object
    :return: True if the database has no tables or all tables are empty, False otherwise
    :rtype: bool
    """
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if not tables:
        return True

    for table_name in tables:
        query = text(f'SELECT COUNT(*) FROM "{table_name}"')
        count = session.execute(query).scalar()
        if count > 0:
            return False

    return True


def start_application(session):
    if is_database_empty(session):
        print("Database is empty or does not have any data. Generating database...")
        regenerate_db()

    start_page(session)


def logged_panel(current_user: User, session):
    """
    Displays the logged panel based on user role (customer or admin).

    :param current_user: The currently logged-in user
    :param session: SQLAlchemy session object
    """
    os.system("cls" if os.name == "nt" else "clear")
    font = pyfiglet.Figlet(font="roman")
    role = "Admin" if current_user.is_admin else "Customer"
    print(f"\n\n{font.renderText(role)}")
    print(f"Current balance: ${current_user.balance:,.2f}")

    choices = [
        "[*] Deposit money",
        "[*] Withdraw money",
        "[*] View all brands",
        "[*] View all cars",
    ]

    if current_user.is_admin:
        choices.extend(
            [
                "[*] View all users",
                "[*] View all orders",
                "[*] Regenerate database",
                "[*] Drop database",
            ]
        )

    choices.extend(
        [
            "[*] Log out",
            "[*] Exit",
        ]
    )

    answer = questionary.select(f"{role} Panel", choices=choices).ask()

    match answer:
        case "[*] Deposit money":
            deposit(current_user, session)
        case "[*] Withdraw money":
            withdraw(current_user, session)
        case "[*] View all users":
            authorize(current_user)
            print_users()
        case "[*] View all brands":
            print_brands_models()
        case "[*] View all cars":
            print_cars()
        case "[*] View all orders":
            authorize(current_user)
            print_orders()
        case "[*] Regenerate database":
            authorize(current_user)
            regenerate_db()
        case "[*] Drop database":
            authorize(current_user)
            drop_db()
        case "[*] Log out":
            log_out(current_user, session)
        case "[*] Exit":
            quit_app(current_user, session)

    input("Press Enter to continue...")
    logged_panel(current_user, session)


if __name__ in {"__main__", "__mp_main__"}:
    main()
    ui.run(favicon='🚗')

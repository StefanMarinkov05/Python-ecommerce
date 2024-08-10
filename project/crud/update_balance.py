import os
from sqlalchemy.orm import sessionmaker
from .create_tables import engine, User
from authentication import authorize

Session = sessionmaker(bind=engine)


def transaction_handler(current_user: User, session, action: str):
    action_type = "deposit" if action == "deposit" else "withdraw"
    action_verb = "Deposited" if action == "deposit" else "Withdrawn"

    os.system("cls" if os.name == "nt" else "clear")

    while True:
        print(
            f"\033[1mCurrent balance:\033[0m \033[92m${current_user.balance:,.2f}\n\033[0m"
        )

        amount = input(
            f"Press Enter if you want to go back\nEnter the amount to {action_type}: \033[92m"
        )
        if amount == "":
            from project import logged_panel

            logged_panel(current_user, session)
            return
        try:
            amount = float(amount)
        except ValueError:
            os.system("cls" if os.name == "nt" else "clear")

            print("\033[91m\nInvalid input. Please enter a numeric value.\n\033[0m")
            continue
        else:
            if amount <= 0:
                os.system("cls" if os.name == "nt" else "clear")

                print("\033[91m\nPlease enter a positive amount.\n\033[0m")
                continue
            elif action == "withdraw" and amount > current_user.balance:
                os.system("cls" if os.name == "nt" else "clear")

                print(
                    "\033[91m\nInsufficient balance. Please enter a smaller amount.\n\033[0m"
                )
                continue

            if action == "deposit":
                current_user.balance += amount
            else:
                current_user.balance -= amount

            session.commit()
            os.system("cls" if os.name == "nt" else "clear")

            print(f"\n\033[0m\033[1m{action_verb}:\033[0m \033[92m${amount:,.2f}\033[0m\n")

            transaction_handler(current_user, session, action)
            break


def deposit(current_user: User, session):
    authorize(current_user)
    transaction_handler(current_user, session, "deposit")


def withdraw(current_user: User, session):
    authorize(current_user)
    transaction_handler(current_user, session, "withdraw")

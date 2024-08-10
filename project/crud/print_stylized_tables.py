from sqlalchemy.orm import sessionmaker
from sqlalchemy import asc, desc
from .create_tables import engine, User, Brand, Model, Car, Order
from support_functions import print_stylized_table
from colorama import Fore, Style

Session = sessionmaker(bind=engine)
session = Session()


def sp_users(order_by="Id", desc_order=False):
    """
    Print all users in the shop along with their details in a stylized table.

    This function queries the database for all users and displays them in a table format.
    The table can be sorted based on different attributes such as First Name, Last Name, Email, or Balance.
    Sorting can be done in ascending or descending order.

    :param order_by: Specifies the attribute to sort the users by. Defaults to "Id".
    :type order_by: str
    :param desc_order: Whether to sort in descending order. Defaults to False (ascending order).
    :type desc_order: bool
    :return: A stylized table with all users, sorted based on the specified attribute and order.
    :rtype: None
    """
    order_column = {
        "First Name": User.first_name,
        "Last Name": User.last_name,
        "Email": User.email,
        "Last used": User.last_used,
        "Balance": User.balance,
        "Id": User.id,
    }.get(order_by, User.id)

    order = desc(order_column) if desc_order else asc(order_column)

    users = session.query(User).order_by(order).all()

    headers = [
        "№",
        "Id",
        "Names",
        "Email",
        "IP Address",
        "Has signed out",
        "Last used",
        "Balance",
    ]
    table = []

    for i, user in enumerate(users):
        user_data = [
            i + 1,
            user.id,
            user.first_name + " " + user.last_name,
            user.email,
            user.ip_address,
            user.is_signed_out,
            user.last_used,
            f"${user.balance:,.2f}",
        ]

        if user.email.endswith("admin.com"):
            colored_line = [
                Fore.RED + str(item) + Style.RESET_ALL for item in user_data
            ]
            table.append(colored_line)
        else:
            table.append(user_data)

    print_stylized_table(table, headers)

    session.close()


def sp_cars(order_by="Id", desc_order=False):
    """
    Print all cars in the shop along with their details in a stylized table.

    This function queries the database for all cars and displays them in a table format.
    The table can be sorted based on different attributes such as Brand, Model, Price, or Amount.
    Sorting can be done in ascending or descending order.

    The available sorting options are:
    - "Id": Sorts cars by their unique identifier.
    - "Brand": Sorts cars by the brand name.
    - "Model": Sorts cars by the model name.
    - "Price": Sorts cars by the price of the car.
    - "Amount": Sorts cars by the available amount.

    :param order_by: Specifies the attribute to sort the cars by. Defaults to "Id".
    :type order_by: str
    :param desc_order: Whether to sort in descending order. Defaults to False (ascending order).
    :type desc: bool
    :return: A stylized table with all cars, sorted based on the specified attribute and order.
    :rtype: None
    """

    order_column = {
        "Brand": Brand.name,
        "Model": Model.name,
        "Price": Car.price,
        "Amount": Car.amount,
        "Id": Car.id,
    }.get(order_by, Car.id)

    order = desc(order_column) if desc_order else asc(order_column)

    cars = session.query(Car).join(Car.brand).join(Car.model).order_by(order).all()

    headers = ["№", "Id", "Brand", "Model", "Price", "Amount"]
    table = []

    for i, car in enumerate(cars):
        table.append(
            [
                i + 1,
                car.id,
                car.brand.name,
                car.model.name,
                f"${car.price:,.2f}",
                f"{car.amount} left",
            ]
        )

    print_stylized_table(table, headers)
    session.close()


def sp_brands_models(order_by="Id", desc_order=False):
    """
    Print all car brands in the shop including all their models on a single line.

    :param order_by: Field to sort by. Options are "Id" (default), "Name".
    :type order_by: str
    :param desc_order: Whether to sort in descending order. Defaults to False (ascending order).
    :type desc: bool
    :return: A stylized table with all car brands in the database including their models.
    :rtype: None
    """

    if order_by == "Name":
        order_column = Brand.name
    else:
        order_column = Brand.id

    order = desc(order_column) if desc_order else asc(order_column)

    brands = session.query(Brand).order_by(order).all()
    models = session.query(Model).all()

    headers = ["№", "Id", "Name", "Models"]
    table = []

    # Build a dictionary of models grouped by brand name
    model_dict = {model.brand.name: [] for model in models}
    for model in models:
        model_dict[model.brand.name].append(model.name)

    for i, brand in enumerate(brands):
        row_id = i + 1
        brand_name = brand.name
        model_names = model_dict.get(brand_name, [])
        model_list = ", ".join(model_names)
        table.append(
            [
                row_id,
                brand.id,
                brand_name,
                model_list,
            ]
        )

    print_stylized_table(table, headers)
    session.close()


def sp_orders(order_by="Id", desc_order=False):
    """
    Print all orders in the shop along with their details in a stylized table.

    This function queries the database for all orders and displays them in a table format.
    The table can be sorted based on different attributes such as Brand, Model, Price, or Amount.
    Sorting can be done in ascending or descending order.

    :param order_by: Specifies the attribute to sort the orders by. Defaults to "Id".
    :type order_by: str
    :param desc_order: Whether to sort in descending order. Defaults to False (ascending order).
    :type desc_order: bool
    :return: A stylized table with all orders, sorted based on the specified attribute and order.
    :rtype: None
    """

    Session = sessionmaker(bind=engine)
    session = Session()

    order_column = {
        "Customer name": User.first_name,
        "Customer email": User.email,
        "Car brand": Car.brand,
        "Car price": Car.price,
        "Date": Order.date,
        "Id": Order.id,
    }.get(order_by, Order.id)

    order = desc(order_column) if desc_order else asc(order_column)

    orders = session.query(Order).join(Order.user).join(Order.car).order_by(order).all()

    headers = [
        "№",
        "Id",
        "Customer name",
        "Customer email",
        "Car brand",
        "Car price",
        "Date",
    ]
    table = []

    for i, order in enumerate(orders):
        table.append(
            [
                i + 1,
                order.id,
                f"{order.user.first_name} {order.user.last_name}",
                order.user.email,
                f"{order.car.brand} {order.car.model}",
                f"${order.car.price:,.2f}",
                order.date,
            ]
        )

    print_stylized_table(table, headers)
    session.close()

import random, json
from sqlalchemy.orm import sessionmaker
from .create_tables import engine, User, Brand, Model, Car, Base
from .delete_db import drop_db
from support_functions import parse_datetime


CAR_GENERATION_PROBABILITY = 0.75  # 0 <= P(G) <= 1


def main():
    regenerate_db()


def generate_random_price():
    """
    Generates a random price for a car.

    :return: A randomly generated price
    :rtype: float
    """
    return round(random.uniform(10000, 420000), 2)


def generate_random_amount():
    """
    Generates a random amount of cars available.

    :return: A randomly generated amount
    :rtype: int
    """
    return random.randint(0, 42)


def load_test_data(file_path):
    """
    Loads test data from a JSON file.

    :param file_path: Path to the JSON file containing test data
    :type file_path: str
    :return: Data loaded from the JSON file
    :rtype: dict
    """
    with open(file_path, "r") as file:
        return json.load(file)



def add_test_data():
    """
    Generates unique test data for car brands and models using the data from test_data.json.
    If these brands or models already exist in the database, the query for their creation is skipped.
    To avoid overfitting, there is a 75% chance for creating a new car, which can be manipulated by
    changing the value of CAR_GENERATION_PROBABILITY to another number between 0 and 1.

    :return: None
    """

    Session = sessionmaker(bind=engine)
    session = Session()

    data = load_test_data("/workspaces/85111694/project/test_data.json")
    users = data.get("users", [])
    brand_names = data.get("brands", [])
    brand_models = data.get("models", {})

    for user in users:
        existing_user = session.query(User).filter_by(email=user["email"]).first()
        if existing_user is None:
            new_user = User(
                first_name=user["first_name"],
                last_name=user["last_name"],
                email=user["email"],
                password=user["password"],
                ip_address=user["ip_address"],
                is_signed_out=user["is_signed_out"],
                last_used=parse_datetime(user["last_used"]),
                is_admin=user["email"].endswith("@admin.com"),
                balance=user["balance"],
            )
            session.add(new_user)

    for brand_name in brand_names:
        brand = session.query(Brand).filter_by(name=brand_name).first()
        if not brand:
            brand = Brand(name=brand_name)
            session.add(brand)
            session.commit()

        for model_name in brand_models.get(brand_name, []):
            model = session.query(Model).filter_by(name=model_name, brand=brand).first()
            if not model:
                model = Model(name=model_name, brand=brand)
                session.add(model)

    # Add cars for most of the models, avoiding duplicates
    for brand_name in brand_names:
        brand = session.query(Brand).filter_by(name=brand_name).one()
        model_names = brand_models.get(brand_name, [])

        for model_name in model_names:
            model = session.query(Model).filter_by(name=model_name, brand=brand).one()

            existing_cars = session.query(Car).filter_by(model=model).all()

            if not existing_cars and random.random() < CAR_GENERATION_PROBABILITY:
                price = generate_random_price()
                amount = generate_random_amount()
                car = Car(brand=brand, model=model, price=price, amount=amount)
                session.add(car)

    session.commit()

    print("All data has been regenerated")


def regenerate_db():
    drop_db()
    print("All tables have been deleted.")
    Base.metadata.create_all(engine)
    print("All tables have been created.")
    add_test_data()
    print("Data has been generated and inserted")


if __name__ == "__main__":
    main()

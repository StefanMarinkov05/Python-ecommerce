from sqlalchemy.orm import sessionmaker
from .create_tables import Base, engine


def main():
    drop_db()


def drop_db():
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        Base.metadata.drop_all(engine)
        print("All tables have been dropped.")
    finally:
        session.close()


if __name__ == "__main__":
    main()

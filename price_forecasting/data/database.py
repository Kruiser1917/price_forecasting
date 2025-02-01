from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///price_forecast.db"

Base = declarative_base()


class PriceData(Base):
    __tablename__ = "price_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=False)
    add_cost = Column(Float, nullable=False)
    company = Column(String, nullable=False)
    product = Column(String, nullable=False)


def get_engine():
    return create_engine(DATABASE_URL, echo=False)


def create_tables():
    engine = get_engine()
    Base.metadata.create_all(engine)


def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()


def insert_data(data_list):
    """
    Сохранение списка данных в БД.
    data_list - список словарей с ключами ['price', 'count', 'add_cost', 'company', 'product'].
    """
    session = get_session()
    try:
        for data in data_list:
            record = PriceData(
                price=float(data["price"]),
                count=int(data["count"]),
                add_cost=float(data["add_cost"]),
                company=data["company"],
                product=data["product"]
            )
            session.add(record)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def fetch_all_data():
    session = get_session()
    try:
        return session.query(PriceData).all()
    finally:
        session.close()

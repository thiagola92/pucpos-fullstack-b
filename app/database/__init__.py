import click
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.accounts import Account
from app.database.persons import Person
from app.database.addresses import Address
from app.database.properties import Property
from app.database.property_owners import PropertyOwner

directory = Path("./instance")
directory.mkdir(exist_ok=True)

engine = create_engine(f"sqlite:///{directory}/app.db")
DatabaseSession = sessionmaker(bind=engine)


def close_db(e=None):
    engine.dispose()


def init_db():
    Account.metadata.drop_all(engine)
    Address.metadata.drop_all(engine)
    Person.metadata.drop_all(engine)
    Property.metadata.drop_all(engine)
    PropertyOwner.metadata.drop_all(engine)

    Account.metadata.create_all(engine)
    Address.metadata.create_all(engine)
    Person.metadata.create_all(engine)
    Property.metadata.create_all(engine)
    PropertyOwner.metadata.create_all(engine)


@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Database initialized.")

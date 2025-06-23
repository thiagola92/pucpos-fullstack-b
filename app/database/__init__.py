import click
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

from app.database.plans import Plan
from app.database.types import Type
from app.database.accounts import Account
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
    Plan.metadata.drop_all(engine)
    Type.metadata.drop_all(engine)
    Account.metadata.drop_all(engine)
    Address.metadata.drop_all(engine)
    Property.metadata.drop_all(engine)
    PropertyOwner.metadata.drop_all(engine)

    Plan.metadata.create_all(engine)
    Type.metadata.create_all(engine)
    Account.metadata.create_all(engine)
    Address.metadata.create_all(engine)
    Property.metadata.create_all(engine)
    PropertyOwner.metadata.create_all(engine)

    # Create fake data.
    with DatabaseSession() as s:
        accounts = [
            Account(
                email="asdf@asdf.com",
                password=generate_password_hash("asdf"),
            ),
            Account(
                email="asdf1@asdf.com",
                password=generate_password_hash("asdf"),
            ),
        ]

        s.add_all(accounts)
        s.commit()

        addresses = [
            Address(
                country="Brasil",
                state="RJ",
                city="Rio de Janeiro",
                street="Av. Padre Leonel Franca",
                house_number=20,
            ),
            Address(
                country="Brasil",
                state="RJ",
                city="Rio de Janeiro",
                street="R. Marquês de São Vicente",
                house_number=25,
            ),
            Address(
                country="Brasil",
                state="RJ",
                city="Rio de Janeiro",
                street="R. Artur Araripe",
                house_number=30,
            ),
            Address(
                country="Brasil",
                state="RJ",
                city="Rio de Janeiro",
                street="R. Gen. Rabêlo",
                house_number=30,
            ),
            Address(
                country="Brasil",
                state="RJ",
                city="Rio de Janeiro",
                street="R. Manuel Ferreira",
                house_number=35,
            ),
            Address(
                country="Brasil",
                state="RJ",
                city="Rio de Janeiro",
                street="Av. Rodrigo Otávio",
                house_number=40,
            ),
        ]

        s.add_all(addresses)
        s.commit()

        plans = [
            Plan(
                id=1,
                action="Vender",
            ),
            Plan(
                id=2,
                action="Alugar",
            ),
        ]

        s.add_all(plans)
        s.commit()

        types = [
            Type(
                id=1,
                name="Casa",
            ),
            Type(
                id=2,
                name="Apartamento",
            ),
        ]

        s.add_all(types)
        s.commit()

        properties = [
            Property(
                address_id=addresses[0].id,
                price=100000000,
                plan_id=1,
                type_id=1,
                photo="template_house_0.svg",
            ),
            Property(
                address_id=addresses[1].id,
                price=100000099,
                plan_id=1,
                type_id=2,
                photo="template_house_1.svg",
            ),
            Property(
                address_id=addresses[2].id,
                price=200000000,
                plan_id=1,
                type_id=2,
                photo="template_house_2.svg",
            ),
            Property(
                address_id=addresses[3].id,
                price=250050099,
                plan_id=1,
                type_id=1,
                photo="template_house_3.svg",
            ),
            Property(
                address_id=addresses[4].id,
                price=50000000,
                plan_id=1,
                type_id=1,
                photo="template_house_4.svg",
            ),
            Property(
                address_id=addresses[5].id,
                price=500,
                plan_id=2,
                type_id=1,
                photo="template_house_5.svg",
            ),
        ]

        s.add_all(properties)
        s.commit()

        property_owneres = [
            PropertyOwner(
                account_id=accounts[0].id,
                property_id=properties[0].id,
            ),
            PropertyOwner(
                account_id=accounts[0].id,
                property_id=properties[1].id,
            ),
            PropertyOwner(
                account_id=accounts[0].id,
                property_id=properties[2].id,
            ),
            PropertyOwner(
                account_id=accounts[0].id,
                property_id=properties[3].id,
            ),
            PropertyOwner(
                account_id=accounts[0].id,
                property_id=properties[4].id,
            ),
            PropertyOwner(
                account_id=accounts[1].id,
                property_id=properties[5].id,
            ),
        ]

        s.add_all(property_owneres)
        s.commit()


@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Database initialized.")

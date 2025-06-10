import click
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.accounts import Account

directory = Path("./instance")
directory.mkdir(exist_ok=True)

engine = create_engine(f"sqlite:///{directory}/app.db")
DatabaseSession = sessionmaker(bind=engine)


def close_db(e=None):
    engine.dispose()


def init_db():
    Account.metadata.drop_all(engine)
    Account.metadata.create_all(engine)


@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Database initialized.")

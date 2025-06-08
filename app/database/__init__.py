from datetime import datetime
from pathlib import Path

import sqlite3
import click
from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )

        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db_dir = Path(current_app.root_path).joinpath("database")

    for path in db_dir.iterdir():
        if not path.is_file() or not path.name.endswith(".sql"):
            continue

        with current_app.open_resource(path) as f:
            db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Database initialized.")


sqlite3.register_converter(
    "timestamp",
    lambda v: datetime.fromisoformat(v.decode()),
)

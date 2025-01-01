"""App to show silhouettes of pokemon."""

from __future__ import annotations

import json
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)

SILHOUETTE_FOLDER = Path("static") / "silhouettes"
NAME_TO_NUMBER_FILE = Path("name_to_number.json")
NUMBER_TO_NAME_FILE = Path("number_to_name.json")

with NAME_TO_NUMBER_FILE.open("r") as file:
    name_to_number = json.load(file)

with NUMBER_TO_NAME_FILE.open("r") as file:
    number_to_name = json.load(file)


def get_silhouette_path(number: int | None) -> str | None:
    """Get the silhouette path for a given number.

    Args:
        number: The number to get the silhouette path for.

    Returns:
        The path to the silhouette image or None if the number is not found.

    """
    if number is None:
        return None

    full_path = SILHOUETTE_FOLDER / f"{number:03d}.png"
    return str(full_path) if full_path.exists() else None


def get_number_and_name(query: str | None) -> tuple[int | None, str | None]:
    """Get the number and name for a given query.

    It will return None, None if the number or name is not found.

    Args:
        query: The query to get the number and name for.

    Returns:
        A tuple of the number and name.

    """
    if query is None:
        return None, None

    query = query.lower()
    if query.isdigit():
        app.logger.debug("Query is a number")
        number = int(query)
        name = number_to_name.get(str(number), None)
    else:
        app.logger.debug("Query is not a number")
        number = name_to_number.get(query, None)
        name = query

    if name is None or number is None:
        app.logger.debug("Name or number is None")
        return None, None
    app.logger.debug("Number: %s, Name: %s", number, name)
    return number, name


@app.route("/", methods=["GET"])
def index() -> str:
    """Return the index page."""
    query = request.args.get("query")
    number, name = get_number_and_name(query)
    silhouette_path = get_silhouette_path(number)

    return render_template(
        "index.html",
        silhouette=silhouette_path,
        query=query,
        number=number,
        name=name,
    )

import re


def _split_items(field):
    if not field:
        return []
    if isinstance(field, list):
        return [str(x).strip() for x in field if str(x).strip()]
    parts = re.split(r"[\n;,]+", str(field))
    return [p.strip() for p in parts if p.strip()]


def generate_portfolio(user_data):
    """Return a structure suitable for rendering a simple portfolio.

    The front end template can iterate over the dictionary.
    """
    portfolio = {
        "name": user_data.get("name", ""),
        "photo": user_data.get("photo", ""),
        "skills": _split_items(user_data.get("skills")),
        "projects": _split_items(user_data.get("projects")),
        "about": user_data.get("about", ""),
        "theme": user_data.get("theme", "default"),
    }
    return portfolio


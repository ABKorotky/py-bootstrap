DESCRIPTION = "Provides bootstrapping for Python packages based on tox tool."

CONTEXT = {
    "name": None,
    "dir_name": None,
    "title": None,
    "description": None,
    "repo": None,
    "python_major": "3",
    "python_minor": "13",
    "author": None,
    "author_email": None,
    "year": None,
    "first_version_date": None,
}

CONTEXT_REQUIRED_KEYS = [
    "name",
    "description",
    "author",
    "author_email",
]


def validate_context(context: dict[str, str]) -> bool:
    for key in CONTEXT_REQUIRED_KEYS:
        if not context.get(key):
            raise ValueError(f"Missing required context key: {key}")
    return True


def prepare_context(context: dict[str, str]):
    import re
    from datetime import datetime

    name = context["name"]
    name_parts: list[str] = re.split("[-_ ]", name.strip())

    context["empty"] = ""

    if not context.get("Name"):
        val = "".join(part.title() for part in name_parts)
        context["Name"] = val

    if not context.get("NAME"):
        val = "_".join(part.upper() for part in name_parts)
        context["NAME"] = val

    if not context.get("dir_name"):
        val = "_".join(name_parts)
        context["dir_name"] = val

    if not context.get("title"):
        val = " ".join(part.title() for part in name_parts)
        context["title"] = val

    if not context.get("year"):
        context["year"] = str(datetime.now().year)

    if not context.get("first_version_date"):
        context["first_version_date"] = datetime.now().strftime("%Y-%m-%d")

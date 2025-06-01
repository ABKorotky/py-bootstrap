DESCRIPTION = "Generates a skeleton of Python application based on tox tool."

CONTEXT: dict[str, str] = {
    "name": "",
    "dir_name": "",
    "title": "",
    "description": "",
    "repo": "",
    "python_major": "3",
    "python_minor": "13",
}

CONTEXT_REQUIRED_KEYS: list[str] = [
    "name",
    "description",
]


def validate_context(context: dict[str, str]) -> bool:
    for key in CONTEXT_REQUIRED_KEYS:
        if not context.get(key):
            raise ValueError(f"Missing required context key: {key}")
    return True


def prepare_context(context: dict[str, str]):
    import re
    from datetime import datetime

    context["empty"] = ""

    name = context["name"]
    name_parts: list[str] = re.split("[-_ ]", name.strip())

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

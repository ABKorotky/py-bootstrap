DESCRIPTION = "Describes the test bootstrap."

CONTEXT = {
    "key": None,
    "key2": None,
    "key_dir": None,
    "error": None,
}

CONTEXT_REQUIRED_KEYS = ["key"]


def validate_context(context: dict[str, str]) -> bool:
    for key in CONTEXT_REQUIRED_KEYS:
        if not context.get(key):
            raise ValueError(f"Missing required context key: {key}")
    return True


def prepare_context(context: dict[str, str]):
    key = context["key"]
    if not context.get("key2"):
        context["key2"] = f"computed value based on {key}"

    if not context.get("key_dir"):
        context["key_dir"] = f"{key}.d"

    if context.get("error"):
        raise ValueError(f"Context error: {context['error']}")

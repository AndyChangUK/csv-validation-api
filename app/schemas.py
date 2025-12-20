def parse_rules(rule_string: str):
    """
    Converts rule strings like:
    'email|required|min:5'
    into a dictionary the validator can understand.
    """
    rules = rule_string.split("|")
    parsed = {}

    for rule in rules:
        if ":" in rule:
            key, value = rule.split(":", 1)
            parsed[key] = value
        else:
            parsed[rule] = True

    return parsed

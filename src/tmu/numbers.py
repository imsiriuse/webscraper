import re


def isnumber(text):
    result = False
    if re.match("^[0-9]+$", text):
        result = True
    if re.match("^[0-9]+\\.[0-9]+$", text):
        result = True
    if re.match("^[0-9]+,[0-9]+$", text):
        result = True
    if re.match("^[0-9]+\\\\[0-9]+$", text):
        result = True
    if re.match("^[0-9]+/[0-9]+$", text):
        result = True
    if re.match("^[0-9]+e-?[0-9]+$", text):
        result = True
    if re.match("^[0-9]+\\^10-?[0-9]+$"):
        result = True
    return result


def tonumber(text):
    if re.match("^[0-9]+$", text):
        return int(text)
    if re.match("^[0-9]+\\.[0-9]+$", text):
        return float(text)
    if re.match("^[0-9]+,[0-9]+$", text):
        return float(text.replace(",", "."))
    if re.match("^[0-9]+e-?[0-9]+$", text):
        return float(text)
    if re.match("^[0-9]+/[0-9]+$", text):
        groups = re.search("^([0-9]+)/([0-9]+)$", text)
        return int(groups.group(1)) / int(groups.group(2))
    if re.match("^[0-9]+\\\\[0-9]+$", text):
        groups = re.search("^([0-9]+)\\\\([0-9]+)$", text)
        return int(groups.group(1)) / int(groups.group(2))
    if re.match("^[0-9]+\\^10-?[0-9]+$"):
        return float(text.replace("^10", "e"))

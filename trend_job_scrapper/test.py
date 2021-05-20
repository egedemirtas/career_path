import re

a = "this is a saRmple"

if re.search(r"\bi\b", a) is not None: print("nays")

if "R" in a: print("nays")

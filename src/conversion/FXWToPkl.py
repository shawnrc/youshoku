import json
import sys

if len(sys.argv) < 2:
    print("missing path to json blob")
    exit(1)

recipes = None
with open(sys.argv[1]) as blob:
    recipes = json.load(blob)

for recipe in recipes:
    print(json.dumps(recipe))
    exit(0)

import json
import os
import sys
from typing import Any, Dict

if len(sys.argv) < 2:
    print("missing path to json blob")
    exit(1)

recipes = None
with open(sys.argv[1]) as blob:
    recipes = json.load(blob)

os.mkdir('./output')
os.chdir('./output')

def to_pkl(recipe: Dict[str, Any]) -> str:
    pkl = ""

for recipe in recipes:
    if 'X100V' in recipe['Camera']:
        filename = f'{recipe["Recipe"]}.FP1'
        with open(filename, 'w') as output:
            output.write()
    exit(0)

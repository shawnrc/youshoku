import json
import os
import re
import sys

from typing import Any, Dict

if len(sys.argv) < 2:
    print("missing path to json blob")
    exit(1)

recipes = None
with open(sys.argv[1]) as blob:
    recipes = json.load(blob)

os.makedirs('./out/bw', exist_ok=True)
os.makedirs('./out/color', exist_ok=True)

def camel_case(string: str) -> str:
    subbed = re.sub(r"(_|-)+", " ", string).title().replace(" ", "")
    return ''.join([subbed[0].lower(), subbed[1:]])

def to_pkl(recipe: Dict[str, Any]) -> str:
    grain_effect, grain_size = recipe['Grain Effect'].split()
    is_color = recipe['Color or B&W'] == 'Color'
    chrome_fx_blue = recipe['Color Chrome Effect Blue'] or "Off"

    toning: str = recipe['Toning']
    monochrome_wc = None
    monochrome_mg = None
    if toning == "0":
        monochrome_wc = 0
        monochrome_mg = 0
    elif (toning_match := re.search(r'WC (?P<WC>[+-]?\d) MG (?P<MG>[+-]?\d)', toning)):
        monochrome_wc = int(toning_match.group('WC'))
        monochrome_mg = int(toning_match.group('MG'))

    if (up_to_match := re.search(r'up to ISO (\d{3,5})', recipe['ISO'])):
        max_iso = up_to_match.group(1)
    elif (range_match := re.search(r'\d{3,5} to (\d{3,5})', recipe['ISO'])):
        max_iso = range_match.group(1)
    else:
        max_iso = "12800"

    return f"""import ".../schemas/x100VRecipe.pkl"

{camel_case(recipe['Recipe'])} = new x100VRecipe.X100VRecipe {{
    name = "{recipe['Recipe']}"
    filmSimulation = "{recipe['Film Simulation']}"{f'\nmonochromaticColorWC = {monochrome_wc}' if not is_color else ''}{f'\nmonochromaticColorMG = {monochrome_mg}' if not is_color else ''}
    grainEffect = "{grain_effect}"
    grainSize = "{grain_size}"
    colorChromeEffect = "{recipe['Color Chrome Effect']}"
    colorChromeFxBlue = "{chrome_fx_blue}"
    whiteBalance = "{recipe['White Balance']}"
    wbShiftRed = {int(recipe['WB Shift Red'])}
    wbShiftBlue = {int(recipe['WB Shift Blue'])}
    dynamicRange = "{recipe['Dynamic Range']}"
    highlight = {int(recipe['Highlight'])}
    shadow = {int(recipe['Shadow'])}
    {f'color = {int(recipe["Color"])}' if is_color else ''}
    sharpness = {int(recipe['Sharpening'])}
    noiseReduction = {int(recipe['Noise Reduction'])}
    clarity = {int(recipe['Clarity'])}
    maxIso = {max_iso}
    exposureCompensation = "{recipe['Exposure Compensation']}"

    metadata {{
        author {{
            name = "Ritchie Roesch"
            url = "https://ritchieroesch.com"
        }}
        transcriber {{
            name = "Shawn Chowdhury"
            url = "https://github.com/shawnrc"
        }}
        source = "{recipe['Recipe Website']}"
        date = "{recipe['Date']}"
    }}
}}
    """

def to_snake(string: str) -> str:
    return '_'.join([token.lower() for token in string.split()])

for recipe in recipes:
    if 'X100V' in recipe['Camera']:
        chroma = 'bw' if recipe['Color or B&W'] == 'B&W' else 'color'
        filename = f'./out/{chroma}/{to_snake(recipe["Recipe"])}.pkl'
        with open(filename, 'w+') as output:
            output.write(to_pkl(recipe))

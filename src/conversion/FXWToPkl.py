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

def to_pkl(recipe: Dict[str, Any]) -> str:
    if len((grain_spec := recipe['Grain Effect'].split())) > 1:
        grain_effect, grain_size = grain_spec
    else:
        grain_effect, grain_size = ('Off', "Small")
    is_color = recipe['Color or B&W'] in {'Color', 'Sepia'}
    chrome_fx_blue = recipe['Color Chrome Effect Blue'] or 'Off'

    dr_spec = recipe['Dynamic Range']
    dr_block = f'dynamicRange = "{dr_spec}"'
    if 'DR-P' not in dr_spec:
        dr_block += f'\n    highlight = {int(recipe['Highlight'])}\n    shadow = {int(recipe['Shadow'])}'

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

    mc_block = ''
    if monochrome_wc is not None:
        mc_block = f'\n    monochromaticColorWC = {monochrome_wc}\n    monochromaticColorMG = {monochrome_mg}'

    if 'K' in recipe['White Balance']:
        white_balance = f'whiteBalance = "Temperature"\n    wbColorTemp = {recipe['White Balance'][:-1]}'
    else:
        white_balance = f'whiteBalance = "{recipe['White Balance']}"'

    return f"""module RenderedRecipe

import ".../schemas/x100VRecipe.pkl"

recipe = new x100VRecipe.X100VRecipe {{
    name = "{recipe['Recipe']}"
    filmSimulation = "{recipe['Film Simulation']}"{mc_block}
    grainEffect = "{grain_effect}"
    grainSize = "{grain_size}"
    colorChromeEffect = "{recipe['Color Chrome Effect']}"
    colorChromeFxBlue = "{chrome_fx_blue}"
    {white_balance}
    wbShiftRed = {int(recipe['WB Shift Red'])}
    wbShiftBlue = {int(recipe['WB Shift Blue'])}
    {dr_block}{f'\n    color = {int(recipe["Color"])}' if is_color else ''}
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

def sanitize(string: str) -> str:
    return ''.join([char for char in string if char not in {'(', ')', '/', '+', "'"}])

def normalize(string: str) -> str:
    return '_'.join([sanitized.lower() for token in string.split() if (sanitized := sanitize(token))])

def has_xp5_setting(recipe: Dict[str, Any]) -> bool:
    return any(len(it) > 2 for it in (recipe['Highlight'], recipe['Shadow']))

for recipe in recipes:
    if 'X100V' in set(recipe['Camera'].split(', ')) and not has_xp5_setting(recipe):
        chroma = 'bw' if recipe['Color or B&W'] == 'B&W' else 'color'
        filename = normalize(recipe["Recipe"])
        output_path = f'./out/{chroma}/{filename}.pkl'
        with open(output_path, 'w+') as output:
            output.write(to_pkl(recipe))
        # exit(0)

from glob import glob
import os
import subprocess

dirs = ['disc', 'unit_square', 'restricted_channel', 'aggregation_quality', 'actii']
images = 'images'

txt = ''
txt += '| path | image |\n'
txt += '| ---- | ----- |\n'
for d in dirs:
    for f in glob(os.path.join(d, '*.pdf')) + glob(os.path.join(d, '*.png')):
        newf = os.path.join(images, os.path.basename(f))
        newf = os.path.splitext(newf)[0] + ".png"
        _ = subprocess.run(['convert', '-density', '300', f, newf])
        # newrow = f'<tr><td>`{f}`</td><td><img src="{newf}" height=200px/></td></tr>\n'
        newrow = f'| `{os.path.splitext(f)[0]}` | <img src="{newf}" height=200px/> |\n'
        txt += newrow
txt += ''
with open('table.txt', 'w') as f:
    f.write(txt)

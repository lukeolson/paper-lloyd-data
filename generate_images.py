from glob import glob
import os
import subprocess

dirs = ['disc', 'unit_square', 'restricted_channel', 'aggregation_quality', 'actii']
images = 'images'

txt = ''
txt += '| directory | image |\n'
txt += '| --------- | :---- |\n'
for d in dirs:
    for f in glob(os.path.join(d, '*.pdf')) + glob(os.path.join(d, '*.png')):
        newf = os.path.join(images, os.path.basename(f))
        newf = os.path.splitext(newf)[0] + ".png"
        _ = subprocess.run(['convert', '-density', '300', f, newf])
        newrow = f'| `{os.path.dirname(f)}` | <img src="{newf}" width=300px/> |\n'
        txt += newrow
txt += ''
with open('table.txt', 'w') as f:
    f.write(txt)

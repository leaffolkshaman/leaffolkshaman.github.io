from PIL import Image
import os
from numpy import asarray, frombuffer
from sys import argv
import pygal
data={}
for file in os.listdir(argv[1]):
    im = Image.open(os.path.join(argv[1],file)).convert("RGB")#
    pixels = asarray(im)
    tempdict={}
    for row in pixels:
        for pixel in row: 
            t=pixel.dtype
            pixel=pixel.tobytes()
            if pixel in tempdict:
                tempdict[pixel]+=1
            else:
                tempdict[pixel]=1
    highest = [(266, 266, 266), 0]
    for pixel in tempdict:
        number=tempdict[pixel]
        if number > highest[1]:
            highest = [frombuffer(pixel, dtype=t), number]
    data[file[0:-4]]=tuple(highest[0].tolist())
    del tempdict

style=pygal.style.Style(colors=tuple(['rgb'+str(data[i]) for i in data]))
wmap = pygal.maps.world.World(style=style)
for i in data:
    wmap.add("Biggest color in flag of "+i, {i:255})
f = open(argv[2]+".svg", "wb")
f.write(wmap.render())
f.close()

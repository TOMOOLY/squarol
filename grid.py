import sys
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
ttf="fonts/ttf/Squarol-Regular.ttf"
cmap=TTFont(ttf).getBestCmap()
chars=[chr(c) for c in sorted(cmap) if c>0x20 and c not in (0xA0,) and not (0x300<=c<0x370)]
cols=24; cell=80
rows=(len(chars)+cols-1)//cols
img=Image.new("RGB",(cols*cell,rows*cell+20),"white"); d=ImageDraw.Draw(img)
f=ImageFont.truetype(ttf,52)
for i,ch in enumerate(chars):
    x=(i%cols)*cell; y=(i//cols)*cell
    d.rectangle([x,y,x+cell-1,y+cell-1],outline=(225,225,225))
    d.text((x+10,y+8),ch,font=f,fill="black")
img.save(sys.argv[1])
print(len(chars))

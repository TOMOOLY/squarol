from PIL import Image, ImageDraw, ImageFont
ttf = "fonts/ttf/Squarol-Regular.ttf"
F = lambda s: ImageFont.truetype(ttf, s)
W, H = 2400, 1500
img = Image.new("RGB", (W, H), (14, 14, 16)); d = ImageDraw.Draw(img)
acc = (255, 92, 40); fg = (245, 242, 236); dim = (130, 128, 124)
d.text((110, 90), "SQUAROL", font=F(330), fill=fg)
d.text((118, 470), "Leaf-corner display type for logos & wordmarks", font=F(54), fill=acc)
# logo tiles
tiles = [("NOVA", acc, (14,14,16)), ("Kinetic", fg, (14,14,16)), ("VOLT.", (14,14,16), acc), ("orbit", (14,14,16), fg)]
x, y = 110, 620
for txt, bg, col in tiles:
    d.rounded_rectangle([x, y, x + 520, y + 300], radius=0, fill=bg)
    f = F(118); bw = d.textlength(txt, font=f)
    d.text((x + (520 - bw) / 2, y + 85), txt, font=f, fill=col)
    x += 550
d.text((110, 990), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", font=F(96), fill=fg)
d.text((110, 1120), "abcdefghijklmnopqrstuvwxyz", font=F(96), fill=fg)
d.text((110, 1250), "0123456789 & @ # $ % ! ? ÀÉÎÕÜ ßæø", font=F(96), fill=dim)
img.save("documentation/specimen.png")

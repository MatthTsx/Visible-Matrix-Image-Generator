from PIL import Image, ImageColor, ImageEnhance, ImageFilter
import os
import math

color2 = ImageColor.getcolor('white', "RGB")
color1 = ImageColor.getcolor('black', "RGB")
image = Image.open('Images/luffy.jpeg')

size_original = image.size
size = max(size_original[0], size_original[1])

pixels = 256
ratio = min(pixels/size_original[0], pixels/size_original[1])


image = image.resize((
    math.ceil(ratio * size_original[0]),
    math.ceil(ratio * size_original[1]),
), resample=Image.Resampling.BILINEAR)

image = image.filter(ImageFilter.FIND_EDGES)
new_sizes = image.size
mtrz_img = Image.new(mode="RGB", size=(
    new_sizes[0] * 7,
    new_sizes[1] * 7,
))

media = 0

image_final = image.copy()


zero2 = [
    [0,0,0,0,0,0,0],
    [0,0,1,1,1,0,0],
    [0,0,1,0,1,0,0],
    [0,0,1,0,1,0,0],
    [0,0,1,0,1,0,0],
    [0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0],
]
one2 = [
    [0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,1,1,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0],
]

colors = [
    ImageColor.getcolor("black","RGB"),
    ImageColor.getcolor("white","RGB")
]

def AddNumberToMatrix(mtrz_img, x, y, isZero):
    arryImg = [[]]
    if(isZero):
        arryImg = zero2
    else:
        arryImg = one2
    
    for _y in range(0, 7):
        for _x in range(0, 7):
            mtrz_img.putpixel(
                xy=(x * 7 + _x, y * 7 + _y),
                value= colors[ arryImg[_y][_x] ]
            )

    return mtrz_img

for i in range(0, int(new_sizes[0])) :
    for j in range(0, new_sizes[1]):
        pixel = image.getpixel(xy=(i,j))
        media += pixel[0] + pixel[1] + pixel[2]

media /= (new_sizes[0] * new_sizes[1])
print(media)

for i in range(0, int(new_sizes[0])) :
    for j in range(0, new_sizes[1]):
        pixel = image.getpixel(xy=(i,j))
        isZero = True
        if pixel[0] + pixel[1] + pixel[2] > media * 1.25:
            image_final.putpixel(xy=(i,j), value=color1)
            isZero = False
        else:
            image_final.putpixel(xy=(i,j), value=color2)
        mtrx_img = AddNumberToMatrix(mtrz_img, i, j, isZero)



image_final = image_final.resize((
    math.ceil(size_original[0]),
    math.ceil(size_original[1]),
), Image.Resampling.NEAREST)
image_final.show()

mtrz_img.show()
from PIL import Image, ImageColor, ImageEnhance, ImageFilter
import os
import math

color2 = ImageColor.getcolor('white', "RGB")
color1 = ImageColor.getcolor('black', "RGB")
image = Image.open('Images/luffy.jpeg')
size_original = image.size
size = max(size_original[0], size_original[1])

mtrx_img = Image.new(mode="RGB", size=(
    math.floor(256 * 15 * size_original[0] / size),
    math.ceil (256 * 15 * size_original[1] / size),
))

result = Image.new("RGBA", (size, size), (255,0,0,0))

result.paste(image, (math.floor((size - size_original[0])/2), math.floor((size - size_original[1])/2) ))
image = result

image = image.resize((256,256), resample=Image.Resampling.BILINEAR)
image = image.filter(ImageFilter.FIND_EDGES)
sizes = 256
# .resize((200,200))

media = 0

image_final = image.copy()


zero = [
    [1,1,1,1,1],
    [1,0,0,0,1],
    [1,0,1,0,1],
    [1,0,0,0,1],
    [1,1,1,1,1]
]

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

one = [
    [0,0,0,0,0],
    [0,1,1,0,0],
    [0,0,1,0,0],
    [0,1,1,1,0],
    [0,0,0,0,0]
]
colors = [
    ImageColor.getcolor("black","RGB"),
    ImageColor.getcolor("white","RGB")
]

def AddNumberToMatrix(mtrx_img, x, y, isZero):
    arryImg = [[]]
    if(isZero):
        arryImg = zero2
    else:
        arryImg = one2
    
    for _y in range(0, 7):
        for _x in range(0, 7):
            mtrx_img.putpixel(
                xy=(x * 7 + _x, y * 7 + _y),
                value= colors[ arryImg[_y][_x] ]
            )

    return mtrx_img

for i in range(0, int(sizes)) :
    for j in range(0, sizes):
        pixel = image.getpixel(xy=(i,j))
        media += pixel[0] + pixel[1] + pixel[2]
# image.filter(ImageFilter.EMBOSS)
media /= (sizes * sizes)
print(media)

for i in range(0, int(sizes)) :
    for j in range(0, sizes):
        pixel = image.getpixel(xy=(i,j))
        isZero = True
        # if sum(pixel) > 0:
        if pixel[0] + pixel[1] + pixel[2] > media * 1.25:
            image_final.putpixel(xy=(i,j), value=color1)
            isZero = False
        else:
            image_final.putpixel(xy=(i,j), value=color2)
        mtrx_img = AddNumberToMatrix(mtrx_img, i, j, isZero)



image_final = image_final.resize((size,size), Image.Resampling.NEAREST)
image_final = image_final.crop((
    math.floor((size - size_original[0])/2),
    math.floor((size - size_original[1])/2),
    math.floor(size - (size - size_original[0])/2),
    math.floor(size - (size - size_original[1])/2)
))
image_final.show()

mtrx_img.show()
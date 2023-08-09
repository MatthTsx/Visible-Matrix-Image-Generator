from PIL import Image, ImageColor, ImageFilter
import moviepy.editor as mp
from moviepy.video.fx.resize import resize
import os
import numpy as np
import math

root = os.getcwd()

name = "luf"
skip = 1
maxDuration = 10

array = [] #image's array
clip = mp.VideoFileClip(root + "/videos/"+name+".mp4")

# clip = resize(clip, height=500) n sei oq eu queria cm iss

sizes = clip.size
Square_size = max(sizes[0],sizes[1])

pixels = 256
Color1 = ImageColor.getcolor("white", "RGB")
Color2 = ImageColor.getcolor("black", "RGB")

print(sizes)

media = 0
def setFilter(c, media):
    image = Image.fromarray(c)
    image_size = image.size
    prefered_size = max(image_size[0], image_size[1])
    mtx_img = Image.new(mode="RGB", size=(
        math.floor(256 * 5 * image_size[0] / prefered_size),
        math.floor(256 * 5 * image_size[1] / prefered_size),
    ))

    new_img = Image.new("RGB", (prefered_size, prefered_size), (69,69,69))
    new_img.paste(image, (
        math.floor( (prefered_size - image_size[0]) / 2),
        math.floor( (prefered_size - image_size[1]) / 2),
    ))

    image = new_img.copy()
    image = image.resize((pixels, pixels), Image.Resampling.BILINEAR)
    image = image.filter(ImageFilter.FIND_EDGES)

    # media = 0

    if(media == 0):
        for i in range(0, pixels):
            for j in range(0, pixels):
                pixel = image.getpixel(xy = (i,j))
                media += pixel[0] + pixel[1] + pixel[2]
        media /= (pixels * pixels)

    for i in range(0, pixels):
        for j in range(0,pixels):
            pixel = image.getpixel(xy = (i,j))
            isZero = True # black
            if(pixel[0] + pixel[1] + pixel[2] > media):
                image.putpixel(xy = (i,j), value=Color1)
                isZero = False # white
            else:
                image.putpixel(xy = (i,j), value=Color2)
            mtx_img = AddNumberToMatrix(mtx_img, i, j, isZero)

    image = image.resize((prefered_size, prefered_size), Image.Resampling.NEAREST)
    image = image.crop((
        math.floor((prefered_size - image_size[0])/2),
        math.floor((prefered_size - image_size[1])/2),
        math.floor(prefered_size - (prefered_size - image_size[0])/2),
        math.floor(prefered_size - (prefered_size - image_size[1])/2)
    ))
    return image, 2

zero = [
    [0,0,0,0,0],
    [0,1,1,1,0],
    [0,1,0,1,0],
    [0,1,1,1,0],
    [0,0,0,0,0]
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
        arryImg = zero
    else:
        arryImg = one
    
    for _y in range(0, 4):
        for _x in range(0, 4):
            mtrx_img.putpixel(
                xy=(x + _x, y + _y),
                value= colors[ arryImg[_y][_x] ]
            )

    return mtrx_img

def GetFrames(times, imgdir):
    if not os.path.exists(imgdir):
        os.makedirs(imgdir)

    for t in range(1, times, skip):
        c = clip.get_frame(1/clip.fps * t)
        img, mtx_img = setFilter(c,media)
        array.append(np.asarray(img))
        print(int(t/skip)," / ", int(times/skip),",                                  no skip: ", times)

    newClip = mp.ImageSequenceClip(array, fps=clip.fps / skip)
    newClip.write_videofile(imgdir+ "/" +name+".mp4")


GetFrames(int(clip.fps * min(clip.duration, maxDuration)), root + "/videoResult")


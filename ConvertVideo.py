from PIL import Image, ImageColor, ImageFilter
import moviepy.editor as mp
from moviepy.video.fx.resize import resize
import os
import numpy as np
import math

root = os.getcwd()

FileInputName = "frog"
FileName = "frog3"

skip = 1
maxDuration = 60 * 60 #max duration (seconds)

VideoArray = [] #image
Video2Array= [] #Matriz
clip = mp.VideoFileClip(root + "/videos/"+FileInputName+".mp4")

# clip = resize(clip, height=500) n sei oq eu queria cm iss
sizes = clip.size

pixels = 256 / 2
ratio = min(pixels / sizes[0], pixels / sizes[1])

Color2 = ImageColor.getcolor("white", "RGB")
Color1 = ImageColor.getcolor("black", "RGB")

print(sizes)

media = 0
def setFilter(c): #Image creator
    image = Image.fromarray(c)

    image = image.resize((
        math.ceil(ratio * sizes[0]),
        math.ceil(ratio * sizes[1]),
    ), Image.Resampling.BILINEAR)
    image = image.filter(ImageFilter.FIND_EDGES)
    new_size = image.size

    mtz_img = Image.new(mode="RGB", size=(
        new_size[0] * 7, #7 = Zero || One length
        new_size[1] * 7,
    ))

    setAvg_Media(new_size, image)

    for i in range(0, new_size[0]):
        for j in range(0,new_size[1]):
            pixel = image.getpixel(xy = (i,j))
            isZero = True # white
            if(pixel[0] + pixel[1] + pixel[2] > media):
                image.putpixel(xy = (i,j), value=Color1)
                isZero = False # black
            else:
                image.putpixel(xy = (i,j), value=Color2)
            mtz_img = AddNumberToMatrix(mtz_img, i, j, isZero)

    image = image.resize((
        sizes[0],
        sizes[1]
    ), Image.Resampling.NEAREST)
    return image, mtz_img

def setAvg_Media(new_size, image):
    global media
    if(media == 0):
        for i in range(0, new_size[0]):
            for j in range(0, new_size[1]):
                pixel = image.getpixel(xy = (i,j))
                media += pixel[0] + pixel[1] + pixel[2]
        media /= (new_size[0] * new_size[1])

zero = [
    [0,0,0,0,0,0,0],
    [0,0,1,1,1,0,0],
    [0,0,1,0,1,0,0],
    [0,0,1,0,1,0,0],
    [0,0,1,0,1,0,0],
    [0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0],
]
one = [
    [0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,1,1,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0],
]

colors = [
    ImageColor.getcolor("white","RGB"),
    ImageColor.getcolor("black","RGB"),
]

def AddNumberToMatrix(mtrz_img, x, y, isZero): #Matriz-Image creator
    arryImg = [[]]
    if(isZero):
        arryImg = zero
    else:
        arryImg = one
    
    for _y in range(0, 7):
        for _x in range(0, 7):
            mtrz_img.putpixel(
                xy=(x * 7 + _x, y * 7 + _y),
                value= colors[ arryImg[_y][_x] ]
            )

    return mtrz_img

def GetFrames(times, imgdir):
    if not os.path.exists(imgdir):
        os.makedirs(imgdir)

    for t in range(1, times, skip):
        c = clip.get_frame(1/clip.fps * t)
        img, mtz_img = setFilter(c)
        VideoArray.append(np.asarray(img))
        Video2Array.append(np.asarray(mtz_img))
        print(int(t/skip)," / ", int(times/skip),"                                  no skip: ", times)

    newClip = mp.ImageSequenceClip(VideoArray, fps=clip.fps / skip)
    newClip.write_videofile(imgdir+ "/" +FileName+".mp4")

    newMatrizClip = mp.ImageSequenceClip(Video2Array, fps=clip.fps / skip)
    newMatrizClip.write_videofile(imgdir+ "/" +FileName+"-Matriz.mp4")


GetFrames(int(clip.fps * min(clip.duration, maxDuration)), root + "/videoResult")
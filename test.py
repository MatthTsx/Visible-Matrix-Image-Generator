import moviepy.editor as mp
import os
import pygame

clip = mp.VideoFileClip(os.getcwd() + "/videoResults")

clip.preview()

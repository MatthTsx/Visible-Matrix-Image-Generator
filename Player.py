import moviepy.editor as mp
import os
import pygame

clip = mp.VideoFileClip(os.getcwd() + "/videoResult/sponge-Matriz.mp4")

clip.preview()

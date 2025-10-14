#ASCII STARS test (this time its black and white so it will show text better)

#importing libraries
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

#defining ASCII characters (light to dark) and width of output
ASCII_CHARS = "@%#*+=-:. " 
WIDTH = 100

#function to convert each frame to ASCII
def frame_to_ascii(frame):
    #convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

     #resize frame based on aspect ratop
    height, width = gray.shape
    aspect_ratio = height / width
    new_height = int(aspect_ratio * WIDTH * 0.55)
    resized = cv2.resize(gray, (WIDTH, new_height))

    #Map each pixel to an ASCII character
    ascii_frame = ""
    for row in resized:
        for pixel in row:
            index = min(int(pixel) * len(ASCII_CHARS) // 256, len(ASCII_CHARS) - 1)
            ascii_frame += ASCII_CHARS[index]
        ascii_frame += "\n"
    return ascii_frame

#function to render ASCII string to image
def ascii_to_image(ascii_str, font_path="cour.ttf", font_size=10, image_size=(800, 600)):
    #create a blank image
    img = Image.new("RGB", image_size, color="black")
    draw = ImageDraw.Draw(img)

    #load font
    font = ImageFont.load_default()

    # Draw ASCII text onto the image
    draw.text((10, 10), ascii_str, font=font, fill="white")
    return img

#path to input video file
video_path = "stars.mov"

#open video file
cap = cv2.VideoCapture(video_path)

#List to store ASCII frames
ascii_frames = []

#Read and convert each frame to ASCII
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    ascii_art = frame_to_ascii(frame)
    ascii_frames.append(ascii_art)

#Release video capture
cap.release()

#Setup video writer to save ASCII-rendered frames
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('asciistars_output.avi', fourcc, 10, (800, 600)) 

#Convert ASCII frames to images and write to video
for ascii_str in ascii_frames:
    img = ascii_to_image(ascii_str)
    frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    out.write(frame)

# Finalize video file
out.release()

import subprocess

#Convert AVI to MP4
subprocess.run([
    "ffmpeg", "-y", "-i", "asciistars_output.avi",
    "-c:v", "libx264", "-preset", "fast", "-crf", "23",
    "ascii_output.mp4"
])

#Preview the MP4 video automatically
subprocess.run(["open", "asciistars_output.mp4"])
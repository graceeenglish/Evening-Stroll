#Evening Stroll Project

#Importing libraries that will be used
import cv2 #Image and video processing 
from PIL import Image #Image processing (can mapipulate images)
import time  #For controlling playback speed of the final ascii art 

#ASCII Characters used (from darkest to lightest) 
ASCII_CHARS = [" ", ".", ",", ":", ";", "+", "*", "?", "S", "#", "@"]

#Resize images and convert to grayscale (grayscale allows for mapping the brightness to ASCII characters)
def get_resized_grayscale_image(frame, new_width=100): #Defining function to take in a frame and create a resized image
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) #Converting OpenCV frames to PIL Image and converting BGR to RGB before creating PIL Image to ensure correct brightness for ASCII mapping
    width, height = image.size #Getting original width and height of images using PIL’s .size
    aspect_ratio = height / width # Calculate the aspect ratio to maintain the image's proportions during resizing
    new_height = int(new_width * aspect_ratio * 0.55) #0.55 is a scaling factor to adjust for character height and spacing)
    resized_image = image.resize((new_width, new_height)) #Resize the image to the new dimensions
    grayscale_image = resized_image.convert("L")  #Convert to grayscale ("L" represents different shades of gray)
    return grayscale_image #Return to processed image

#Mapping each pixels brightness to a ASCII character (Esser50K Youtube Video tutorial explained this process and I adapted it for this proje)
def pixels_to_ascii(image):
    pixels = image.getdata() #Getting data from the images
    characters = " " #Assigning an empty string to store ASCII characters
    
    for pixel_value in pixels:#Looping each pixel in the image
        characters += ASCII_CHARS[pixel_value * len(ASCII_CHARS) // 256] #Mapping pixel value (0-255) to ASCII character 
    return characters #Return the complete ASCII string for the image

#This is the main function where the code converts the video to ASCII to be played back in the terminal
def convert_video_to_ascii(video_path): 
    cap = cv2.VideoCapture(video_path) #Capture video from specified path
    if not cap.isOpened(): #Checking if the video opened successfully
        print("Error: Could not open video.") 
        return #Exit the function if video can't be opened

    import os #Importing os to clear terminal
    os.system('cls' if os.name == 'nt' else 'clear') #Clear the terminal screen before playing ASCII

    while True: #Read each frame of the video
        success, frame = cap.read() #Reading the frame
        if not success: #If no more frames to read = break the loop 
            break

        resized_image = get_resized_grayscale_image(frame) #Resize and convert to grayscale
        ascii_frame = pixels_to_ascii(resized_image) #Convert pixels to ASCII characters
        width = resized_image.width #Get the width of the resized image 

        print(f"\033[{resized_image.height}A", end="") #Move the cursor up to write over the previous ASCII frame
        for i in range(0, len(ascii_frame), width): #Print each line of the ASCII frame
            print(ascii_frame[i:i+width]) #Printing the ASCII characters line by line

        time.sleep(0.01) #Controling the playback speed (0.01 is showing 100 frames per second )

    cap.release() #Release the video capture object
    print("Video Finished... I hope you had a nice evening stroll!.") #Print fuction used to show that the video has finished playing

#Running the main function
if __name__ == "__main__": #if = block runs only when the script is executed directly, not when imported
    video_path = "eveningstroll.mp4" #Path to the video file
    convert_video_to_ascii(video_path) #Calling the main function to convert the video to ASCII
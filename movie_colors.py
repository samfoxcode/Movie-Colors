import cv2
import numpy
import os
from PIL import Image, ImageDraw

def get_frames_and_color(videopath):
    vidcap = cv2.VideoCapture(videopath)
    success,image = vidcap.read()
    count = 0
    success = True
    color_array = []

    while success:
        cv2.imwrite("frame%d.jpg" % count, image) # save frame as JPEG     
        success,image = vidcap.read()
        print('Read a new frame: ', success)
        myimg = cv2.imread("frame%d.jpg" % count) # read frame
        avg_color_per_row = numpy.average(myimg, axis=0) # get average per row
        avg_color = numpy.average(avg_color_per_row, axis=0) # get average for whole image
        color_array.append(reversed(avg_color.astype(int)))
        try:
            os.remove("frame%d.jpg" % count)
        except OSError:
            pass
        count += 1

    return color_array

if __name__ == '__main__':
    movie = input("Enter .mp4 name here (Ex. movie.mp4): ") # take in movie name
    colors = get_frames_and_color(movie)

    finalImage = Image.new("RGB", (len(colors), 650)) # create blank canvas
    finalImageDraw = ImageDraw.Draw(finalImage)
    count = 0
    for i in colors:
        finalImageDraw.line([(count, 0), (count, 1000)], fill=tuple(i)) # draw colors onto canvas
        count = count + 1
    finalImage.save(os.path.splitext(movie)[0] + "_avgcolor_spectrum.PNG")

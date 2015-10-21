from PIL import Image
import math

def getAngle(x, y): #Gets the angle of any pixel in the new image (in reference to its center)
                    #the coordinates have to be adjusted so that the center of the picture would be the origin
                    #this is done in main, or whatever
  y=-y
  p=math.sqrt( math.pow(x, 2) + math.pow(y, 2) )

  if x<0 and y<0:
    angle = math.degrees( math.asin(-x/p) )
  elif x<0 and y>0:
    angle = 90 + math.degrees( math.asin(y/p) )
  elif x>0 and y>0:
    angle = 180 + math.degrees( math.asin(x/p) )
  elif x>0 and y<0:
    angle = 270 + math.degrees( math.asin(-y/p) )
  elif y==0 and x<0:
    angle = 90
  elif x==0 and y>0:
    angle = 180
  elif y==0 and x>0:
    angle = 270
  else:
    angle=0
  return angle


def getColorAtAngle(angle, image1, radius): #Returns a list of RGB colors for each angle and radius
                                           #Parameters: "angle" of pixel from the new image, the original image, and the
                                           # radius is the distance of the pixel from the center of the new image

                                           ##This function works, but it might be the reason why the images come out aliased
                                           #also this function sometimes causes the program to crash when it calls pixels that
                                           #dont exist.


  width, height = image1.size
  circumference  = 2*math.pi*radius
  if radius==0: #might need to change?
    circumference=1
  count=0
  aveRed = 0
  aveBlue = 0
  aveGreen = 0
  magicPoint = round(angle * width/360 + width/720, 0) #magicPoint is supposed to be the point on the original pic that the
                                                     #angle and radius of the point should represent
  r=radius
  if r >= height:#to be fixed later. This helps the program not crash.
      r = height - 1
  r, g, b  = image1.getpixel((magicPoint, r)) #pixel call that sometimes causes crashes
  aveGreen += g #split(pixel)
  aveRed += r
  aveBlue += b
  arr = [aveRed, aveGreen, aveBlue]
  return arr


#I guess this is the "main" part of the program

canvas = Image.new('RGB', (250, 250)) #This is the size of the new image.
file = 'small.jpg'
panorama = Image.open(file)
#pixels = list(canvas.getdata())

#for pixel in pixels:
output = {}
for col in range(panorama.size[0]):
  for row in range(panorama.size[1]):
    pixel = panorama.getpixel((col,row))
    #value = (int, int, int)
    width, height = canvas.size

    centerY = height/2 #get the center of the new image so the radius of the pixel can be calculated
    centerX = width/2

    actualDistance = math.sqrt( math.pow(row-centerX, 2) + math.pow(col-centerY, 2) ) #gets the radius
                                                                                                      #using pythagorean theorem
    roundDown = actualDistance - actualDistance%1;
    roundUp = roundDown+1

    angle = getAngle(row-centerX, col-centerY) #getAngle() called

    color = getColorAtAngle(angle, panorama, height-roundDown) #getColorAtAngle() called
    #color ends up being a list of RGB

    r, g, b  = panorama.getpixel((row, col))

    setRed = r
    setGreen = g
    setBlue = b

  #originally I used the rounded up radius and averaged its color with the rounded down, but there was even worse aliasing than
  #there is now for some reason. Here's what the code looked like:
  #
  #color1 = getColorAtAngle(angle, panorama, getHeight(panorama)-roundDown)
  #color2 = getColorAtAngle(angle, panorama, getHeight(panorama)-roundUp)
  #setGreen(pixel, color1[1]*(actualDistance%1) + color2[1]*(1-actualDistance%1) )
  #setRed(pixel, color1[0]*(actualDistance%1)  + color2[0]*(1-actualDistance%1) )
  #setBlue(pixel, color1[2]*(actualDistance%1)  + color2[2]*(1-actualDistance%1) )


  panorama.show()


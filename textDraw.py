#!usr/bin/env python  
#coding=utf-8  


#import random
#import sys

def getDrawing(negative):
# Get position of every non space or line feed in a txt
# Returns a nested list of every position in which there is an element for each line
  points=[]
  for i, line in enumerate(negative.readlines()):
    points.append([])
    for j, char in enumerate(line):
      if char!=" " and char!="\n":   
        points[i].append(j)
  return points

def alignDraw(points, maxLineChars):
  # Put all spaces in a line
  pointLine=[]
  for line, linePoints in enumerate(points):
    for point in linePoints:
      pointLine.append(point+line*maxLineChars)
  return pointLine

def readBook(book):
# Returns all lines in the book in a list of strings with some formatting
  lines=""
  # Remove \n
  for line in book.readlines():
    line = line.strip("\n")
    lines +=(str(line)+" ")
  # Remove double spacings and others
  lines = lines.replace("'","")
  lines = lines.replace('"',"")
  lines = lines.replace("***","")
  lines = lines.replace("	","")  # tab
  lines = lines.replace("a.m.","am")
  lines = lines.replace("A.M.","am")
  lines = lines.replace("p.m.","pm")
  lines = lines.replace("P.M.","pm")
  lines = lines.replace(")","")
  lines = lines.replace("(","")
  #lines = lines.replace("!","")
  #lines = lines.replace("?"," ")
  lines = lines.replace("...",".")
  lines = lines.replace(" .",".")
  lines = lines.replace(". ",".")
  lines = lines.replace(" . ",".")
  lines = lines.replace("0.","0,")
  lines = lines.replace("1.","1,")
  lines = lines.replace("2.","2,")
  lines = lines.replace("3.","3,")
  lines = lines.replace("4.","4,")
  lines = lines.replace("5.","5,")
  lines = lines.replace("6.","6,")
  lines = lines.replace("7.","7,")
  lines = lines.replace("8.","8,")
  lines = lines.replace("9.","9,")
  lines = lines.replace("*","")
  lines = lines.replace("  "," ")
  lines = lines.replace("   "," ")
  lines = lines.replace("    "," ")
  lines = lines.replace("...",".")
  lines = lines.replace(" .",".")
  lines = lines.replace(". ",".")

  # Separate sentences
  lines = lines.split(".")
  # Miscellaneous formatting
  for i, line in enumerate(lines):
    try:
      if line[0]==" ":
        lines[i] = "QUITA_ESPACIOS_AL_PRINCIPIO"+lines[i]
        lines[i] = lines[i].replace("QUITA_ESPACIOS_AL_PRINCIPIO,","")
        lines[i] = lines[i].replace("QUITA_ESPACIOS_AL_PRINCIPIO ","")
    except:
      pass
    if "?" not in line:
      if "!" not in line:
       lines[i] += "."
    lines[i] = lines[i].replace(" .",".")
  for i, line in enumerate(lines):
    if lines[i]==".":
      #lines[i-1] = lines[i-1]+".."
      lines.pop(i)
  for i, line in enumerate(lines):# Clear too short
    if (len(lines[i])<1):
      print lines[i]
      lines.pop(i)
	  
	 #Why is this not working??
    if ('"' in lines[i]):
      print lines[i]
      #lines.pop(i)

  return lines

def checkLine(pointLine, drawLineAux):
    # Checks spaces in drawLineAux in positions defined by pointLine
    for point in pointLine:
      #print "POINT: "+str(point)
      if len(drawLineAux)==point-1:
        #print "CRITICAL LINE LENGTH!"
        return False
      if point < len(drawLineAux): # Avoid ending phrase right before space
        if not drawLineAux[point]==" ":
          # Discard Aux and break
          #print "INVALID POINT! "+str(drawLineAux[point])
          return False
      else:
        # If not breaked till this point Aux is good
        return True
      #print "VALID POINT!"
	
def drawText(points, phrases, maxLineChars, drawing):
# Draws in drawing the design defined by spaces using the spaces in the phrases in lines, with maxLineChars characters page length
  drawLine=""
  drawLineAux=""
  notFinished=True
 
  # Align drawing points in a single line
  pointLine = alignDraw(points, maxLineChars)
  print "Number of points: "+str(len(pointLine))
  
  i=0
  endOfBookCounter=0;
  while len(drawLine)<pointLine[-1]:
    # Try adding new line until text is completed
    #drawLineAux=drawLine+random.choice(phrases)
    drawLineAux=drawLine+phrases[i]
    i+=1
    if i>len(phrases)-1:
      i=0
      endOfBookCounter+=1
	  
    if endOfBookCounter>50:
      # Start over
      endOfBookCounter=0
      return False
    #print "\n\n"
    #print drawLineAux
    if checkLine(pointLine, drawLineAux):
      #print "LINE IS VALID!"
      #phrases.pop(i)
      drawLine = drawLineAux+" "
  
  print drawLine
  print "END reached "+str(endOfBookCounter)+" times"
  #raw_input("\ndrawLine CREATED!")

  # Add line feed every maxLineChars characters
  drawText=""
  for i, char in enumerate(drawLine):
    drawText = drawText+char
    if not (i+1) % (maxLineChars):# Divisible by maxLineChars
      drawText = drawText+"\n"
  drawing.write(drawText)
  drawing.close()
  return True
    
####################  
#      MAIN:       #
####################
if __name__=="__main__":

  negative=open("model.txt")
  book=open("microserfs.txt")
  drawing = open("drawing.txt", "w")

  # Read model and book
  points = getDrawing(negative)
  phrases = readBook(book)

  # Paint model with book
  while not drawText(points, phrases, 130, drawing):
    open("drawing.txt", 'w').close()
    print "STARTING OVER!"


print "END"

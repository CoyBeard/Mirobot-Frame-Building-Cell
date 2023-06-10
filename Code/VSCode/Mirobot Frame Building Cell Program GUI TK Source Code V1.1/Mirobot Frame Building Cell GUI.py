from datetime import datetime
from this import s
from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
from tkinter import filedialog
#import numpy as np
from array import array
import os.path
import time
import math




root = Tk()

root.title('Mirobot Dynamic Timelapse GCode Generator')
root.iconbitmap('wlkataiconIcon.ico')
root.geometry('1200x900')
root.configure(background="#999999")

"""""
#root = Tk()

LoadingScreen = Toplevel()
LoadingScreen.title('Mirobot Dynamic Timelapse GCode Generator')
LoadingScreen.iconbitmap('wlkataiconIcon.ico')
LoadingScreen.geometry('1200x900')
LoadingScreen.configure(background="#999999")

#Frame Building Canvas Max Position Image
LoadingScreenImage = ImageTk.PhotoImage(Image.open('images/LoadingScreen.png'))
LoadingScreenImageLabel = Label(LoadingScreen, image = LoadingScreenImage )
LoadingScreenImageLabel.place(x=0, y=0)
LoadingScreenImageLabel.image = LoadingScreenImage

#Create Canvas
LoadingScreenCanvas = Canvas(root, width = 800, height = 600, bg = 'white')
LoadingScreenCanvas.place(x=20, y=165)
LoadingScreenImage = ImageTk.PhotoImage(Image.open('images/LoadingScreen.png'))
LoadingScreenImageLabel = Label(LoadingScreenCanvas, image = LoadingScreenImage )
LoadingScreenImageLabel.place(x=0, y=0)
LoadingScreenImageLabel.image = LoadingScreenImage


time.sleep(2) # Sleep for 2 seconds
"""""
#LoadingScreen.destroy()

"""
#TESTING
testvar = range(10,10 + 1)
print(testvar)
print(list(testvar))

"""
c = range(1,5+1)
d = range(3,9+1)

# Python program to find the common elements
# in two lists
def CommonElements(a, b):
    a_set = set(a)
    b_set = set(b)
 
    if (a_set & b_set):
        e = a_set & b_set
        #print("Common elements: " + str(e))
        return array("i", e)

    else:
        print("No common elements")
        return 'NULL'
        
#a = list(c)
#b = list(d)
# print(CommonElements(a, b)[1])



#Vars
Photos = 5;                                        #Number of photos
TimelapseLength = 60;                              #Seconds How long the timelapse will record   (TimelapseLength / Photos) - (LongestMovementTime * 2) - PickupOffset - MaterialWidthMINSpec - BuildPlatformTilt - BuildSpaceXMM  MUST BE > 0
StartPosition = [200, -100, 175, 0, 0, 0]          #X, Y, Z, A, B, C Cordinate where the first photo is taken 
EndPosition = [200, 100, 175, 0, 0, 0]             #X, Y, Z, A, B, C Cordinate where the last photo is taken 
global RestPositionJ1
global RestPositionJ2
global RestPositionJ3
global RestPositionJ4
global RestPositionJ5
global RestPositionJ6
RestPositionJ1 = StringVar()
RestPositionJ2 = StringVar()
RestPositionJ3 = StringVar()
RestPositionJ4 = StringVar()
RestPositionJ5 = StringVar()
RestPositionJ6 = StringVar()
#Set defalt Settings
RestPositionJ1.set(0)                              #J1, J2, J3, J4, J5, J6 Angle Where robot will rest in between Photos
RestPositionJ2.set(-40)
RestPositionJ3.set(60)
RestPositionJ4.set(0)
RestPositionJ5.set(-14)
RestPositionJ6.set(0)
MovementSpeed = 2000                               #0 - 2000 Speed when robot moves to position




#New
#INT
#MaterialWidth = 19;
MMtoPX = 1.7538

BuildSpaceXMM = 280
BuildSpaceYMM = 275
BuildSpaceXPX = BuildSpaceXMM * MMtoPX #505   BuildSpaceXMM * MMtoPX    Correct for 280 = 491
BuildSpaceYPX = BuildSpaceYMM * MMtoPX #492   BuildSpaceYMM * MMtoPX    Correct for 275 = 482

#DEBUGGING
print("BuildSpaceXPX= " + str(BuildSpaceXPX))
print("BuildSpaceYPX= " + str(BuildSpaceYPX))

StickInfoBoxWidth = 135
StickInfoBoxHeight = 60
StickInfoBoxCanvasWidth = 540
StickInfoBoxCanvasHeight = 300

PreviewPanelWidth = 600
PreviewPanelHeight = 600
PreviewPanelZeroXPX = 65
PreviewPanelZeroYPX = 68

PlaceXOffset = 40
PlaceYOffset = 40
PlaceZOffset = 40

#Math
global StickInfoBoxClickedOn
StickInfoBoxClickedOn = 0
StickInfoBoxColor = "#ebcda4"   ##ebcda4 = Unselected "tan" = Selected

StickPlaceXCalcPos = 0
StickPlaceZCalcPos = 0

#17.5mm vertival to horizontal offset
VerticalHorizontalOffset = 0 #17.5
HalfToolLength = 24
VerticalHorizontalOffsetA = 0
VerticalHorizontalOffsetB = -70
VerticalHorizontalOffsetC = 0


#Bolian
NewStickWindowOpen = False
calibrationPauseTaken = False
GlueApplicatorEnable = False

#Set Defalt Settings
global MaterialWidth
global GlueSetTime
global PickupPositionX
global PickupPositionY
global PickupPositionZ
global PickupPositionA
global PickupPositionB
global PickupPositionC
global FrameDropOffPositionX
global FrameDropOffPositionY
MaterialWidth = IntVar()
GlueSetTime = IntVar()
PickupZeroPositionX = IntVar()
PickupZeroPositionY = IntVar()
PickupZeroPositionZ = IntVar()
PickupZeroPositionA = IntVar()
PickupZeroPositionB = IntVar()
PickupZeroPositionC = IntVar()
BuildPlatformZeroPositionX = IntVar()
BuildPlatformZeroPositionY = IntVar()
BuildPlatformZeroPositionZ = IntVar()
BuildPlatformZeroPositionA = IntVar()
BuildPlatformZeroPositionB = IntVar()
BuildPlatformZeroPositionC = IntVar()
BuildPlatformZeroPositionA7 = IntVar()
BuildPlatformMaxPositionX = IntVar()
BuildPlatformMaxPositionY = IntVar()
BuildPlatformMaxPositionZ = IntVar()
BuildPlatformMaxPositionA = IntVar()
BuildPlatformMaxPositionB = IntVar()
BuildPlatformMaxPositionC = IntVar()
BuildPlatformMaxPositionA7 = IntVar()
FrameDropOffPositionX = IntVar()
FrameDropOffPositionY = IntVar()
MaterialWidth.set(19)
MaterialStopHeight = 20 #Distance stick needs to travel up to clear the height of the material stop
StickMinimumLength = 50 #Dual Suction Cup Tool 47mm Long
PlungeIntoStickDistance = 24 #Distance Suction Cups Plunge Into the Stick When Picking It Up
GlueSetTime.set(15)
PickupZeroPositionX.set(120.5) #138.5
PickupZeroPositionY.set(-253) #-222
PickupZeroPositionZ.set(60.5) #45.5
PickupZeroPositionA.set(0) #0
PickupZeroPositionB.set(0) #0
PickupZeroPositionC.set(90) #0
PickupPositionXOffset = 22 #Because the Zero Position is at the Edge of the Suction Cup While the Program Calls for the Middle of the Tool      24
PickupPositionYOffset = 11 #Because the Zero Position is at the Edge of the Suction Cup While the Program Calls for the Middle of the Tool
UniversalPosX = 198
UniversalPosY = 0
UniversalPosZ = 230
UniversalPosA = 0
UniversalPosB = 0
UniversalPosC = 0
GlueNeedleZeroPosX = 118 #190.5  188
GlueNeedleZeroPosY = 141 # 138 151
GlueNeedleZeroPosZ = 107.5 # 183.5 203
GlueNeedleZeroPosA = 90 #0
GlueNeedleZeroPosB = 0 #-90
GlueNeedleZeroPosC = -90 #0
GlueNeedleZeroPosD = 165
GlueNeedleInsetOffset = 7
GlueNeedleZeroPosStickEndModeXOffset = 30 # 148  -15 178.5               189 when in Stick End Mode        -14
GlueNeedleZeroPosStickEndModeYOffset = -16 # 141  -13 125
GlueNeedleZeroPosStickEndModeZOffset = 45 # 152.5  -19 164.5
GlueNeedleZeroPosStickEndModeAOffset = -90 # 0
GlueNeedleZeroPosStickEndModeBOffset = 0 # 0
GlueNeedleZeroPosStickEndModeCOffset = 90 # 0
GlueApplicationBetweenPointDelay = 0.1
BuildPlatformZeroPositionX.set(214) #224
BuildPlatformZeroPositionY.set(0)   #
BuildPlatformZeroPositionZ.set(40)  #65
BuildPlatformZeroPositionA.set(110)  #0
BuildPlatformZeroPositionB.set(-180)   #-70
BuildPlatformZeroPositionC.set(-90) #0
BuildPlatformZeroPositionA7.set(0)  #
BuildPlatformMaxPositionX.set(284)
BuildPlatformMaxPositionY.set(0)
BuildPlatformMaxPositionZ.set(261)
BuildPlatformMaxPositionA.set(110)
BuildPlatformMaxPositionB.set(-180)
BuildPlatformMaxPositionC.set(-90)
BuildPlatformMaxPositionA7.set(280)
FrameDropOffPositionX.set(0)
FrameDropOffPositionY.set(0)

#Stick Data (Stick 0 and 21 are not visible)                BuildPlatformZeroPositionX
MaxStick = 20
StickCount = 1
global StickData #"Stick0", "Length (MM)", "H", "X Position (MM)", "Y Position (MM)", 0, 0, 0, 0, 0
StickData = [  "Stick0", 0, "H", 0, 0, 0, 0, 0, 0, 0
              ,"Stick1", 0, "H", 0, 0, 0, 0, 0, 0, 1
              ,"Stick2", 0, "H", 0, 0, 0, 0, 0, 0, 2
              ,"Stick3", 0, "H", 0, 0, 0, 0, 0, 0, 3
              ,"Stick4", 0, "H", 0, 0, 0, 0, 0, 0, 4
              ,"Stick5", 0, "H", 0, 0, 0, 0, 0, 0, 5
              ,"Stick6", 0, "H", 0, 0, 0, 0, 0, 0, 6
              ,"Stick7", 0, "H", 0, 0, 0, 0, 0, 0, 7
              ,"Stick8", 0, "H", 0, 0, 0, 0, 0, 0, 8
              ,"Stick9", 0, "H", 0, 0, 0, 0, 0, 0, 9
             ,"Stick10", 0, "H", 0, 0, 0, 0, 0, 0, 10
             ,"Stick11", 0, "H", 0, 0, 0, 0, 0, 0, 11
             ,"Stick12", 0, "H", 0, 0, 0, 0, 0, 0, 12
             ,"Stick13", 0, "H", 0, 0, 0, 0, 0, 0, 13
             ,"Stick14", 0, "H", 0, 0, 0, 0, 0, 0, 14
             ,"Stick15", 0, "H", 0, 0, 0, 0, 0, 0, 15
             ,"Stick16", 0, "H", 0, 0, 0, 0, 0, 0, 16
             ,"Stick17", 0, "H", 0, 0, 0, 0, 0, 0, 17
             ,"Stick18", 0, "H", 0, 0, 0, 0, 0, 0, 18
             ,"Stick19", 0, "H", 0, 0, 0, 0, 0, 0, 19
             ,"Stick20", 0, "H", 0, 0, 0, 0, 0, 0, 20
             ,"Stick21", 0, "H", 0, 0, 0, 0, 0, 0, 21]

#Temporary array that stores a Score: Y Position Having the Highest Value, X Next Highest Value, and last Two Digits Are Reserved For What Stick Number the Stick is (In Order to Sort the Sticks by Whos the Closest to the Origin Favoring the Y Value)
StickValues = []

#Array algorithmically generated to contain all existing sticks in order based on stick score
SortedSticks = []

global DefaltStickName
DefaltStickName = StringVar()

#Horizontal or Vertical Drop Down Selection
OrentSelectOptions = [
    'Horizontal',
    'Vertical',
]

#Advanced Settings 
global PickupOffset
global BuildPlatformTilt
global MaterialWidthMINSpec
global MaterialWidthMAXSpec
global BuildPlatformWidth
global BuildPlatformHeight
PickupOffset = StringVar()               #Seconds robot waits before taking the photo so the camra isn't shaking from movement
BuildPlatformTilt = StringVar()                      #Seconds gripper holds down to trigger photo
MaterialWidthMINSpec = IntVar()                       #Seconds robot waits after trigger photo to return to rest position
MaterialWidthMAXSpec = IntVar()                       #Seconds robot waits after trigger photo to return to rest position
BuildPlatformWidth = IntVar()                   #Seconds it takes to close the gripper 
BuildPlatformHeight = IntVar()                   #Seconds it takes to close the gripper 
#Set Defalts
PickupOffset.set(10)
BuildPlatformTilt.set(0.25)
MaterialWidthMINSpec.set(5)
MaterialWidthMAXSpec.set(20)
BuildPlatformWidth.set(BuildSpaceXMM)
BuildPlatformHeight.set(BuildSpaceYMM)




#Math Vars:
StartEndCarttesianDiffrence = [0, 0, 0, 0, 0, 0]    #Diffrence of each cordinates start and end position
global PhotoDelay
PhotoDelay = 0;                                     #Rest period between photos
Photo = 0;                                          #What photo the program is on, starts at photo number 0
XStep = 0;                                          #Distance on X axis travled per photo
YStep = 0;                                          #Distance on Y axis travled per photo
ZStep = 0;                                          #Distance on Z axis travled per photo
AStep = 0;                                          #Distance on A axis travled per photo
BStep = 0;                                          #Distance on B axis travled per photo
CStep = 0;                                          #Distance on C axis travled per photo


global SetProgramName
SetProgramName = StringVar()
#Set Defalt
SetProgramName.set('Set Program Name')
    
global DirectoryChosen
DirectoryChosen = StringVar()
#Set Defalt
DirectoryChosen.set('NULL')

global Version
Version = StringVar()
#Set Defalt
Version.set('V1.0.0')

# structure to represent a co-ordinate
# point
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
def printPoints(source, l, m):
    # m is the slope of line, and the
    # required Point lies distance l
    # away from the source Point
    a = Point(0, 0)
    b = Point(0, 0)
 
    # slope is 0
    if m == 0:
        a.x = source.x + l
        a.y = source.y
 
        b.x = source.x - l
        b.y = source.y
 
    # if slope is infinite
    elif math.isfinite(m) is False:
        a.x = source.x
        a.y = source.y + l
 
        b.x = source.x
        b.y = source.y - l
    else:
        dx = (l / math.sqrt(1 + (m * m)))
        dy = m * dx
        a.x = source.x + dx
        a.y = source.y + dy
        b.x = source.x - dx
        b.y = source.y - dy
        
        #Round to 10th
        a.x = round(a.x, 1)
        a.y = round(a.y, 1)
        b.x = round(b.x, 1)
        b.y = round(b.y, 1)
 
    # print the first Point
    print(f"{a.x}, {a.y}")
    
    return (a)
 
    # print the second Point
    print(f"{b.x}, {b.y}")
    
#Sort Stick Data
def SortStickData():
    #Clear Temp Arrays
    StickValues.clear()
    SortedSticks.clear()
    
    for x in range(StickCount): #Repeat for how many sticks 
        if x > 0: #Skip Stick 0
            #For Every Stick Give it a Score: Y Position Having the Highest Value, X Next Highest Value, and last Two Digits Are Reserved For What Stick Number the Stick is (In Order to Sort the Sticks by Whos the Closest to the Origin Favoring the Y Value)
            StickValues.append((int(StickData[(x * 10) + 4]) * 100000) + (int(StickData[(x * 10) + 3]) * 100) + (int(StickData[(x * 10) + 9])))
            
        #DEBUGGING
        print(StickValues)
    
    #Sort Sticks Numericly (lowest Score to Highest Score)
    StickValues.sort()
    
    #DEBUGGING
    print(StickValues)
    
    #Write Sorted Array Based on StickValues
    for y in range(len(StickValues)): #Repeat for how many sticks 
        for x in range(10): #Write all 10 (0-9) Stick Data Values
            
            #DEBUGGING
            print("Sorted Stick Y Value")
            print(y)
            print("Sorted Stick X Value")
            print(x)
            
            #Write all 10 (0-9) Stick Data Values to SortedSticks Array
            SortedSticks.append(StickData[(int(str(StickValues[y])[-2:]) * 10) + x])
    
    #DEBUGGING
    print("Sorted Sticks Array: ")
    print(SortedSticks)
            
        

#Exicute GenerateGCode  SubStick
def GenerateGCode():
    #Error Messages 
    #Fill All Fields Errer Detection
    if len(FrameDropOffPositionXEntry.get()) == 0 or len(FrameDropOffPositionYEntry.get()) == 0 or len(GlueSetTimeEntry.get()) == 0 or len(MaterialWidthEntry.get()) == 0: #len(StickPickupZeroPositionXEntry.get()) == 0 or len(StickPickupZeroPositionYEntry.get()) == 0 or len(StickPickupZeroPositionZEntry.get()) == 0 or len(StickPickupZeroPositionAEntry.get()) == 0 or len(StickPickupZeroPositionBEntry.get()) == 0 or len(StickPickupZeroPositionCEntry.get()) == 0 or 
        messagebox.showerror('info', 'Please fill out all fields!')
    else:
        #No Sticks Errer Detection
        if StickCount <= 1:
            messagebox.showerror('info', 'No Sticks Inputted!')
        else:
            #Destination File Chosen Errer Detection
            if str(DirectoryChosen.get()) == 'NULL':
                messagebox.showerror('info', 'Please chose a destination file!')
            else:
                #One Time Calculations:
                SortStickData()
                global StickPickupZeroPositionXEntry
                calibrationPauseTaken = true #deactivated

                #Compile File Name and Address
                completeName = os.path.join(str(folder_selected), str(SetProgramName.get())+'.gcode')
                f = open(completeName, 'w')

                #Write GCode
                    
                #Defalt Title Paragraph
                f.write(';File generated by Mirobot Frame Building Cell GUI\n')
                f.write(';' + str(Version.get()) + '\n')
                f.write(";Date Generated: ") 
                f.write(str(datetime.now()))
                f.write('\n')
                f.write('\n')
                f.write('\n')

                
                #GCode
                f.write('\n')
                #Home the Robot
                f.write(';Home\n')
                f.write('$h7\n')
                #Set Feedrate
                f.write('G01 F' + str(MovementSpeedSlider.get()) + '\n')
                f.write('\n')
                
                for x in range(int(StickCount - 1)): #Repeat for how many sticks, dont include 0
                    #Stick Number
                    f.write('\n')
                    f.write(';Stick: ' + str(SortedSticks[(x * 10) + 0]) + '\n')
                    f.write('\n')
                    #Move Above Stick
                    f.write(';Move Above Stick\n')
                    f.write('M20 G90 G00' + ' X' + str(PickupZeroPositionX.get() - (int(SortedSticks[(x * 10) + 1]) / 2) + PickupPositionXOffset)
                                        + ' Y' + str(PickupZeroPositionY.get() - (int(MaterialWidthEntry.get()) / 2) + PickupPositionYOffset) 
                                        + ' Z' + str(PickupZeroPositionZ.get() + (int(MaterialWidthEntry.get()) + int(PickupOffsetEntry.get()))) 
                                        + ' A' + str(PickupZeroPositionA.get()) 
                                        + ' B' + str(PickupZeroPositionB.get()) 
                                        + ' C' + str(PickupZeroPositionC.get())
                                        + ' D' + str(BuildPlatformZeroPositionA7.get()) + '\n')
                    f.write('\n')
                    #Activate Suction Cups
                    f.write(';Activate Suction Cups\n')
                    f.write('M3S1000\n')  
                    f.write('\n')
                    #Plunge to Stick
                    f.write(';Plunge to Stick\n')
                    f.write('M20 G90 G01' + ' X' + str(PickupZeroPositionX.get() - (int(SortedSticks[(x * 10) + 1]) / 2) + PickupPositionXOffset) 
                                        + ' Y' + str(PickupZeroPositionY.get() - (int(MaterialWidthEntry.get()) / 2) + PickupPositionYOffset) 
                                        + ' Z' + str(PickupZeroPositionZ.get() + (int(MaterialWidthEntry.get()) - PlungeIntoStickDistance)) 
                                        + ' A' + str(PickupZeroPositionA.get()) 
                                        + ' B' + str(PickupZeroPositionB.get()) 
                                        + ' C' + str(PickupZeroPositionC.get())
                                        + ' D' + str(BuildPlatformZeroPositionA7.get()) + '\n')
                    f.write('\n')
                    
                    #Pause to let operator adjust the wrist to payload
                    if calibrationPauseTaken == False:
                        f.write(';Pause to let operator adjust the wrist to payload\n')
                        f.write('G4 P6'+'\n')
                        f.write('\n')
                        calibrationPauseTaken = True
                    
                    #Pickup Stick
                    f.write(';Pickup Stick\n')
                    f.write('M20 G90 G01' + ' X' + str(PickupZeroPositionX.get() - (int(SortedSticks[(x * 10) + 1]) / 2) + PickupPositionXOffset) 
                                        + ' Y' + str(PickupZeroPositionY.get() - (int(MaterialWidthEntry.get()) / 2) + PickupPositionYOffset) 
                                        + ' Z' + str(PickupZeroPositionZ.get() + (int(MaterialWidthEntry.get()) + MaterialStopHeight + int(PickupOffsetEntry.get()))) 
                                        + ' A' + str(PickupZeroPositionA.get()) 
                                        + ' B' + str(PickupZeroPositionB.get()) 
                                        + ' C' + str(PickupZeroPositionC.get())
                                        + ' D' + str(BuildPlatformZeroPositionA7.get()) + '\n')
                    f.write('\n')
                    
                    #Move to Universal Position
                    f.write(';Move to Universal Position\n')
                    f.write('M20 G90 G00' + ' X' + str(UniversalPosX) 
                                        + ' Y' + str(UniversalPosY) 
                                        + ' Z' + str(UniversalPosZ) 
                                        + ' A' + str(UniversalPosA) 
                                        + ' B' + str(UniversalPosB) 
                                        + ' C' + str(UniversalPosC)
                                        + ' D' + str(BuildPlatformZeroPositionA7.get() + 100) + '\n')
                    f.write('\n')
                    if (GlueApplicatorEnable):
                        #Check if Stick Needs Glued
                        for y in range(x):
                            #Create X and Y Range of Values For the Compairing Stick
                            if str(SortedSticks[(y * 10) + 2]) == "H":
                                #DEBUGGING  
                                print('Compairing Stick: ' + str(y) + ' is Horizontal')
                                
                                CompairingStickXValues = range(int(SortedSticks[(y * 10) + 3]), int(SortedSticks[(y * 10) + 3]) + int(SortedSticks[(y * 10) + 1]) + 1)
                                CompairingStickYValues = range(int(SortedSticks[(y * 10) + 4]), int(SortedSticks[(y * 10) + 4]) + int(MaterialWidthEntry.get()) + 1)
                                
                            if str(SortedSticks[(y * 10) + 2]) == "V":
                                #DEBUGGING  
                                print('Compairing Stick: ' + str(y) + ' is Vertical')
                                
                                CompairingStickXValues = range(int(SortedSticks[(y * 10) + 3]), int(SortedSticks[(y * 10) + 3]) + int(MaterialWidthEntry.get()) + 1)
                                CompairingStickYValues = range(int(SortedSticks[(y * 10) + 4]), int(SortedSticks[(y * 10) + 4]) + int(SortedSticks[(y * 10) + 1]) + 1)
                                
                            #Create X and Y Range of Values For the In Hand Stick
                            if str(SortedSticks[(x * 10) + 2]) == "H":
                                #DEBUGGING  
                                print('In Hand Stick: ' + str(x) + ' is Horizontal')
                                
                                InHandStickXValues = range(int(SortedSticks[(x * 10) + 3]), int(SortedSticks[(x * 10) + 3]) + int(SortedSticks[(x * 10) + 1]) + 1)
                                InHandStickYValues = range(int(SortedSticks[(x * 10) + 4]), int(SortedSticks[(x * 10) + 4]) + int(MaterialWidthEntry.get()) + 1)
                                
                            if str(SortedSticks[(x * 10) + 2]) == "V":
                                #DEBUGGING  
                                print('In Hand Stick: ' + str(x) + ' is Vertical')
                                
                                InHandStickXValues = range(int(SortedSticks[(x * 10) + 3]), int(SortedSticks[(x * 10) + 3]) + int(MaterialWidthEntry.get()) + 1)
                                InHandStickYValues = range(int(SortedSticks[(x * 10) + 4]), int(SortedSticks[(x * 10) + 4]) + int(SortedSticks[(x * 10) + 1]) + 1)
                                
                            #DEBUGGING
                            print('Compairing Stick X Values: ' + str(CompairingStickXValues))
                            print('Compairing Stick Y Values: ' + str(CompairingStickYValues))
                            print('In Hand Stick X Values: ' + str(InHandStickXValues))
                            print('In Hand Stick Y Values: ' + str(InHandStickYValues))
                            
                            #Create an Array of All the Common X Values and an Array For All the Common Y Values 
                            CommonXValues = CommonElements(CompairingStickXValues, InHandStickXValues)
                            CommonYValues = CommonElements(CompairingStickYValues, InHandStickYValues)
                            print('Common X Values: ' + str(CommonXValues)) #[1]
                            print('Common Y Values: ' + str(CommonYValues)) #[1]
                            
                            #Find Which Array (X or Y) is the Common (The Face the Glue Goes on) If Nether is the Common Then the Sticks do Not Come In Contact
                            if (len(CommonXValues) == 1):
                                #DEBUGGING
                                print('X is the Common')
                                '''
                                #Move to Universal Position
                                f.write(';Move to Universal Position\n')
                                f.write('M20 G90 G00' + ' X' + str(UniversalPosX) 
                                                    + ' Y' + str(UniversalPosY) 
                                                    + ' Z' + str(UniversalPosZ) 
                                                    + ' A' + str(UniversalPosA) 
                                                    + ' B' + str(UniversalPosB) 
                                                    + ' C' + str(UniversalPosC) + '\n')
                                f.write('\n')
                                '''
                                #If On End of Stick
                                if (str(SortedSticks[(x * 10) + 2]) == 'H'):
                                    for z in range(len(CommonYValues)):
                                        f.write(';Move Stick to Glue Point Along X Axis\n')
                                        f.write(';Point: ' + str(z) + '\n')
                                        f.write('M20 G90 G00' + ' X' + str(GlueNeedleZeroPosX + GlueNeedleZeroPosStickEndModeXOffset)
                                                            + ' Y' + str(GlueNeedleZeroPosY + GlueNeedleZeroPosStickEndModeYOffset - (int(SortedSticks[(x * 10) + 1]) / 2) + PickupPositionXOffset + GlueNeedleInsetOffset) 
                                                            + ' Z' + str(GlueNeedleZeroPosZ + GlueNeedleZeroPosStickEndModeZOffset + (int(MaterialWidthEntry.get())) + (int(SortedSticks[(x * 10) + 3]) - int(CommonYValues[z]))) #(int(MaterialWidthEntry.get()) + int(PickupOffsetEntry.get()))
                                                            + ' A' + str(GlueNeedleZeroPosA + GlueNeedleZeroPosStickEndModeAOffset) 
                                                            + ' B' + str(GlueNeedleZeroPosB + GlueNeedleZeroPosStickEndModeBOffset) 
                                                            + ' C' + str(GlueNeedleZeroPosC + GlueNeedleZeroPosStickEndModeCOffset)
                                                            + ' D' + str(GlueNeedleZeroPosD) + '\n')
                                        f.write('\n')
                                        
                                        #Delay Between Points to Slowly Apply Glue     
                                        f.write(';Delay Between Points to Slowly Apply Glue\n')
                                        f.write('G4 P' + str(GlueApplicationBetweenPointDelay) + '\n')
                                        f.write('\n')
                                
                                #If On Edge of Stick
                                if (str(SortedSticks[(x * 10) + 2]) == 'V'):
                                    #Move Stick to Glue Points
                                    for z in range(len(CommonYValues)):
                                        f.write(';Move Stick to Glue Point Along X Axis\n')
                                        f.write(';Point: ' + str(z) + '\n')
                                        f.write('M20 G90 G00' + ' X' + str(GlueNeedleZeroPosX - (int(MaterialWidthEntry.get()) / 2))
                                                            + ' Y' + str(GlueNeedleZeroPosY - (int(MaterialWidthEntry.get()) / 2) + GlueNeedleInsetOffset) 
                                                            + ' Z' + str(GlueNeedleZeroPosZ + (int(SortedSticks[(x * 10) + 1]) / 2) + (int(SortedSticks[(x * 10) + 3]) - int(CommonYValues[z]))) #(int(MaterialWidthEntry.get()) + int(PickupOffsetEntry.get()))
                                                            + ' A' + str(GlueNeedleZeroPosA) 
                                                            + ' B' + str(GlueNeedleZeroPosB) 
                                                            + ' C' + str(GlueNeedleZeroPosC)
                                                            + ' D' + str(GlueNeedleZeroPosD) + '\n')
                                        f.write('\n')
                                        
                                        #Delay Between Points to Slowly Apply Glue     
                                        f.write(';Delay Between Points to Slowly Apply Glue\n')
                                        f.write('G4 P' + str(GlueApplicationBetweenPointDelay) + '\n')
                                        f.write('\n')
                                
                            
                            if (len(CommonYValues) == 1):
                                #DEBUGGING
                                print('Y is the Common')
                                ''''
                                #Move to Universal Position
                                f.write(';Move to Universal Position\n')
                                f.write('M20 G90 G00' + ' X' + str(UniversalPosX) 
                                                    + ' Y' + str(UniversalPosY) 
                                                    + ' Z' + str(UniversalPosZ) 
                                                    + ' A' + str(UniversalPosA) 
                                                    + ' B' + str(UniversalPosB) 
                                                    + ' C' + str(UniversalPosC)
                                                    + ' D' + str(BuildPlatformZeroPositionA7.get()) + '\n')
                                f.write('\n')
                                '''
                                #If On End of Stick
                                if (str(SortedSticks[(x * 10) + 2]) == 'V'):
                                    for z in range(len(CommonXValues)):
                                        f.write(';Move Stick to Glue Point Along Y Axis\n')
                                        f.write(';Point: ' + str(z) + '\n')
                                        f.write('M20 G90 G00' + ' X' + str(GlueNeedleZeroPosX + GlueNeedleZeroPosStickEndModeXOffset)
                                                            + ' Y' + str(GlueNeedleZeroPosY + GlueNeedleZeroPosStickEndModeYOffset - (int(SortedSticks[(x * 10) + 1]) / 2) + PickupPositionXOffset + GlueNeedleInsetOffset) 
                                                            + ' Z' + str(GlueNeedleZeroPosZ + GlueNeedleZeroPosStickEndModeZOffset + (int(MaterialWidthEntry.get())) + (int(SortedSticks[(x * 10) + 3]) - int(CommonXValues[z]))) #(int(MaterialWidthEntry.get()) + int(PickupOffsetEntry.get()))
                                                            + ' A' + str(GlueNeedleZeroPosA + GlueNeedleZeroPosStickEndModeAOffset) 
                                                            + ' B' + str(GlueNeedleZeroPosB + GlueNeedleZeroPosStickEndModeBOffset) 
                                                            + ' C' + str(GlueNeedleZeroPosC + GlueNeedleZeroPosStickEndModeCOffset)
                                                            + ' D' + str(GlueNeedleZeroPosD) + '\n')
                                        f.write('\n')
                                        
                                        #Delay Between Points to Slowly Apply Glue     
                                        f.write(';Delay Between Points to Slowly Apply Glue\n')
                                        f.write('G4 P' + str(GlueApplicationBetweenPointDelay) + '\n')
                                        f.write('\n')
                                
                                #If On Edge of Stick
                                if (str(SortedSticks[(x * 10) + 2]) == 'H'):
                                    #Move Stick to Glue Points
                                    for z in range(len(CommonXValues)):
                                        f.write(';Move Stick to Glue Point Along Y Axis\n')
                                        f.write(';Point: ' + str(z) + '\n')
                                        f.write('M20 G90 G00' + ' X' + str(GlueNeedleZeroPosX - (int(MaterialWidthEntry.get()) / 2))
                                                            + ' Y' + str(GlueNeedleZeroPosY - (int(MaterialWidthEntry.get()) / 2) + GlueNeedleInsetOffset) 
                                                            + ' Z' + str(GlueNeedleZeroPosZ + (int(SortedSticks[(x * 10) + 1]) / 2) + (int(SortedSticks[(x * 10) + 3]) - int(CommonXValues[z]))) #(int(MaterialWidthEntry.get()) + int(PickupOffsetEntry.get()))
                                                            + ' A' + str(GlueNeedleZeroPosA) 
                                                            + ' B' + str(GlueNeedleZeroPosB) 
                                                            + ' C' + str(GlueNeedleZeroPosC)
                                                            + ' D' + str(GlueNeedleZeroPosD) + '\n')
                                        f.write('\n')
                                        
                                        #Delay Between Points to Slowly Apply Glue     
                                        f.write(';Delay Between Points to Slowly Apply Glue\n')
                                        f.write('G4 P' + str(GlueApplicationBetweenPointDelay) + '\n')
                                        f.write('\n')
                                    
                                else:
                                    #DEBUGGING
                                    print('No Contact')
                            
                        ''''    
                        #Place Glued Stick On Canvas  
                        if (len(CommonXValues) == 1):    
                            #If On End of Stick
                            if (str(SortedSticks[(x * 10) + 2]) == 'H'):
                                
                            #If On Edge of Stick
                            if (str(SortedSticks[(x * 10) + 2]) == 'V'):
                                
                        if (len(CommonYValues) == 1):
                            #If On End of Stick
                            if (str(SortedSticks[(x * 10) + 2]) == 'V'):
                                
                            #If On Edge of Stick
                            if (str(SortedSticks[(x * 10) + 2]) == 'H'):
                        '''
                        
                        #BuildPlatformZeroPositionX
                        
                        #Move to Universal Position
                        f.write(';Move to Universal Position\n')
                        f.write('M20 G90 G00' + ' X' + str(UniversalPosX) 
                                            + ' Y' + str(UniversalPosY) 
                                            + ' Z' + str(UniversalPosZ) 
                                            + ' A' + str(UniversalPosA) 
                                            + ' B' + str(UniversalPosB) 
                                            + ' C' + str(UniversalPosC)
                                            + ' D' + str(BuildPlatformZeroPositionA7.get() + 100) + '\n')
                        f.write('\n')
                    
                    #If Stick is Vertical
                    if (str(SortedSticks[(x * 10) + 2]) == 'V'):
                        '''
                        StickPlaceXCalcPos = math.sin((90 - math.atan((int(BuildPlatformMaxPositionZ.get()) - int(BuildPlatformZeroPositionZ.get())) / (int(BuildPlatformMaxPositionX.get()) - int(BuildPlatformZeroPositionX.get()))))) * ((int(SortedSticks[(x * 10) + 4]) + (int(SortedSticks[(x * 10) + 1]) / 2)) / math.sin(90))
                        StickPlaceZCalcPos = math.sin(90 - ((90 - math.atan((int(BuildPlatformMaxPositionZ.get()) - int(BuildPlatformZeroPositionZ.get())) / (int(BuildPlatformMaxPositionX.get()) - int(BuildPlatformZeroPositionX.get())))))) * ((int(SortedSticks[(x * 10) + 4]) + (int(SortedSticks[(x * 10) + 1]) / 2)) / math.sin(90))
                        
                        
                        #DEBUGGING
                        print("AAS Method:")
                        print(str(int(SortedSticks[(x * 10) + 4]) + (int(SortedSticks[(x * 10) + 1]) / 2)))
                        print(str(StickPlaceXCalcPos))
                        print(str(round(BuildPlatformZeroPositionX.get() + StickPlaceXCalcPos, 1)) )
                        print(str(round(BuildPlatformZeroPositionX.get() + StickPlaceXCalcPos - (math.sin(90 - (math.atan((BuildPlatformMaxPositionX.get() - BuildPlatformZeroPositionX.get()) / (BuildPlatformMaxPositionZ.get() - BuildPlatformZeroPositionZ.get())))) * (PlaceZOffset / math.sin(90))), 1)) )
                        
                        
                        # driver function
                        print("GFG Method:")
                        p = Point(int(BuildPlatformZeroPositionX.get()), int(BuildPlatformZeroPositionZ.get()))
                        #q = Point(1, 0)
                        print("Slope: " + str((int(BuildPlatformMaxPositionZ.get()) - int(BuildPlatformZeroPositionZ.get())) / (int(BuildPlatformMaxPositionX.get()) - int(BuildPlatformZeroPositionX.get()))))
                        print("Length: " + str(int(SortedSticks[(x * 10) + 4]) + (int(SortedSticks[(x * 10) + 1]) / 2)))
                        print("Point P: ("+ str(p.x) + ", " + str(p.y) + ")")
                        printPoints(p, (int(SortedSticks[(x * 10) + 4]) + (int(SortedSticks[(x * 10) + 1]) / 2)), ((int(BuildPlatformMaxPositionZ.get()) - int(BuildPlatformZeroPositionZ.get())) / (int(BuildPlatformMaxPositionX.get()) - int(BuildPlatformZeroPositionX.get()))))
                        print("\n")
                        #printPoints(q, 5, 0)
                        '''
                        p = Point(int(BuildPlatformZeroPositionX.get()), int(BuildPlatformZeroPositionZ.get()))
                        StickPlaceXCalcPos = printPoints(p, (int(SortedSticks[(x * 10) + 4]) + (int(SortedSticks[(x * 10) + 1]) / 2)), ((int(BuildPlatformMaxPositionZ.get()) - int(BuildPlatformZeroPositionZ.get())) / (int(BuildPlatformMaxPositionX.get()) - int(BuildPlatformZeroPositionX.get())))).x
                        StickPlaceZCalcPos = printPoints(p, (int(SortedSticks[(x * 10) + 4]) + (int(SortedSticks[(x * 10) + 1]) / 2)), ((int(BuildPlatformMaxPositionZ.get()) - int(BuildPlatformZeroPositionZ.get())) / (int(BuildPlatformMaxPositionX.get()) - int(BuildPlatformZeroPositionX.get())))).y
                        print("StickPlaceXCalcPos = " + str(StickPlaceXCalcPos))
                        print("StickPlaceZCalcPos = " + str(StickPlaceZCalcPos))
                        print("StickPlaceXCalcPos = " + str(StickPlaceXCalcPos))
                        print("StickPlaceZCalcPos = " + str(StickPlaceZCalcPos))
                        print("Y pos: " + str(int(SortedSticks[(x * 10) + 4])))
                        print("Half Stick Length: " + str((int(SortedSticks[(x * 10) + 1]) / 2)))
                        print("Final Y pos: " + str((int(SortedSticks[(x * 10) + 4]) + (int(SortedSticks[(x * 10) + 1]) / 2))))
                    
                        #Make sure axis D doesent colide with glue sensor LS
                        if ((round((BuildPlatformZeroPositionA7.get() + (int(SortedSticks[(x * 10) + 3]) + (int(MaterialWidth.get()) / 2) + PlaceXOffset)), 1)) > GlueNeedleZeroPosD): 
                            AxisDOLPos = GlueNeedleZeroPosD
                            AxisYOLCompPos = (round((BuildPlatformZeroPositionA7.get() + (int(SortedSticks[(x * 10) + 3]) + (int(MaterialWidth.get()) / 2) + PlaceXOffset)), 1)) - GlueNeedleZeroPosD
                        else:
                            AxisDOLPos = round((BuildPlatformZeroPositionA7.get() + (int(SortedSticks[(x * 10) + 3]) + (int(MaterialWidth.get()) / 2) + PlaceXOffset)), 1)
                            AxisYOLCompPos = 0
                            
                        f.write(';Above Stick Placement\n')
                        f.write('M20 G90 G00' + ' X' + str(round(StickPlaceXCalcPos - (math.sin(90 - ((90 - math.atan(((BuildPlatformMaxPositionX.get() - BuildPlatformZeroPositionX.get())) / (BuildPlatformMaxPositionZ.get() - BuildPlatformZeroPositionZ.get()))))) * (PlaceZOffset / math.sin(90))), 1)) 
                                            + ' Y' + str(BuildPlatformZeroPositionY.get() + AxisYOLCompPos) 
                                            + ' Z' + str(round(StickPlaceZCalcPos + (math.sin(90 - (90 - (90 - math.atan(((BuildPlatformMaxPositionX.get() - BuildPlatformZeroPositionX.get())) / (BuildPlatformMaxPositionZ.get() - BuildPlatformZeroPositionZ.get()))))) * (PlaceZOffset / math.sin(90))), 1)) 
                                            + ' A' + str((BuildPlatformZeroPositionA.get())) 
                                            + ' B' + str((BuildPlatformZeroPositionB.get())) 
                                            + ' C' + str((BuildPlatformZeroPositionC.get()))
                                            + ' D' + str(AxisDOLPos) + '\n')
                        f.write('\n')
                        
                        f.write(';Stick Move In\n')
                        f.write('M20 G90 G01' + ' X' + str(round(printPoints(Point(StickPlaceXCalcPos, StickPlaceZCalcPos), PlaceZOffset, ((int(BuildPlatformMaxPositionZ.get()) - int(BuildPlatformZeroPositionZ.get())) / (int(BuildPlatformMaxPositionX.get()) - int(BuildPlatformZeroPositionX.get())))).x))
                                            + ' Y' + str(BuildPlatformZeroPositionY.get() + AxisYOLCompPos) 
                                            + ' Z' + str(round(printPoints(Point(StickPlaceXCalcPos, StickPlaceZCalcPos), PlaceZOffset, ((int(BuildPlatformMaxPositionZ.get()) - int(BuildPlatformZeroPositionZ.get())) / (int(BuildPlatformMaxPositionX.get()) - int(BuildPlatformZeroPositionX.get())))).y)) 
                                            + ' A' + str((BuildPlatformZeroPositionA.get())) 
                                            + ' B' + str((BuildPlatformZeroPositionB.get())) 
                                            + ' C' + str((BuildPlatformZeroPositionC.get()))
                                            + ' D' + str(AxisDOLPos) + '\n')
                        f.write('\n')
                        
                        #Make sure axis D doesent colide with glue sensor LS
                        if ((round((BuildPlatformZeroPositionA7.get() + (int(SortedSticks[(x * 10) + 3]) + (int(MaterialWidth.get()) / 2))), 1)) > GlueNeedleZeroPosD): 
                            AxisDOLPos = GlueNeedleZeroPosD
                            AxisYOLCompPos = (round((BuildPlatformZeroPositionA7.get() + (int(SortedSticks[(x * 10) + 3]) + (int(MaterialWidth.get()) / 2))), 1)) - GlueNeedleZeroPosD
                        else:
                            AxisDOLPos = round((BuildPlatformZeroPositionA7.get() + (int(SortedSticks[(x * 10) + 3]) + (int(MaterialWidth.get()) / 2))), 1)
                            AxisYOLCompPos = 0
                            
                        f.write(';Stick Move Over\n')
                        f.write('M20 G90 G01' + ' X' + str(round(printPoints(Point(StickPlaceXCalcPos, StickPlaceZCalcPos), PlaceZOffset, ((int(BuildPlatformMaxPositionZ.get()) - int(BuildPlatformZeroPositionZ.get())) / (int(BuildPlatformMaxPositionX.get()) - int(BuildPlatformZeroPositionX.get())))).x))
                                            + ' Y' + str(BuildPlatformZeroPositionY.get() + AxisYOLCompPos) 
                                            + ' Z' + str(round(printPoints(Point(StickPlaceXCalcPos, StickPlaceZCalcPos), PlaceZOffset, ((int(BuildPlatformMaxPositionZ.get()) - int(BuildPlatformZeroPositionZ.get())) / (int(BuildPlatformMaxPositionX.get()) - int(BuildPlatformZeroPositionX.get())))).y)) 
                                            + ' A' + str((BuildPlatformZeroPositionA.get())) 
                                            + ' B' + str((BuildPlatformZeroPositionB.get())) 
                                            + ' C' + str((BuildPlatformZeroPositionC.get()))
                                            + ' D' + str(AxisDOLPos) + '\n')
                        f.write('\n')
                        
                        f.write(';Stick Move Down, Place\n')
                        f.write('M20 G90 G01' + ' X' + str(round(StickPlaceXCalcPos, 1)) 
                                            + ' Y' + str(BuildPlatformZeroPositionY.get() + AxisYOLCompPos) 
                                            + ' Z' + str(round(StickPlaceZCalcPos, 1)) 
                                            + ' A' + str((BuildPlatformZeroPositionA.get())) 
                                            + ' B' + str((BuildPlatformZeroPositionB.get())) 
                                            + ' C' + str((BuildPlatformZeroPositionC.get()))
                                            + ' D' + str(AxisDOLPos) + '\n')
                        f.write('\n')
                        
                        #Deactivate Suction Cups
                        f.write(';Deactivate Suction Cups\n')
                        f.write('M3S0\n')
                        f.write('\n')
                        
                        #Wait For Sunction to Deactivate
                        f.write(';Wait For Sunction to Deactivate\n')
                        f.write('G4 P0.5' + '\n')
                        f.write('\n')
                        
                        f.write(';Away From Stick\n')
                        f.write('M20 G90 G01' + ' X' + str(round(StickPlaceXCalcPos - (math.sin(90 - ((90 - math.atan(((BuildPlatformMaxPositionX.get() - BuildPlatformZeroPositionX.get())) / (BuildPlatformMaxPositionZ.get() - BuildPlatformZeroPositionZ.get()))))) * (PlaceZOffset / math.sin(90))), 1)) 
                                            + ' Y' + str(BuildPlatformZeroPositionY.get() + AxisYOLCompPos) 
                                            + ' Z' + str(round(StickPlaceZCalcPos + (math.sin(90 - (90 - (90 - math.atan(((BuildPlatformMaxPositionX.get() - BuildPlatformZeroPositionX.get())) / (BuildPlatformMaxPositionZ.get() - BuildPlatformZeroPositionZ.get()))))) * (PlaceZOffset / math.sin(90))), 1)) 
                                            + ' A' + str((BuildPlatformZeroPositionA.get())) 
                                            + ' B' + str((BuildPlatformZeroPositionB.get())) 
                                            + ' C' + str((BuildPlatformZeroPositionC.get()))
                                            + ' D' + str(AxisDOLPos) + '\n')
                        f.write('\n')
                        
                        f.write(';Push Stick Into Place\n')
                        f.write('M20 G90 G01' + ' X' + str(round(StickPlaceXCalcPos + 5, 1)) 
                                            + ' Y' + str(BuildPlatformZeroPositionY.get() + AxisYOLCompPos) 
                                            + ' Z' + str(round(StickPlaceZCalcPos, 1)) 
                                            + ' A' + str((BuildPlatformZeroPositionA.get())) 
                                            + ' B' + str((BuildPlatformZeroPositionB.get())) 
                                            + ' C' + str((BuildPlatformZeroPositionC.get()))
                                            + ' D' + str(AxisDOLPos) + '\n')
                        f.write('\n')
                        
                        f.write(';Away From Stick\n')
                        f.write('M20 G90 G01' + ' X' + str(round(StickPlaceXCalcPos - (math.sin(90 - ((90 - math.atan(((BuildPlatformMaxPositionX.get() - BuildPlatformZeroPositionX.get())) / (BuildPlatformMaxPositionZ.get() - BuildPlatformZeroPositionZ.get()))))) * (PlaceZOffset / math.sin(90))), 1)) 
                                            + ' Y' + str(BuildPlatformZeroPositionY.get() + AxisYOLCompPos) 
                                            + ' Z' + str(round(StickPlaceZCalcPos + (math.sin(90 - (90 - (90 - math.atan(((BuildPlatformMaxPositionX.get() - BuildPlatformZeroPositionX.get())) / (BuildPlatformMaxPositionZ.get() - BuildPlatformZeroPositionZ.get()))))) * (PlaceZOffset / math.sin(90))), 1)) 
                                            + ' A' + str((BuildPlatformZeroPositionA.get())) 
                                            + ' B' + str((BuildPlatformZeroPositionB.get())) 
                                            + ' C' + str((BuildPlatformZeroPositionC.get()))
                                            + ' D' + str(AxisDOLPos) + '\n')
                        f.write('\n')
                            
                    
                            
                    #If Stick is Horizontal
                    if (str(SortedSticks[(x * 10) + 2]) == 'H'):
                        '''
                        StickPlaceXCalcPos = math.sin((90 - math.atan((int(BuildPlatformMaxPositionZ.get()) - int(BuildPlatformZeroPositionZ.get())) / (int(BuildPlatformMaxPositionX.get()) - int(BuildPlatformZeroPositionX.get()))))) * ((int(SortedSticks[(x * 10) + 4]) - VerticalHorizontalOffset + (int(MaterialWidth.get()) / 2)) / math.sin(90))
                        StickPlaceZCalcPos = math.sin(90 - ((90 - math.atan((int(BuildPlatformMaxPositionZ.get()) - int(BuildPlatformZeroPositionZ.get())) / (int(BuildPlatformMaxPositionX.get()) - int(BuildPlatformZeroPositionX.get())))))) * ((int(SortedSticks[(x * 10) + 4]) - VerticalHorizontalOffset + (int(MaterialWidth.get()) / 2)) / math.sin(90))
                        
                        
                        #DEBUGGING
                        print(str(int(SortedSticks[(x * 10) + 4]) + (int(SortedSticks[(x * 10) + 1]) / 2)))
                        print(str(StickPlaceXCalcPos))
                        print(str(round(BuildPlatformZeroPositionX.get() + StickPlaceXCalcPos, 1)) )
                        print(str(round(BuildPlatformZeroPositionX.get() + StickPlaceXCalcPos - (math.sin(90 - ((90 - math.atan((BuildPlatformMaxPositionX.get() - BuildPlatformZeroPositionX.get()) / (BuildPlatformMaxPositionZ.get() - BuildPlatformZeroPositionZ.get()))))) * (PlaceZOffset / math.sin(90))), 1)) )
                        '''
                        p = Point(int(BuildPlatformZeroPositionX.get()), int(BuildPlatformZeroPositionZ.get()))
                        #printPoints(p, (int(SortedSticks[(x * 10) + 4]) - VerticalHorizontalOffset + (int(MaterialWidth.get()) / 2)), ((int(BuildPlatformMaxPositionZ.get()) - int(BuildPlatformZeroPositionZ.get())) / (int(BuildPlatformMaxPositionX.get()) - int(BuildPlatformZeroPositionX.get()))))
                        StickPlaceXCalcPos = printPoints(p, (int(SortedSticks[(x * 10) + 4]) - VerticalHorizontalOffset + (int(MaterialWidth.get()) / 2)), ((int(BuildPlatformMaxPositionZ.get()) - int(BuildPlatformZeroPositionZ.get())) / (int(BuildPlatformMaxPositionX.get()) - int(BuildPlatformZeroPositionX.get())))).x
                        StickPlaceZCalcPos = printPoints(p, (int(SortedSticks[(x * 10) + 4]) - VerticalHorizontalOffset + (int(MaterialWidth.get()) / 2)), ((int(BuildPlatformMaxPositionZ.get()) - int(BuildPlatformZeroPositionZ.get())) / (int(BuildPlatformMaxPositionX.get()) - int(BuildPlatformZeroPositionX.get())))).y
                        print("StickPlaceXCalcPos = " + str(StickPlaceXCalcPos))
                        print("StickPlaceZCalcPos = " + str(StickPlaceZCalcPos))
                        print("Y pos: " + str(int(SortedSticks[(x * 10) + 4])))
                        print("VerticalHorizontalOffset: " + str(VerticalHorizontalOffset))
                        print("(int(MaterialWidth.get()) / 2): " + str((int(MaterialWidth.get()) / 2)))
                        print("Final Y Pos: " + str((int(SortedSticks[(x * 10) + 4]) - VerticalHorizontalOffset + (int(MaterialWidth.get()) / 2))))
                    
                        #Make sure axis D doesent colide with glue sensor LS
                        if ((round((BuildPlatformZeroPositionA7.get() + (int(SortedSticks[(x * 10) + 3]) + (int(SortedSticks[(x * 10) + 1]) / 2) + PlaceXOffset)), 1)) > GlueNeedleZeroPosD): 
                            AxisDOLPos = GlueNeedleZeroPosD
                            AxisYOLCompPos = (round((BuildPlatformZeroPositionA7.get() + (int(SortedSticks[(x * 10) + 3]) + (int(SortedSticks[(x * 10) + 1]) / 2) + PlaceXOffset)), 1)) - GlueNeedleZeroPosD
                        else:
                            AxisDOLPos = round((BuildPlatformZeroPositionA7.get() + (int(SortedSticks[(x * 10) + 3]) + (int(SortedSticks[(x * 10) + 1]) / 2) + PlaceXOffset)), 1)
                            AxisYOLCompPos = 0
                    
                        f.write(';Above Stick Placement\n')
                        f.write('M20 G90 G00' + ' X' + str(round(StickPlaceXCalcPos - (math.sin(90 - (math.atan((BuildPlatformMaxPositionX.get() - BuildPlatformZeroPositionX.get()) / (BuildPlatformMaxPositionZ.get() - BuildPlatformZeroPositionZ.get())))) * (PlaceZOffset / math.sin(90))), 1)) 
                                            + ' Y' + str(BuildPlatformZeroPositionY.get() + AxisYOLCompPos) 
                                            + ' Z' + str(round(StickPlaceZCalcPos + (math.sin(90 - (90 - (BuildPlatformMaxPositionX.get() - BuildPlatformZeroPositionX.get()) / (BuildPlatformMaxPositionZ.get() - BuildPlatformZeroPositionZ.get()))) * (PlaceZOffset / math.sin(90))), 1)) 
                                            + ' A' + str(VerticalHorizontalOffsetA) 
                                            + ' B' + str(VerticalHorizontalOffsetB) 
                                            + ' C' + str(VerticalHorizontalOffsetC)
                                            + ' D' + str(AxisDOLPos) + '\n')
                        f.write('\n')
                        
                        f.write(';Stick Move In\n')
                        f.write('M20 G90 G01' + ' X' + str(round(printPoints(Point(StickPlaceXCalcPos, StickPlaceZCalcPos), PlaceZOffset, ((int(BuildPlatformMaxPositionZ.get()) - int(BuildPlatformZeroPositionZ.get())) / (int(BuildPlatformMaxPositionX.get()) - int(BuildPlatformZeroPositionX.get())))).x, 1)) 
                                            + ' Y' + str(BuildPlatformZeroPositionY.get() + AxisYOLCompPos) 
                                            + ' Z' + str(round(printPoints(Point(StickPlaceXCalcPos, StickPlaceZCalcPos), PlaceZOffset, ((int(BuildPlatformMaxPositionZ.get()) - int(BuildPlatformZeroPositionZ.get())) / (int(BuildPlatformMaxPositionX.get()) - int(BuildPlatformZeroPositionX.get())))).y, 1)) 
                                            + ' A' + str(VerticalHorizontalOffsetA) 
                                            + ' B' + str(VerticalHorizontalOffsetB) 
                                            + ' C' + str(VerticalHorizontalOffsetC)
                                            + ' D' + str(AxisDOLPos) + '\n')
                        f.write('\n')
                        
                        #Make sure axis D doesent colide with glue sensor LS
                        if ((round((BuildPlatformZeroPositionA7.get() + (int(SortedSticks[(x * 10) + 3]) + (int(SortedSticks[(x * 10) + 1]) / 2))), 1)) > GlueNeedleZeroPosD): 
                            AxisDOLPos = GlueNeedleZeroPosD
                            AxisYOLCompPos = (round((BuildPlatformZeroPositionA7.get() + (int(SortedSticks[(x * 10) + 3]) + (int(SortedSticks[(x * 10) + 1]) / 2))), 1)) - GlueNeedleZeroPosD
                        else:
                            AxisDOLPos = round((BuildPlatformZeroPositionA7.get() + (int(SortedSticks[(x * 10) + 3]) + (int(SortedSticks[(x * 10) + 1]) / 2))), 1)
                            AxisYOLCompPos = 0
                            
                        f.write(';Stick Move Over\n')
                        f.write('M20 G90 G01' + ' X' + str(round(printPoints(Point(StickPlaceXCalcPos, StickPlaceZCalcPos), PlaceZOffset, ((int(BuildPlatformMaxPositionZ.get()) - int(BuildPlatformZeroPositionZ.get())) / (int(BuildPlatformMaxPositionX.get()) - int(BuildPlatformZeroPositionX.get())))).x, 1)) 
                                            + ' Y' + str(BuildPlatformZeroPositionY.get() + AxisYOLCompPos) 
                                            + ' Z' + str(round(printPoints(Point(StickPlaceXCalcPos, StickPlaceZCalcPos), PlaceZOffset, ((int(BuildPlatformMaxPositionZ.get()) - int(BuildPlatformZeroPositionZ.get())) / (int(BuildPlatformMaxPositionX.get()) - int(BuildPlatformZeroPositionX.get())))).y, 1)) 
                                            + ' A' + str(VerticalHorizontalOffsetA) 
                                            + ' B' + str(VerticalHorizontalOffsetB) 
                                            + ' C' + str(VerticalHorizontalOffsetC)
                                            + ' D' + str(AxisDOLPos) + '\n')
                        f.write('\n')
                        
                        f.write(';Stick Move Down, Place\n')
                        f.write('M20 G90 G01' + ' X' + str(round(StickPlaceXCalcPos, 1)) 
                                            + ' Y' + str(BuildPlatformZeroPositionY.get() + AxisYOLCompPos) 
                                            + ' Z' + str(round(StickPlaceZCalcPos, 1)) 
                                            + ' A' + str(VerticalHorizontalOffsetA)
                                            + ' B' + str(VerticalHorizontalOffsetB)
                                            + ' C' + str(VerticalHorizontalOffsetC)
                                            + ' D' + str(AxisDOLPos) + '\n')
                        f.write('\n')
                        
                        #Deactivate Suction Cups
                        f.write(';Deactivate Suction Cups\n')
                        f.write('M3S0\n')
                        f.write('\n')
                        
                        #Wait For Sunction to Deactivate
                        f.write(';Wait For Sunction to Deactivate\n')
                        f.write('G4 P0.5' + '\n')
                        f.write('\n')
                        
                        f.write(';Away From Stick\n')
                        f.write('M20 G90 G01' + ' X' + str(round(StickPlaceXCalcPos - (math.sin(90 - (math.atan((BuildPlatformMaxPositionX.get() - BuildPlatformZeroPositionX.get()) / (BuildPlatformMaxPositionZ.get() - BuildPlatformZeroPositionZ.get())))) * (PlaceZOffset / math.sin(90))), 1)) 
                                            + ' Y' + str(BuildPlatformZeroPositionY.get() + AxisYOLCompPos) 
                                            + ' Z' + str(round(StickPlaceZCalcPos + (math.sin(90 - (90 - (BuildPlatformMaxPositionX.get() - BuildPlatformZeroPositionX.get()) / (BuildPlatformMaxPositionZ.get() - BuildPlatformZeroPositionZ.get()))) * (PlaceZOffset / math.sin(90))), 1)) 
                                            + ' A' + str(VerticalHorizontalOffsetA) 
                                            + ' B' + str(VerticalHorizontalOffsetB) 
                                            + ' C' + str(VerticalHorizontalOffsetC)
                                            + ' D' + str(AxisDOLPos) + '\n')
                        f.write('\n')
                        
                        f.write(';Push Stick Into Place\n')
                        f.write('M20 G90 G01' + ' X' + str(round(StickPlaceXCalcPos + 5, 1)) 
                                            + ' Y' + str(BuildPlatformZeroPositionY.get() + AxisYOLCompPos) 
                                            + ' Z' + str(round(StickPlaceZCalcPos, 1)) 
                                            + ' A' + str(VerticalHorizontalOffsetA)
                                            + ' B' + str(VerticalHorizontalOffsetB)
                                            + ' C' + str(VerticalHorizontalOffsetC)
                                            + ' D' + str(AxisDOLPos) + '\n')
                        f.write('\n')
                        
                        f.write(';Away From Stick\n')
                        f.write('M20 G90 G01' + ' X' + str(round(StickPlaceXCalcPos - (math.sin(90 - (math.atan((BuildPlatformMaxPositionX.get() - BuildPlatformZeroPositionX.get()) / (BuildPlatformMaxPositionZ.get() - BuildPlatformZeroPositionZ.get())))) * (PlaceZOffset / math.sin(90))), 1)) 
                                            + ' Y' + str(BuildPlatformZeroPositionY.get() + AxisYOLCompPos) 
                                            + ' Z' + str(round(StickPlaceZCalcPos + (math.sin(90 - (90 - (BuildPlatformMaxPositionX.get() - BuildPlatformZeroPositionX.get()) / (BuildPlatformMaxPositionZ.get() - BuildPlatformZeroPositionZ.get()))) * (PlaceZOffset / math.sin(90))), 1)) 
                                            + ' A' + str(VerticalHorizontalOffsetA) 
                                            + ' B' + str(VerticalHorizontalOffsetB) 
                                            + ' C' + str(VerticalHorizontalOffsetC)
                                            + ' D' + str(AxisDOLPos) + '\n')
                        f.write('\n')
                    
                    #Move to Universal Position
                    f.write(';Move to Universal Position\n')
                    f.write('M20 G90 G00' + ' X' + str(UniversalPosX) 
                                        + ' Y' + str(UniversalPosY) 
                                        + ' Z' + str(UniversalPosZ) 
                                        + ' A' + str(UniversalPosA) 
                                        + ' B' + str(UniversalPosB) 
                                        + ' C' + str(UniversalPosC)
                                        + ' D' + str(BuildPlatformZeroPositionA7.get() + 100) + '\n')
                    f.write('\n')
                    

                    
                #End at rest position
                f.write('\n')
                f.write(';End in rest position\n')
                f.write('M21 G90 G00 ' + 'X' + str((int(float(RestPositionJ1.get()) * 100) / 100) + 90) + ' ' + 'Y' + str(int(float(RestPositionJ2.get()) * 100) / 100) + ' ' + 'Z' + str(int(float(RestPositionJ3.get()) * 100) / 100) + ' ' + 'A' + str(int(float(RestPositionJ4.get()) * 100) / 100) + ' ' + 'B' + str(int(float(RestPositionJ5.get()) * 100) / 100) + ' ' + 'C' + str(int(float(RestPositionJ6.get()) * 100) / 100) + '\n')
                    
                #Close File
                f.close
                
                #Feedback
                messagebox.showinfo('info', 'File Complete!')
    
    
#Exicute GenerateStickFeed UpdatePreview
def GenerateStickFeed():
    #Error Messages 
    #Enter Material Width Errer Detection
    if len(MaterialWidthEntry.get()) == 0:
        messagebox.showerror('info', 'Please Enter Material Width!')
    else:
        #No Sticks Errer Detection
        if StickCount <= 1:
            messagebox.showerror('info', 'No Sticks Inputted!')
        else:
            #Destination File Chosen Errer Detection
            if str(DirectoryChosen.get()) == 'NULL':
                messagebox.showerror('info', 'Please chose a destination file!')
            else:
                #One Time Calculations:
                SortStickData()

                #Compile File Name and Address
                completeName = os.path.join(str(folder_selected), str(SetProgramName.get())+' Stick Feed Order' + '.txt')
                f = open(completeName, 'w')

                #Write Document
                    
                #Defalt Title Paragraph
                f.write(';File generated by Mirobot Frame Building Cell GUI\n')
                f.write(';' + str(Version.get()) + '\n')
                f.write(";Date Generated: ") 
                f.write(str(datetime.now()))
                f.write('\n')
                f.write('\n')
                f.write('\n')
                
                #Stick Feed Order
                #Universal Information
                f.write('Universal Information:')
                f.write('\n')
                f.write('Material Width: ' + str(MaterialWidthEntry.get()))
                f.write('\n')
                f.write('Build Platform Width: ' + str(BuildSpaceXMM) + 'mm')
                f.write('\n')
                f.write('Build Platform Heighth: ' +str(BuildSpaceYMM) +  'mm')
                f.write('\n')
                f.write('\n')
                f.write('\n')
                
                #Sticks and Lengths
                f.write('Stick Feed Order:')
                f.write('\n')
                for x in range(StickCount - 1):
                    #Order Number
                    f.write(str(x + 1) + '.  ')
                    #Print Stick Name
                    f.write(str(SortedSticks[(x * 10) + 0]) + ', ')
                    #Print Stick Length
                    f.write('Length: ' + str(SortedSticks[(x * 10) + 1]) + 'mm')
                    #New Line Between Sticks
                    f.write('\n')
                    f.write('\n')
                    
                #End Doc
                f.write('\n')
                f.write('End')
                
                #Close File
                f.close
                
                #Feedback
                messagebox.showinfo('info', 'File Complete!')
                
#When Mouse is Clicked Inside the Stick Panel
def ClickedOnSticks( event ):    
    #DEBUGGING
    print( "mouse clicked at x=" + str(event.x) + " y=" + str(event.y) )    
    
    global StickInfoBoxClickedOn
    #Figure Which Row the Mouse Was Clicked in and Apply Quantity of Sticks in Previous Column (5, 10, 15)
    StickInfoBoxClickedOn = (round((event.x / StickInfoBoxWidth) -0.5)) * 5
    #Fugure How Many Sticks Come Before Selected in That Row and Add to Quantity From Previous Columns
    StickInfoBoxClickedOn += (round((event.y / StickInfoBoxHeight) -0.5)) + 1
    
    #Adjust Clicks Out of Boundry that Will Feed Inacurate Information
    if (event.y > 300):
        StickInfoBoxClickedOn -= 1
    
    #DEBUGGING
    print( "mouse clicked Stick Box=" + str(StickInfoBoxClickedOn))
    
    #Write To Selected Stick That it is Selected (0 = Deselected 1 = Selected)
    global StickData
    if (StickData[((StickInfoBoxClickedOn * 10) + 5)] == 1):
        StickData[((StickInfoBoxClickedOn * 10) + 5)] = 0
    else:
        StickData[((StickInfoBoxClickedOn * 10) + 5)] = 1
    
    UpdatePreview()
    
    
def DeleteClickedOnSticks():
    global StickCount
    #DEBUGGING
    print("Delete Button Pressed")
    
    #Look through Stick Data
    #y= Count Which Piece of Data Were Looking at 
    y=0
    for x in StickData:
        #If Were Looking at Every 5th Piece of Data (Info Box Selected)
        if (str(y)[-1] == '5'):
            #Check if Stick is Selected
            if (StickData[y] == 1):
                #DEBUGGING
                print("delete y=" + str(y) + ": " + str(StickData[y]))
                print("StickData Length= " + str(len(StickData)))
                #Print Data List Before Deletion
                print(StickData)
                
                #repeat for how many variables in StickData Come After Deleted Stick
                print("FollowingVarCount= " + str(len(StickData) - (y - 5)))
                for x in range(len(StickData) - (y - 5)):
                    #Only Write Data if Following Data is Avalible, Error Prevention
                    if (((y + 5) + x) < len(StickData)):
                        #Skip Writing Over Stick Order ID(9) Since they Need to Stay Consecutive
                        if (str(x)[-1] != "9"): #or logic does not work here
                            #if (str(x)[-1] != "0"):
                            print("x= " + str(x))
                            #Move Folowing Stick Data to Deleted Stick Data
                            StickData[(y - 5) + x] = StickData[(y + 5) + x]
                else:
                    #DEBUGGING print Data List When Done 
                    print(StickData)
                    
                    #Back up y 10 Counts So it Doesent Miss Newly Replaced Info Box
                    y -= 10
                    
                
                StickCount -= 1
                UpdatePreview()    
                  
        y+=1
        
    #Generate New Stick Name at End of List
    #if (str(x)[-1] == "0" and x > (StickCount * 10)):
    #print("Stick Count *10 = " + str(StickCount * 10))
    #print("x=" + str(x))
    #print("StickData=" + str(StickData))
    #print("StickData[210]=" + str(StickData[210]))
    StickData[210] = ("Stick" + str(int(str(StickData[210])[-2:]) + 1))
    print("StickData=" + str(StickData))
    #print(y)
    
                
#Exicute Update Preview
def UpdatePreview():
    global StickData
    #Error Messages 
    #Fill All Fields Errer Detection
    if MaterialWidthMAXSpec.get() < MaterialWidth.get() or MaterialWidthMINSpec.get() > MaterialWidth.get():
        messagebox.showerror('info', 'Material width out of range!')
    else:
        global StickInfoBoxClickedOn
        
        #Add Image to Canvas
        MyImage = MyCanvas.create_image(30,40, anchor=NW, image=img)
        
        #Stick Preview
        for x in range(StickCount):
            #Box Fill Color Based On Mouse Click Selection
            #Deselected
            if (StickData[(((x + 0) * 10) + 5)] == 0):
                StickInfoBoxColor = "#ebcda4"
            #Selected
            if (StickData[(((x + 0) * 10) + 5)] == 1):
                StickInfoBoxColor = "#a69072" 
                
            #Horizontal Sticks
            if (str(StickData[(x * 10) + 2]) == "H"):
                #DEBUGGING
                print( "StickXPos=" + str((PreviewPanelWidth - PreviewPanelZeroXPX) - int(StickData[(x * 10) + 3])))
                print( "StickYPos=" + str((PreviewPanelHeight - PreviewPanelZeroYPX) - int(StickData[(x * 10) + 4])))
                
                #Sticks
                MyCanvas.create_rectangle(((PreviewPanelWidth - PreviewPanelZeroXPX) - (int(StickData[(x * 10) + 3]) * MMtoPX)) - ((int(StickData[(x * 10) + 1])) * MMtoPX), 
                                          ((PreviewPanelHeight - PreviewPanelZeroYPX) - (int(StickData[(x * 10) + 4]) * MMtoPX)) - (MaterialWidth.get() * MMtoPX), 
                                          ((PreviewPanelWidth - PreviewPanelZeroXPX) - (int(StickData[(x * 10) + 3]) * MMtoPX)), 
                                          ((PreviewPanelHeight - PreviewPanelZeroYPX) - (int(StickData[(x * 10) + 4]) * MMtoPX)), 
                                          fill=StickInfoBoxColor)
                
            #Verticle Sticks
            if (str(StickData[(x * 10) + 2]) == "V"):
                #DEBUGGING
                print( "StickXPos=" + str((PreviewPanelWidth - PreviewPanelZeroXPX) - int(StickData[(x * 10) + 3])))
                print( "StickYPos=" + str((PreviewPanelHeight - PreviewPanelZeroYPX) - int(StickData[(x * 10) + 4])))
                
                #Sticks
                MyCanvas.create_rectangle(((PreviewPanelWidth - PreviewPanelZeroXPX) - (int(StickData[(x * 10) + 3]) * MMtoPX))  - (MaterialWidth.get() * MMtoPX),
                                          ((PreviewPanelHeight - PreviewPanelZeroYPX) - (int(StickData[(x * 10) + 4]) * MMtoPX)) - ((int(StickData[(x * 10) + 1])) * MMtoPX), 
                                          ((PreviewPanelWidth - PreviewPanelZeroXPX) - (int(StickData[(x * 10) + 3]) * MMtoPX)), 
                                          ((PreviewPanelHeight - PreviewPanelZeroYPX) - (int(StickData[(x * 10) + 4]) * MMtoPX)), 
                                          fill=StickInfoBoxColor)

        #Grid
        #Horizontal Lines
        for x in range((round((BuildSpaceYMM / MaterialWidth.get()) - 0.5)) + 1):
            MyCanvas.create_line(30, 532 - ((BuildSpaceYPX / ((round((BuildSpaceYMM / MaterialWidth.get()) - 0.5)) + 0)) * x), 535, 532 - ((BuildSpaceYPX / ((round((BuildSpaceYMM / MaterialWidth.get()) - 0.5)) + 0)) * x), fill="grey")

        #Vertical Lines
        for x in range((round((BuildSpaceXMM / MaterialWidth.get()) - 0.5)) + 1):
            MyCanvas.create_line(534 - ((BuildSpaceXPX / ((round((BuildSpaceXMM / MaterialWidth.get()) - 0.5)) + 0)) * x), 40, 534 - ((BuildSpaceXPX / ((round((BuildSpaceXMM / MaterialWidth.get()) - 0.5)) + 0)) * x), 532, fill="grey")
            
        #Stick Info Boxes
        #Create Canvas
        StickDataBoxesCanvas = Canvas(root, width = StickInfoBoxCanvasWidth, height = StickInfoBoxCanvasHeight, bg = 'white')
        StickDataBoxesCanvas.place(x=20, y=165)
        #Read Mouse clicked as an event for this Panel
        StickDataBoxesCanvas.bind( "<Button>", ClickedOnSticks ) 
        #Display Sticks Data Boxes
        for x in range(StickCount - 1):
            #Box Fill Color Based On Mouse Click Selection
            #Deselected
            if (StickData[(((x + 1) * 10) + 5)] == 0):
                StickInfoBoxColor = "#ebcda4"
            #Selected
            if (StickData[(((x + 1) * 10) + 5)] == 1):
                StickInfoBoxColor = "#a69072" 
                
            #Row 1
            if -1 < x < 5:
                #Box
                StickDataBoxesCanvas.create_rectangle(0 + (StickInfoBoxWidth * 0), 0 + (x * StickInfoBoxHeight) - (StickInfoBoxCanvasHeight * 0), (StickInfoBoxWidth * 1), StickInfoBoxHeight + (x * StickInfoBoxHeight) - (StickInfoBoxCanvasHeight * 0), fill=StickInfoBoxColor, activedash= True)
                #Stick Name
                StickDataBoxesCanvas.create_text(67 + (StickInfoBoxWidth * 0), 12 + (x * StickInfoBoxHeight) - (StickInfoBoxCanvasHeight * 0), text=StickData[((x + 1) * 10) + 0], font="Arial 8 bold")
                #Stick Length
                StickDataBoxesCanvas.create_text(8 + (StickInfoBoxWidth * 0), 35 + (x * StickInfoBoxHeight) - (StickInfoBoxCanvasHeight * 0), text=StickData[((x + 1) * 10) + 1] + 'mm', font="Arial 11 bold", anchor='w')
                #Stick Position
                StickDataBoxesCanvas.create_text(75 + (StickInfoBoxWidth * 0), 35 + (x * StickInfoBoxHeight) - (StickInfoBoxCanvasHeight * 0), text=StickData[((x + 1) * 10) + 3] + ", " + StickData[((x + 1) * 10) + 4], font="Arial 11 bold", anchor='w')
                
                #DEBUGGING
                print( "StickInfoBoxClickedOn=" + str(StickInfoBoxClickedOn))
                print( "Reading Box Color Data Pos=" + str((StickInfoBoxClickedOn * 10) + 5))
                print( "Reading Box Color ID=" + str(StickData[((StickInfoBoxClickedOn * 10) + 5)]))
                print( "Box Color=" + str(StickInfoBoxColor))
            else:
                #Row 2
                if 4 < x < 10:
                    #Box
                    StickDataBoxesCanvas.create_rectangle(0 + (StickInfoBoxWidth * 1), 0 + (x * StickInfoBoxHeight) - (StickInfoBoxCanvasHeight * 1), (StickInfoBoxWidth * 2), StickInfoBoxHeight + (x * StickInfoBoxHeight) - (StickInfoBoxCanvasHeight * 1), fill=StickInfoBoxColor, activedash= True)
                    #Stick Name
                    StickDataBoxesCanvas.create_text(67 + (StickInfoBoxWidth * 1), 12 + (x * StickInfoBoxHeight) - (StickInfoBoxCanvasHeight * 1), text=StickData[((x + 1) * 10) + 0], font="Arial 8 bold")
                    #Stick Length
                    StickDataBoxesCanvas.create_text(8 + (StickInfoBoxWidth * 1), 35 + (x * StickInfoBoxHeight) - (StickInfoBoxCanvasHeight * 1), text=StickData[((x + 1) * 10) + 1] + 'mm', font="Arial 11 bold", anchor='w')
                    #Stick Position
                    StickDataBoxesCanvas.create_text(75 + (StickInfoBoxWidth * 1), 35 + (x * StickInfoBoxHeight) - (StickInfoBoxCanvasHeight * 1), text=StickData[((x + 1) * 10) + 3] + ", " + StickData[((x + 1) * 10) + 4], font="Arial 11 bold", anchor='w')
                else: 
                    #Row 3
                    if 9 < x < 15:
                        #Box
                        StickDataBoxesCanvas.create_rectangle(0 + (StickInfoBoxWidth * 2), 0 + (x * StickInfoBoxHeight) - (StickInfoBoxCanvasHeight * 2), (StickInfoBoxWidth * 3), StickInfoBoxHeight + (x * StickInfoBoxHeight) - (StickInfoBoxCanvasHeight * 2), fill=StickInfoBoxColor, activedash= True)
                        #Stick Name
                        StickDataBoxesCanvas.create_text(67 + (StickInfoBoxWidth * 2), 12 + (x * StickInfoBoxHeight) - (StickInfoBoxCanvasHeight * 2), text=StickData[((x + 1) * 10) + 0], font="Arial 8 bold")
                        #Stick Length
                        StickDataBoxesCanvas.create_text(8 + (StickInfoBoxWidth * 2), 35 + (x * StickInfoBoxHeight) - (StickInfoBoxCanvasHeight * 2), text=StickData[((x + 1) * 10) + 1] + 'mm', font="Arial 11 bold", anchor='w')
                        #Stick Position
                        StickDataBoxesCanvas.create_text(75 + (StickInfoBoxWidth * 2), 35 + (x * StickInfoBoxHeight) - (StickInfoBoxCanvasHeight * 2), text=StickData[((x + 1) * 10) + 3] + ", " + StickData[((x + 1) * 10) + 4], font="Arial 11 bold", anchor='w')
                    else:
                        #Row 4
                        if 14 < x < 20:
                            #Box
                            StickDataBoxesCanvas.create_rectangle(0 + (StickInfoBoxWidth * 3), 0 + (x * StickInfoBoxHeight) - (StickInfoBoxCanvasHeight * 3), (StickInfoBoxWidth * 4), StickInfoBoxHeight + (x * StickInfoBoxHeight) - (StickInfoBoxCanvasHeight * 3), fill=StickInfoBoxColor, activedash= True)
                            #Stick Name
                            StickDataBoxesCanvas.create_text(67 + (StickInfoBoxWidth * 3), 12 + (x * StickInfoBoxHeight) - (StickInfoBoxCanvasHeight * 3), text=StickData[((x + 1) * 10) + 0], font="Arial 8 bold")
                            #Stick Length
                            StickDataBoxesCanvas.create_text(8 + (StickInfoBoxWidth * 3), 35 + (x * StickInfoBoxHeight) - (StickInfoBoxCanvasHeight * 3), textMax=StickData[((x + 1) * 10) + 1] + 'mm', font="Arial 11 bold", anchor='w')
                            #Stick Position
                            StickDataBoxesCanvas.create_text(75 + (StickInfoBoxWidth * 3), 35 + (x * StickInfoBoxHeight) - (StickInfoBoxCanvasHeight * 3), text=StickData[((x + 1) * 10) + 3] + ", " + StickData[((x + 1) * 10) + 4], font="Arial 11 bold", anchor='w')

def ZerosInfoWindow():
    #Window Perameters
    ZerosInfoWindow = Toplevel()
    ZerosInfoWindow.title('How Do I Find Zeros?')
    ZerosInfoWindow.iconbitmap('wlkataiconIcon.ico')
    ZerosInfoWindow.geometry('1200x597')
    ZerosInfoWindow.configure(background="#999999")
    
    #Frame Building Canvas Max Position Image
    FrameBuildingCanvasMaxPositionImage = ImageTk.PhotoImage(Image.open('images/Frame Building Canvas Max Position.png'))
    FrameBuildingCanvasMaxPositionImageLabel = Label(ZerosInfoWindow, image = FrameBuildingCanvasMaxPositionImage )
    FrameBuildingCanvasMaxPositionImageLabel.place(x=634, y=15)
    FrameBuildingCanvasMaxPositionImageLabel.image = FrameBuildingCanvasMaxPositionImage
    
    #Frame Building Canvas Max Position Description
    FrameBuildingCanvasMaxPositionLabel = Label(ZerosInfoWindow, text = 'Canvas Max Position', font= ('Arial', 20))
    FrameBuildingCanvasMaxPositionLabel.place(x = 918, y = 15)
    FrameBuildingCanvasMaxPositionTextBoxMessage ="""Position the dual suction cup     tool in the upper left corner of  the canvas as shown in the image. The suction cups should be        touching the canvas. The          (X,Y,Z,A,B,C) values are used to  determine the angle of the canvas and not the build volume."""

    FrameBuildingCanvasMaxPositionTextBox = Text(ZerosInfoWindow,height=10,width=34,)
    FrameBuildingCanvasMaxPositionTextBox.place(x = 918, y = 50)
    FrameBuildingCanvasMaxPositionTextBox.insert('end', FrameBuildingCanvasMaxPositionTextBoxMessage)
    FrameBuildingCanvasMaxPositionTextBox.config(state='disabled')
    
    #Frame Building Canvas Zero Position Image
    FrameBuildingCanvasZeroPositionImage = ImageTk.PhotoImage(Image.open('images/Frame Building Canvas Zero Position.png'))
    FrameBuildingCanvasZeroPositionImageLabel = Label(ZerosInfoWindow, image = FrameBuildingCanvasZeroPositionImage )
    FrameBuildingCanvasZeroPositionImageLabel.place(x=916, y=302)
    FrameBuildingCanvasZeroPositionImageLabel.image = FrameBuildingCanvasZeroPositionImage
    
    #Frame Building Canvas Zero Position Description
    FrameBuildingCanvasZeroPositionLabel = Label(ZerosInfoWindow, text = 'Canvas Zero Position', font= ('Arial', 20))
    FrameBuildingCanvasZeroPositionLabel.place(x = 652, y = 302)
    FrameBuildingCanvasZeroPositionTextBoxMessage ="""Position the dual suction cup     tool in the lower right corner of the canvas as shown in the image. The suction cups should be        touching the canvas. The          (X,Y,Z,A,B,C) values are used to  determine the angle of the canvas and not the build volume."""
    
    FrameBuildingCanvasZeroPositionTextBox = Text(ZerosInfoWindow,height=10,width=34,)
    FrameBuildingCanvasZeroPositionTextBox.place(x = 640, y = 337)
    FrameBuildingCanvasZeroPositionTextBox.insert('end', FrameBuildingCanvasZeroPositionTextBoxMessage)
    FrameBuildingCanvasZeroPositionTextBox.config(state='disabled')
    
    #Stick Pickup Zero Position Image
    StickPickupZeroPositionImage = ImageTk.PhotoImage(Image.open('images/Pickup Zero Position.png'))
    StickPickupZeroPositionImageLabel = Label(ZerosInfoWindow, image = StickPickupZeroPositionImage )
    StickPickupZeroPositionImageLabel.place(x=1, y=15)
    StickPickupZeroPositionImageLabel.image = StickPickupZeroPositionImage
    
    #Stick Pickup Zero Position Description
    StickPickupZeroPositionLabel = Label(ZerosInfoWindow, text = 'Stick Pickup Zero Position', font= ('Arial', 20))
    StickPickupZeroPositionLabel.place(x = 306, y = 15)
    StickPickupZeroPositionTextBoxMessage ="""Position the dual suction cup     tool in the corner of the materialstop as shown in the image.   The suction cups should be touching   the conveyor belt. The            (X,Y,Z,A,B,C) values are used to  determine the middle of the       material where the robot will be  picking up the stick from."""
    
    StickPickupZeroPositionTextBox = Text(ZerosInfoWindow,height=10,width=34,)
    StickPickupZeroPositionTextBox.place(x = 306, y = 53)
    StickPickupZeroPositionTextBox.insert('end', StickPickupZeroPositionTextBoxMessage)
    StickPickupZeroPositionTextBox.config(state='disabled')
    
#Exicute Update Preview
def NewStick():
    global NewStickWindowOpen
    #Error Messages         
    if NewStickWindowOpen == False:
        #Max Stick Count Error Detection
        if MaxStick < StickCount:
            messagebox.showerror('info', 'Max stick count reached!')
        else:
            #Window Perameters
            NewStickWindow = Toplevel()
            NewStickWindow.title('New Stick')
            NewStickWindow.iconbitmap('wlkataiconIcon.ico')
            NewStickWindow.geometry('900x500')
            NewStickWindow.configure(background="#999999")
            NewStickWindowOpen = True
            
            #Graphic Dimention Example
            #Create Canvas
            StickDimenEXCanvas = Canvas(NewStickWindow, width=400, height=400, bg='white')
            StickDimenEXCanvas.place(x=470, y=70)
                    
            #Horizontal Rectangle
            #StickDimenEXCanvas.create_rectangle(x1, y1, x2, y2, fill="color")
            # x1, y1 = Top Left
            # x2, y2 = Botom Right
            StickDimenEXCanvas.create_rectangle(50, 300, 350, 350, fill="tan")
            
            #Vertical Rectangle
            StickDimenEXCanvas.create_rectangle(300, 300, 350, 50, fill="tan")

            #Origon Elipse
            #MyCanvas.create_oval(x1, y1, x2, y2, fill="color")
            # x1, y1 = Top Left
            # x2, y2 = Botom Right
            StickDimenEXCanvas.create_oval(340,340,360,360, fill="red")

            #Vertical Rectangle Hiden Line
            #MyCanvas.create_line(x1, y1, x2, y2, fill = "color")
            StickDimenEXCanvas.create_line(300, 300, 300, 350, fill="black")
            
            #X and Y Position
            StickDimenEXCanvas.create_text(300, 370, text="X and Y Position", font="Arial 12 bold", fill="red")
            
            #Length Dimention Line
            #Horizontal Line
            StickDimenEXCanvas.create_line(50, 280, 350, 280, fill="black")
            #Left Vertical Line
            StickDimenEXCanvas.create_line(50, 300, 50, 265, fill="black")
            #Length Text
            StickDimenEXCanvas.create_text(200, 265, text="Length (MM)", font="Arial 12 bold", fill="black")
            
            #Horizontal Orientation
            StickDimenEXCanvas.create_text(180, 325, text="H", font="Arial 22 bold", fill="black")
            
            #Vertical Orientation
            StickDimenEXCanvas.create_text(325, 165, text="V", font="Arial 22 bold", fill="black")
            
            #Material Width Dimention
            #Right Vertical Line
            StickDimenEXCanvas.create_line(350, 50, 350, 15, fill="black")
            #Left Vertical Line
            StickDimenEXCanvas.create_line(300, 50, 300, 15, fill="black")
            #Horizontal Line
            StickDimenEXCanvas.create_line(300, 30, 350, 30, fill="black")
            #Material Width Text
            StickDimenEXCanvas.create_text(220, 30, text="Material Width (MM)", font="Arial 12 bold", fill="black")
            
            #Graph
            #Vertical Line
            StickDimenEXCanvas.create_line(390, 30, 390, 390, fill="black")
            #Horizontal Line
            StickDimenEXCanvas.create_line(30, 390, 390, 390, fill="black")
            #Origon Dot
            StickDimenEXCanvas.create_oval(385,385,395,395, fill="black")
            #Vertical Arrow
            #Right Hand
            StickDimenEXCanvas.create_line(390, 30, 395, 35, fill="black")
            #Left Hand
            StickDimenEXCanvas.create_line(390, 30, 385, 35, fill="black")
            #Horizontal Arrow
            #Top Hand
            StickDimenEXCanvas.create_line(30, 390, 35, 385, fill="black")
            #Bottom Hand
            StickDimenEXCanvas.create_line(30, 390, 35, 395, fill="black")
            #Y Max Travel Text
            StickDimenEXCanvas.create_text(380, 15, text=str(BuildSpaceYMM) + 'mm', font="Arial 8 bold", fill="black")
            #X Max Travel Text
            StickDimenEXCanvas.create_text(35, 375, text=str(BuildSpaceXMM) + 'mm', font="Arial 8 bold", fill="black")
            #Origon Text
            StickDimenEXCanvas.create_text(375, 375, text='0', font="Arial 8 bold", fill="black")
            #X Text
            StickDimenEXCanvas.create_text(15, 390, text='X', font="Arial 12 bold", fill="black")
            #Y Text
            StickDimenEXCanvas.create_text(375, 35, text='Y', font="Arial 12 bold", fill="black")
            
            
            #Set Stick Name
            DefaltStickName.set(StickData[StickCount * 10])
            SetStickNameEntry= Entry(NewStickWindow, width = 78, textvariable = DefaltStickName, fg = 'black', font= ('Arial', 15))
            SetStickNameEntry.place(x=15, y=15)
            
            #Stick Length
            StickLengthLabel = Label(NewStickWindow, text= 'Stick Length (mm)', font= ('Arial', 12))
            StickLengthLabel.place(x=15, y= 75, anchor='w')

            StickLengthEntry = Entry(NewStickWindow, width = 10, fg = 'black', font= ('Arial', 12)) #, textvariable = StickData[(StickCount * 10) + 1]
            StickLengthEntry.place(x=325, y= 75, anchor='w')
            StickData[((StickCount * 10) + 1)] = StickLengthEntry.get()
            
            #Stick Orentation
            OrientationLabel = Label(NewStickWindow, text= 'Select Orientation', font= ('Arial', 12))
            OrientationLabel.place(x=15, y= 110, anchor='w')
            
            def OrientSelc (event):
                if clicked.get() == 'Horizontal':
                    #Write Data
                    StickData[((StickCount * 10) + 2)] = "H"
                else:
                    #Write Data
                    StickData[((StickCount * 10) + 2)] = "V"
            
            clicked = StringVar()
            clicked.set(OrentSelectOptions[0])

            drop = OptionMenu(NewStickWindow, clicked, *OrentSelectOptions, command= OrientSelc)
            drop.place(x=325, y= 110, anchor='w')
            
            #Select X Position
            XPosLabel = Label(NewStickWindow, text= 'Stick X Position (mm)', font= ('Arial', 12))
            XPosLabel.place(x=15, y= 145, anchor='w')

            XPosEntry = Entry(NewStickWindow, width = 10, fg = 'black', font= ('Arial', 12)) #, textvariable = StickData[(StickCount * 10) + 3]
            XPosEntry.place(x=325, y= 145, anchor='w')
            StickData[((StickCount * 10) + 3)] = XPosEntry.get()
            
            #Select Y Position
            YPosLabel = Label(NewStickWindow, text= 'Stick Y Position (mm)', font= ('Arial', 12))
            YPosLabel.place(x=15, y= 180, anchor='w')

            YPosEntry = Entry(NewStickWindow, width = 10, fg = 'black', font= ('Arial', 12)) #, textvariable = StickData[(StickCount * 10) + 4]
            YPosEntry.place(x=325, y= 180, anchor='w')
            StickData[((StickCount * 10) + 4)] = YPosEntry.get()
            
            #Close Window Protocol 
            def CloseWindow():
                global NewStickWindowOpen
                NewStickWindowOpen = False
                UpdatePreview()
                NewStickWindow.destroy()
                
            #Write Stick Data
            def AddStick():
                #Recal StickCount
                global StickCount
                
                #Write Data
                StickData[(StickCount * 10) + 0] = str(DefaltStickName.get())
                StickData[(StickCount * 10) + 1] = StickLengthEntry.get()
                StickData[(StickCount * 10) + 3] = XPosEntry.get()
                StickData[(StickCount * 10) + 4] = YPosEntry.get()
                
                #Error Messages
                #Fill All Fields Error Detection
                if StickData[(StickCount * 10) + 1] == 0 or StickData[(StickCount * 10) + 3] == 0 or StickData[(StickCount * 10) + 4] == 0:
                    messagebox.showerror('info', 'Fill out all fields!')
                    
                    #DEBUGGING
                    print(StickData[(StickCount * 10) + 1])
                    print((StickCount * 10) + 1)
                else:
                #Stick Outside Work Space
                
                
                    #DEBUGGING
                    print(StickData[(StickCount * 10) + 2])
                        
                        
                #Vertical Sticks
                    try:
                        if str(StickData[(StickCount * 10) + 2]) == "V" and (((PreviewPanelWidth - PreviewPanelZeroXPX) - (int(StickData[(StickCount * 10) + 3]) * MMtoPX)) - (MaterialWidth.get() * MMtoPX) < ((PreviewPanelWidth - BuildSpaceXPX) - PreviewPanelZeroXPX) or ((PreviewPanelHeight - PreviewPanelZeroYPX) - (int(StickData[(StickCount * 10) + 4]) * MMtoPX)) - ((int(StickData[(StickCount * 10) + 1])) * MMtoPX) < ((PreviewPanelHeight - BuildSpaceYPX) - PreviewPanelZeroYPX)):
                            messagebox.showerror('info', 'Stick Outside v Workspace!')
                            
                            #DEBUGGING
                            print(StickData[(StickCount * 10) + 1])
                            print((StickCount * 10) + 1)
                        else:
                            #Horizontal Sticks
                            if str(StickData[(StickCount * 10) + 2]) == "H" and (((PreviewPanelWidth - PreviewPanelZeroXPX) - (int(StickData[(StickCount * 10) + 3]) * MMtoPX)) - ((int(StickData[(StickCount * 10) + 1])) * MMtoPX) < ((PreviewPanelWidth - BuildSpaceXPX) - PreviewPanelZeroXPX) or ((PreviewPanelHeight - PreviewPanelZeroYPX) - (int(StickData[(StickCount * 10) + 4]) * MMtoPX)) - (MaterialWidth.get() * MMtoPX) < ((PreviewPanelHeight - BuildSpaceYPX) - PreviewPanelZeroYPX)):
                                messagebox.showerror('info', 'Stick Outside h Workspace!')
                                
                                #DEBUGGING
                                print(StickData[(StickCount * 10) + 1])
                                print((StickCount * 10) + 1)
                            else:
                                #Invalad Values Error Detection
                                if int(StickData[(StickCount * 10) + 1]) <= 0 or int(StickData[(StickCount * 10) + 3]) < 0 or int(StickData[(StickCount * 10) + 4]) < 0:
                                    messagebox.showerror('info', 'Negative or Zero values!')
                                else:
                                    #Stick Length Too Short
                                    if int(StickData[(StickCount * 10) + 1]) < StickMinimumLength:
                                        messagebox.showerror('info', 'Stick Length Too Short!')
                                    else:
                                        try :
                                            float(StickData[(StickCount * 10) + 1]) # Tries to convert the value to a float.
                                            float(StickData[(StickCount * 10) + 3])
                                            float(StickData[(StickCount * 10) + 4])
                                            float(StickData[(StickCount * 10) + 5])
                                            
                                            #If Values Valad
                                            #DEBUGGING
                                            print(StickData[(StickCount * 10) + 0])
                                            print(StickData[(StickCount * 10) + 1])
                                            print(StickData[(StickCount * 10) + 2])
                                            print(StickData[(StickCount * 10) + 3])
                                            print(StickData[(StickCount * 10) + 4])
                                            print(StickData[(StickCount * 10) + 5])
                                            print(StickCount)
                                            
                                            #Add Stick
                                            StickCount += 1
                                            
                                            #Close Window
                                            CloseWindow()                        
                                        except ValueError :
                                            #If Values Are Not Numbers
                                            messagebox.showerror('info', 'Must be numerical values!')
                    except:
                        messagebox.showerror('info', 'Must be numerical values!')
                        
                    
            
            #Cancel Button
            CancelButton = Button(NewStickWindow, text='Cancel', command= CloseWindow)
            CancelButton.place(x=190, y= 350, anchor='w')

            #Add Stick (Write Stick Data)
            AddStickButton = Button(NewStickWindow, text='Add Stick', command= AddStick)
            AddStickButton.place(x=290, y= 350, anchor='w')
            
            #Close Window Properly
            def on_closing():
                CloseWindow()
            NewStickWindow.protocol("WM_DELETE_WINDOW", on_closing)
    else:
        #If Window Open Inform User
        messagebox.showinfo('info', "Window already open!")
         
#Exicute Change_Export_Destination Setting
def Change_Export_Destination():
    global folder_selected
    folder_selected = filedialog.askdirectory()
    
    #DEBUGGING
    print(folder_selected)
    
    #Show File Destination on Main Window
    FileDestinationLabel = Label(root, text= 'File Destination: ' + folder_selected, width = 108, height= 1,font= ('Arial', 12))
    FileDestinationLabel.place(x=110, y=740)
    
    #Bolian
    DirectoryChosen.set('Chosen')
  
#Exicute Info
def Info ():
    #Show Program Verson
    messagebox.showinfo('info', str(Version.get()))
    
#Exicute Advanced_Settings
def Advanced_Settings():
    #Window Perameters
    AdvancedSettings = Toplevel()
    AdvancedSettings.title('Advanced Settings')
    AdvancedSettings.iconbitmap('wlkataiconIcon.ico')
    AdvancedSettings.geometry('600x400')
    AdvancedSettings.configure(background="#999999")
        
    #Exicute Restore to defalt Settings 
    def RestoreDefalts ():
        PickupOffset.set(2)
        BuildPlatformTilt.set(0.25)
        MaterialWidthMINSpec.set(0.5)
        MaterialWidthMAXSpec.set(0.5)
        BuildPlatformWidth.set(BuildSpaceXMM)
        BuildPlatformHeight.set(BuildSpaceYMM)
    
    #Buttons
    """""
    #Pickup Offset
    PickupOffsetLabel = Label(AdvancedSettings, text= 'Pickup Offset (mm)', font= ('Arial', 12))
    PickupOffsetLabel.place(x=15, y= 30, anchor='w')

    PickupOffsetEntry = Entry(AdvancedSettings, width = 10, fg = 'black', font= ('Arial', 12), textvariable = PickupOffset)
    PickupOffsetEntry.place(x=325, y= 30, anchor='w')"""""
    
    #Stick Pickup Zero Position
    StickPickupZeroPositionLabel = Label(AdvancedSettings, text= 'Pickup Zero Position (X,Y,Z,A,B,C) ', font= ('Arial', 12))
    StickPickupZeroPositionLabel.place(x=15, y= 30, anchor='w')

    #X
    StickPickupZeroPositionXEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable = PickupZeroPositionX, font= ('Arial', 12))
    StickPickupZeroPositionXEntry.place(x=325, y= 30, anchor='w')

    #Y
    StickPickupZeroPositionYEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable = PickupZeroPositionY, font= ('Arial', 12))
    StickPickupZeroPositionYEntry.place(x=365, y= 30, anchor='w')

    #Z
    StickPickupZeroPositionZEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable = PickupZeroPositionZ, font= ('Arial', 12))
    StickPickupZeroPositionZEntry.place(x=405, y= 30, anchor='w')

    #A
    StickPickupZeroPositionAEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable = PickupZeroPositionA, font= ('Arial', 12))
    StickPickupZeroPositionAEntry.place(x=445, y= 30, anchor='w')

    #B
    StickPickupZeroPositionBEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable = PickupZeroPositionB, font= ('Arial', 12))
    StickPickupZeroPositionBEntry.place(x=485, y= 30, anchor='w')

    #C
    StickPickupZeroPositionCEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable = PickupZeroPositionC, font= ('Arial', 12))
    StickPickupZeroPositionCEntry.place(x=525, y= 30, anchor='w')
    
    """"
    #Build Platform Tilt
    BuildPlatformTiltLabel = Label(AdvancedSettings, text= 'Build Platform Tilt (DEG)', font= ('Arial', 12))
    BuildPlatformTiltLabel.place(x=15, y= 65, anchor='w')

    BuildPlatformTiltEntry = Entry(AdvancedSettings, width = 10, fg = 'black', font= ('Arial', 12), textvariable = BuildPlatformTilt)
    BuildPlatformTiltEntry.place(x=325, y= 65, anchor='w')"""
    
    #Rest Position
    RestPositionLabel = Label(AdvancedSettings, text= 'Rest Position (J1,J2,J3,J4,J5,J6) ', font= ('Arial', 12))
    RestPositionLabel.place(x=15, y= 65, anchor='w')

    #X
    RestPositionXEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable= RestPositionJ1, font= ('Arial', 12))
    RestPositionXEntry.place(x=325, y= 65, anchor='w')

    #Y
    RestPositionYEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable= RestPositionJ2, font= ('Arial', 12))
    RestPositionYEntry.place(x=365, y= 65, anchor='w')

    #Z
    RestPositionZEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable= RestPositionJ3, font= ('Arial', 12))
    RestPositionZEntry.place(x=405, y= 65, anchor='w')

    #A
    RestPositionAEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable= RestPositionJ4, font= ('Arial', 12))
    RestPositionAEntry.place(x=445, y= 65, anchor='w')

    #B
    RestPositionBEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable= RestPositionJ5, font= ('Arial', 12))
    RestPositionBEntry.place(x=485, y= 65, anchor='w')

    #C
    RestPositionCEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable= RestPositionJ6, font= ('Arial', 12))
    RestPositionCEntry.place(x=525, y= 65, anchor='w')
    
    
    #Material Width Specifications
    MaterialWidthSpecLabel = Label(AdvancedSettings, text= 'Material Width Specifications (MIN)(MAX)', font= ('Arial', 12))
    MaterialWidthSpecLabel.place(x=15, y= 100, anchor='w')

    MaterialWidthMINSpecEntry = Entry(AdvancedSettings, width = 10, fg = 'black', font= ('Arial', 12), textvariable = MaterialWidthMINSpec)
    MaterialWidthMINSpecEntry.place(x=325, y= 100, anchor='w')
    
    MaterialWidthMAXSpecEntry = Entry(AdvancedSettings, width = 10, fg = 'black', font= ('Arial', 12), textvariable = MaterialWidthMAXSpec)
    MaterialWidthMAXSpecEntry.place(x=425, y= 100, anchor='w')
    
    
    #Build Platform Width
    BuildSpaceXMMLabel = Label(AdvancedSettings, text= 'Build Platform Width (MM)', font= ('Arial', 12))
    BuildSpaceXMMLabel.place(x=15, y= 135, anchor='w')

    BuildSpaceXMMEntry = Entry(AdvancedSettings, width = 10, fg = 'black', font= ('Arial', 12), textvariable = BuildPlatformWidth)
    BuildSpaceXMMEntry.place(x=325, y= 135, anchor='w')
    
    
    #Build Platform heigth
    BuildSpaceYMMLabel = Label(AdvancedSettings, text= 'Build Platform Heigth (MM)', font= ('Arial', 12))
    BuildSpaceYMMLabel.place(x=15, y= 170, anchor='w')

    BuildSpaceYMMEntry = Entry(AdvancedSettings, width = 10, fg = 'black', font= ('Arial', 12), textvariable = BuildPlatformHeight)
    BuildSpaceYMMEntry.place(x=325, y= 170, anchor='w')
    
    
    #Frame Lower Speed
    MovementSpeedLabel = Label(AdvancedSettings, text= 'Finished Frame Lower Speed ', font= ('Arial', 12))
    MovementSpeedLabel.place(x=15, y= 215, anchor='w')

    MovementSpeedSlider = Scale(AdvancedSettings, from_ = 10, to = 2000, orient= HORIZONTAL ,length=230)
    MovementSpeedSlider.set(2000)
    MovementSpeedSlider.place(x=325, y=195)
    
    
    #Build Platform Zero Position
    BuildPlatformZeroPositionLabel = Label(AdvancedSettings, text= 'Build Platform Zero Pos (X,Y,Z,A,B,C,A7) ', font= ('Arial', 12))
    BuildPlatformZeroPositionLabel.place(x=15, y= 260, anchor='w')

    #X
    BuildPlatformZeroPositionXEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable= BuildPlatformZeroPositionX, font= ('Arial', 12))
    BuildPlatformZeroPositionXEntry.place(x=325, y= 260, anchor='w')

    #Y
    BuildPlatformZeroPositionYEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable= BuildPlatformZeroPositionY, font= ('Arial', 12))
    BuildPlatformZeroPositionYEntry.place(x=360, y= 260, anchor='w')

    #Z
    BuildPlatformZeroPositionZEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable= BuildPlatformZeroPositionZ, font= ('Arial', 12))
    BuildPlatformZeroPositionZEntry.place(x=395, y= 260, anchor='w')

    #A
    BuildPlatformZeroPositionAEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable= BuildPlatformZeroPositionA, font= ('Arial', 12))
    BuildPlatformZeroPositionAEntry.place(x=430, y= 260, anchor='w')

    #B
    BuildPlatformZeroPositionBEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable= BuildPlatformZeroPositionB, font= ('Arial', 12))
    BuildPlatformZeroPositionBEntry.place(x=465, y= 260, anchor='w')

    #C
    BuildPlatformZeroPositionCEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable= BuildPlatformZeroPositionC, font= ('Arial', 12))
    BuildPlatformZeroPositionCEntry.place(x=500, y= 260, anchor='w')
    
    #A7
    BuildPlatformZeroPositionA7Entry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable= BuildPlatformZeroPositionA7, font= ('Arial', 12))
    BuildPlatformZeroPositionA7Entry.place(x=535, y= 260, anchor='w')
    
    
    #Build Platform Max Position
    BuildPlatformMaxPositionLabel = Label(AdvancedSettings, text= 'Build Platform Max Pos (X,Y,Z,A,B,C,A7) ', font= ('Arial', 12))
    BuildPlatformMaxPositionLabel.place(x=15, y= 295, anchor='w')

    #X
    BuildPlatformMaxPositionXEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable= BuildPlatformMaxPositionX, font= ('Arial', 12))
    BuildPlatformMaxPositionXEntry.place(x=325, y= 295, anchor='w')

    #Y
    BuildPlatformMaxPositionYEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable= BuildPlatformMaxPositionY, font= ('Arial', 12))
    BuildPlatformMaxPositionYEntry.place(x=360, y= 295, anchor='w')

    #Z
    BuildPlatformMaxPositionZEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable= BuildPlatformMaxPositionZ, font= ('Arial', 12))
    BuildPlatformMaxPositionZEntry.place(x=395, y= 295, anchor='w')

    #A
    BuildPlatformMaxPositionAEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable= BuildPlatformMaxPositionA, font= ('Arial', 12))
    BuildPlatformMaxPositionAEntry.place(x=430, y= 295, anchor='w')

    #B
    BuildPlatformMaxPositionBEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable= BuildPlatformMaxPositionB, font= ('Arial', 12))
    BuildPlatformMaxPositionBEntry.place(x=465, y= 295, anchor='w')

    #C
    BuildPlatformMaxPositionCEntry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable= BuildPlatformMaxPositionC, font= ('Arial', 12))
    BuildPlatformMaxPositionCEntry.place(x=500, y= 295, anchor='w')
    
    #A7
    BuildPlatformMaxPositionA7Entry = Entry(AdvancedSettings, width = 3, fg = 'black', textvariable= BuildPlatformMaxPositionA7, font= ('Arial', 12))
    BuildPlatformMaxPositionA7Entry.place(x=535, y= 295, anchor='w')
    
    
    #Restore Defalts
    CancelButton = Button(AdvancedSettings, text='Restore Defalts', command= RestoreDefalts)
    CancelButton.place(x=190, y= 350, anchor='w')


    #Save and Close (Settings are Saved Once Changed)
    CancelButton = Button(AdvancedSettings, text='Save and Close', command= AdvancedSettings.destroy)
    CancelButton.place(x=290, y= 350, anchor='w')
    
    
    #How do I Find Zeros? (Opens window containing info on how to find zeros)
    ZerosInfoButton = Button(AdvancedSettings, text='How Do I Find Zeros?', command= ZerosInfoWindow)
    ZerosInfoButton.place(x=435, y= 350, anchor='w')
    
#Top Menu
my_menu = Menu(root)
root.config(menu = my_menu)

#File Menu (1)
file_menu = Menu(my_menu, tearoff= 0)
my_menu.add_cascade(label = 'File', menu = file_menu)
file_menu.add_command(label= 'Change Export Destination', command= Change_Export_Destination)


#Settings Menu (2)
settings_menu = Menu(my_menu, tearoff= 0)
my_menu.add_cascade(label= 'Settings', menu = settings_menu)
settings_menu.add_command(label = 'Advanced Settings', command= Advanced_Settings)


#Help Menu (3)
Help_menu = Menu(my_menu, tearoff= 0)
my_menu.add_cascade(label= 'Help', menu = Help_menu)
Help_menu.add_command(label = 'About', command= Info)

Help_menu.add_command(label = 'Exit', command= root.destroy)

#Home Page Settings
#Update Preview
UpdatePreviewButton = Button (root, text='Update', command= UpdatePreview, font= ('Arial', 15), bg= '#C0C0C0')
UpdatePreviewButton.place(x= 900, y= 30, width= 275, height= 75)

#New Stick
NewStickButton = Button (root, text='New Stick', command= NewStick, font= ('Arial', 15), bg= '#C0C0C0')
NewStickButton.place(x= 575, y= 30, width= 275, height= 75)

#Glue Set Time
GlueSetTimeLabel = Label(root, text= 'Glue Set Time (Sec) ', font= ('Arial', 15))
GlueSetTimeLabel.place(x=15, y= 30, anchor='w')

GlueSetTimeEntry = Entry(root, width = 10, fg = 'black', textvariable = GlueSetTime, font= ('Arial', 15))
GlueSetTimeEntry.place(x=325, y= 30, anchor='w')

#Matertial Width
MaterialWidthLabel = Label(root, text= 'Material Width (MM)', font= ('Arial', 15))
MaterialWidthLabel.place(x=15, y= 65, anchor='w')

MaterialWidthEntry = Entry(root, width = 10, fg = 'black', textvariable = MaterialWidth, font= ('Arial', 15))
MaterialWidthEntry.place(x=325, y= 65, anchor='w')

"""
#Stick Pickup Position
StickPickupPositionLabel = Label(root, text= 'Pickup Position (X,Y,Z,A,B,C) ', font= ('Arial', 15))
StickPickupPositionLabel.place(x=15, y= 100, anchor='w')

#X
StickPickupPositionXEntry = Entry(root, width = 3, fg = 'black', textvariable = PickupPositionX, font= ('Arial', 15))
StickPickupPositionXEntry.place(x=325, y= 100, anchor='w')

#Y
StickPickupPositionYEntry = Entry(root, width = 3, fg = 'black', textvariable = PickupPositionY, font= ('Arial', 15))
StickPickupPositionYEntry.place(x=365, y= 100, anchor='w')

#Z
StickPickupPositionZEntry = Entry(root, width = 3, fg = 'black', textvariable = PickupPositionZ, font= ('Arial', 15))
StickPickupPositionZEntry.place(x=405, y= 100, anchor='w')

#A
StickPickupPositionAEntry = Entry(root, width = 3, fg = 'black', textvariable = PickupPositionA, font= ('Arial', 15))
StickPickupPositionAEntry.place(x=445, y= 100, anchor='w')

#B
StickPickupPositionBEntry = Entry(root, width = 3, fg = 'black', textvariable = PickupPositionB, font= ('Arial', 15))
StickPickupPositionBEntry.place(x=485, y= 100, anchor='w')

#C
StickPickupPositionCEntry = Entry(root, width = 3, fg = 'black', textvariable = PickupPositionC, font= ('Arial', 15))
StickPickupPositionCEntry.place(x=525, y= 100, anchor='w')"""""

#Pickup Offset
PickupOffsetLabel = Label(root, text= 'Pickup Offset (mm)', font= ('Arial', 15))
PickupOffsetLabel.place(x=15, y= 100, anchor='w')

PickupOffsetEntry = Entry(root, width = 10, fg = 'black', font= ('Arial', 15), textvariable = PickupOffset)
PickupOffsetEntry.place(x=325, y= 100, anchor='w')


#Frame Drop Off Position
FrameDropOffPositionLabel = Label(root, text= 'Frame Drop Off Position (X,Y) ', font= ('Arial', 15))
FrameDropOffPositionLabel.place(x=15, y= 135, anchor='w')

#X
FrameDropOffPositionXEntry = Entry(root, width = 3, fg = 'black', textvariable = FrameDropOffPositionX, font= ('Arial', 15))
FrameDropOffPositionXEntry.place(x=325, y= 135, anchor='w')

#Y
FrameDropOffPositionYEntry = Entry(root, width = 3, fg = 'black', textvariable = FrameDropOffPositionY, font= ('Arial', 15))
FrameDropOffPositionYEntry.place(x=365, y= 135, anchor='w')


#Movement Speed
MovementSpeedLabel = Label(root, text= 'Movement Speed ', font= ('Arial', 15))
MovementSpeedLabel.place(x=15, y= 555, anchor='w')

MovementSpeedSlider = Scale(root, from_ = 10, to = 2000, orient= HORIZONTAL ,length=230)
MovementSpeedSlider.set(2000)
MovementSpeedSlider.place(x=225, y=535)

#Mirobot Logo Image
MirobotLogoImage = ImageTk.PhotoImage(Image.open('WlkataLogo.png'))
label = Label(root, image = MirobotLogoImage )
label.place(x=15, y=620)


#Set Program Name
SetProgramNameEntry= Entry(root, width = 40, textvariable = SetProgramName, fg = 'black', font= ('Arial', 15))
SetProgramNameEntry.place(x=15, y=585)

#File Destination
FileDestinationLabel = Label(root, text= 'Chose File to set File Destination', width = 108, height= 1,font= ('Arial', 12))
FileDestinationLabel.place(x=110, y=740)



#Canvas Pannel
panel_1= PanedWindow(bd = 4, relief= 'sunken', bg = '#d9dade')
panel_1.place(x=575, y=125, width = 600, height= 600)

#Create Canvas
MyCanvas = Canvas(root, width=590, height=590, bg='white')
MyCanvas.place(x=580, y=130)

#Add Image to Canvas
img = PhotoImage(file="images/Frame Building Canvas.png")
MyImage = MyCanvas.create_image(30,40, anchor=NW, image=img)
        
#Update Preview
UpdatePreview();
 
#Stick Pannel
panel_2= PanedWindow(bd = 4, relief= 'sunken', bg = 'white')
panel_2.place(x=15, y=160, width = 550, height= 310)


#Delete Selected Sticks
DeleteClickedOnSticksButton = Button (root, text='Delete Selected', command= DeleteClickedOnSticks, font= ('Arial', 15), bg= 'red')
DeleteClickedOnSticksButton.place(x= 15, y= 475, width= 275, height= 50)


#Generate GCode
GenerateGcodeButton = Button (root, text='Generate GCode', command= GenerateGCode, font= ('Arial', 15), bg= '#ce5912')
GenerateGcodeButton.place(x= 810, y= 780, width= 275, height= 75)


#Generate Stick Feed Order
GenerateStickFeedButton = Button (root, text='Generate Stick Feed Order', command= GenerateStickFeed, font= ('Arial', 15), bg= '#00FFFF')
GenerateStickFeedButton.place(x= 110, y= 780, width= 375, height= 75)


mainloop()
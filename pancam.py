# Python pan/tilt camera prog

import sys
import os
import time
import random
import pigpio

import picamera

MIN_WIDTH=1000
MAX_WIDTH=2000

pi = pigpio.pi()
camera = picamera.PiCamera( )

if not pi.connected:
    exit()

class FileMaker( ):
    # constructing this generates the first filename
    def __init__(self, baseName, startFileNum):
        self.baseName = baseName
        self.fileNumber = startFileNum 
        self.filename = self.baseName + '_' + str( self.fileNumber)
        
    def nextFileName(self):
        filename = self.filename
        self.fileNumber = self.fileNumber + 1
        self.filename = self.baseName + '_' + str( self.fileNumber)
        return filename + '.jpg'
        
class FolderMaker ( ):
    # constructing this also makes the first folder and cds to it
    def __init__(self, baseName, startFolderNum):
        self.baseName = baseName
        self.folderNum = startFolderNum
        self.currFolderName = baseName + '_' + str(self.folderNum)
        if not os.path.isdir(self.currFolderName):
            os.makedirs(self.currFolderName)
        os.chdir (self.currFolderName )
    
    # Pop up one dir, then create the next dir in the sequence
    def nextFolder(self):
        os.chdir ( '..' )
        self.folderNum = self.folderNum + 1
        self.currFolderName = self.baseName + '_' + str(self.folderNum)
        if not os.path.isdir(self.currFolderName):
            os.makedirs(self.currFolderName)
        os.chdir (self.currFolderName )
            
        
class Servo ( ):
    def __init__(self, name, pin, posSettings):
        self.name = name 
        self.positions = posSettings
        self.currPos = 0 
        self.pin = pin 
        pi.set_servo_pulsewidth( self.pin, 0 ) # off to start

    def move ( self, posNum ):
        self.currPos = self.positions[posNum]
        pi.set_servo_pulsewidth(self.pin, self.currPos)

    def servoClose(self):
        self.currPos = 0 
        pi.set_servo_pulsewidth( self.pin, 0 ) # off

def main( ):
    xAxisGPIOPin = 23 # Check these
    yAxisGPIOPin = 24 # Check these
    horizontalPositions = [1250, 1500, 1750]
    verticalPositions = [1250, 1500, 1750]
    horizontal = Servo ( "Xaxis", xAxisGPIOPin, horizontalPositions)
    vertical = Servo ( "Yaxis", yAxisGPIOPin, verticalPositions)

    folder = FolderMaker('images', 0)
    file = FileMaker('img', 0)
    for h in range(3):
        for v in range(3):
            horizontal.move(h)
            vertical.move(v)
            time.sleep(1)
            camera.capture(file.nextFileName())
			
	
	
    # Test horizontal movement
    #print( "Staring X axis test")
    #horizontal.move( 0 )
    #time.sleep( 1 )
    #horizontal.move( 1 )
    #time.sleep( 1 )
    #horizontal.move( 2 )
    #time.sleep( 1 )
    #horizontal.servoClose ( )
    #print ( "Done X axis test")

    # Test vertical movement
    #print( "Starting Y axis test")
    #vertical.move( 0 )
    #time.sleep( 1 )
    #vertical.move( 1 )
    #time.sleep( 1 )
    #vertical.move( 2 )
    #time.sleep( 1 )
    #vertical.servoClose ( )
    #print( "Done Y axis test")

   

if __name__ == "__main__":
    main ( )

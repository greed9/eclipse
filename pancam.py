# Python pan/tilt camera prog

import sys
import os
import time
import random
import pigpio
import argparse
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
        self.fileNumber = int(self.fileNumber) + 1
        #if (self.fileNumber < 10):
        #    self.fileNumber = '0' + str(self.fileNumber)
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

    parser = argparse.ArgumentParser(description='Please use -img and -folder')
    parser.add_argument('-img',dest='images',
                    help='an integer for the accumulator')

    parser.add_argument('-folder',dest='folder',
                        help='an integer for the accumulator')

    args = parser.parse_args()
    
    
    xAxisGPIOPin = 24 # Check these
    yAxisGPIOPin = 23 # Check these
    #horizontalPositions = [650, 750, 1000, 1200, 1400, 1600, 1800, 2000]
    #verticalPositions = [1200, 1300, 1400, 1600, 1800, 2000, 2200, 2400]
    horizontalPositions = [1000, 1200, 1400, 1600, 1800, 2000]
    verticalPositions = [1400, 1500, 1600, 1700, 1800, 1900]
    horizontal = Servo ( "Xaxis", xAxisGPIOPin, horizontalPositions)
    vertical = Servo ( "Yaxis", yAxisGPIOPin, verticalPositions)
    
    horizontal.servoClose()
    vertical.servoClose()

    folder = FolderMaker(args.folder, 0)
    file = FileMaker(args.images, 0)
    for v in range(len(horizontalPositions)):
        for h in range(len(verticalPositions)):
            horizontal.move(h)
            vertical.move(v)
            time.sleep(2)
            camera.capture(file.nextFileName())
			
	
    horizontal.servoClose()
    vertical.servoClose()
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
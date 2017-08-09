import serial
import sys

class Command:
	def __init__(self, line):
		arr = line.split(',')
		self.name, self.millis, self.pin, self.data = arr
		
	def printString(self):
		_name = self.name
		_millis = self.millis
		_pin = self.pin
		_data = self.data
		spaces = 15
		print (_name.ljust(spaces) + '\t' + _millis.ljust(spaces) + '\t' + _pin.ljust(spaces) + '\t'+  _data.ljust(spaces))


def main():
	ser = serial.Serial('/dev/ttyACM0', 9600)
	while(True):
		line =  str(ser.readline())
		line = line[2:-5]
		try:
			command = Command(line)
			command.printString()
		except:
			print('BAD LINE ' + line + ' EXCEPTION ' + str(sys.exc_info()[0]))
		
	

if __name__ == '__main__':
	main()

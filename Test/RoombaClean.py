import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

if not ser.isOpen():
	ser.open()

ser.isOpen()

ser.write(chr(0x80))	# Start
ser.write(chr(0x83))	# Safe
ser.write(chr(0x87))	# Clean

ser.close()
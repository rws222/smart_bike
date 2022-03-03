# Camera
import jetson.inference
import jetson.utils
import argparse
import sys

# Distance sensor
import serial
import time

# Camera setup
is_headless = ["--headless"] if sys.argv[0].find('console.py') != -1 else [""]
try:
	opt = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)
# create video output object 
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv+is_headless)
# load the object detection network
net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)
# create video sources
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)

# Distance sensor serial setup
ser = serial.Serial("/dev/ttyTHS1", 115200)

# process frames until the user exits
while True:
	# Camera
	# capture the next image
	img = input.Capture()
	# detect objects in the image (with overlay)
	detections = net.Detect(img, overlay=opt.overlay)
	# print the detections
	print("detected {:d} objects in image".format(len(detections)))
	for detection in detections:
		print(detection)
	# render the image
	output.Render(img)
	# update the title bar
	output.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS()))
	# print out performance info
	net.PrintProfilerTimes()

	
	
	# Distance sensor
        count = ser.in_waiting
        if count > 8:
            recv = ser.read(9)  
            ser.reset_input_buffer()  
            
            if recv[0] == 0x59 and recv[1] == 0x59:     #python3
                distance = recv[2] + recv[3] * 256
                strength = recv[4] + recv[5] * 256
                print('(', distance, ',', strength, ')')
                ser.reset_input_buffer()
	
	
	
	
	
	# exit on input/output EOS
	if not input.IsStreaming() or not output.IsStreaming():
		break


        
if __name__ == '__main__':
    try:
        if ser.is_open == False:
            ser.open()
        getTFminiData()
    except KeyboardInterrupt:   # Ctrl+C
        if ser != None:
            ser.close()

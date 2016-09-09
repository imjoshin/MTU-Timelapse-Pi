#local storage
LOCAL="/home/pi/MTU-Timelapse"

#in minutes. 60 % interval must be 0
INTERVAL=5

#time between failed uploads
FAILTIME=5
#retry count
RETRYCOUNT=3

CMD="raspistill -o '/home/pi/MTU-Timelapse/cam/%s/%s-%s.jpg'  -hf -vf -h 1080 -w 1920 --nopreview --timeout 1"

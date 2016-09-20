from time import sleep
from subprocess import call
from datetime import datetime
import auth, settings, os, paramiko, time, sys, signal, errno, socket
from threading import Thread


def main():
	ts = time.time()
	with open("/home/pi/cam.log", "a") as myfile:
    		myfile.write("Started at %s\n" % datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
	while(True):
		while(datetime.now().minute % settings.INTERVAL != 0):
			sleep(1)

		hour = datetime.now().strftime("%H")
		minute = datetime.now().strftime("%M")
		date = datetime.now().strftime("%m-%d-%y")

		directory = "%s/cam/%s" % (settings.LOCAL, date)
		if not os.path.exists(directory):
			os.makedirs(directory, mode=0777)

		call(settings.CMD % (date, hour, minute), shell=True)
		os.chmod("%s/%s-%s.jpg" % (directory, hour, minute), 777)
		sleep(65)


def sync():
	while True:
		try:
			tp = paramiko.Transport((auth.IP, 22))
			tp.connect(username = auth.USER, password = auth.PASS)
			sftp = paramiko.SFTPClient.from_transport(tp)
		except:
			print "\033[31mError\033[0m connecting to internet"
			sleep(settings.FAILTIME)
			continue

		#iterate through directories and create
		for d in getDirectories("%s/cam/" % settings.LOCAL):
			#if directory creation failed, skip upload
			if not createDir(sftp, "%s/%s" % (auth.REMOTE, d)):
				continue
			#iterate through files and upload
			for f in os.listdir("%s/cam/%s" % (settings.LOCAL, d)):
				uploadFile(sftp, "cam/%s" % (d), f, "%s/%s/%s" % (auth.REMOTE, d, f))
			#delete directory if empty
			if len(os.listdir("%s/cam/%s" % (settings.LOCAL, d))) is 0:
				os.rmdir("%s/cam/%s" % (settings.LOCAL, d))

		sftp.close()
		tp.close()
		sleep(30)

def uploadFile(sftp, directory, file, remote):
	#file is remote file, directory is local directory where it is stored

	#try to upload 3 times
	for i in range(0, settings.RETRYCOUNT):
		try:
			#upload and remove
			sftp.put("%s/%s/%s" % (settings.LOCAL, directory, file), remote)
			os.remove("%s/%s/%s" % (settings.LOCAL, directory, file))
			print "File \033[32m%s\033[0m uploaded successfully to \033[36m%s/%s\033[0m." % (file, auth.REMOTE, directory.replace("cam/", ""))
			break
		except:
			print "\033[31mError\033[0m uploading file \033[32m%s\033[0m to \033[36m%s/%s\033[0m." % (file, auth.REMOTE, directory.replace("cam/", ""))
			sleep(settings.FAILTIME)
			continue

def createDir(sftp, directory):
	#check if directory exists
	try:
		sftp.stat("%s" % (directory))
		return True
	except IOError, e:
		if e.errno == errno.ENOENT:
			print "Directory \033[32m%s\033[0m doesn't exist!" % (directory)

	#try to create it
	for i in range(0, settings.RETRYCOUNT):
		try:
			sftp.mkdir(directory)
			print "Directory \033[32m%s\033[0m created successfully." % (directory)
			return True
		except:
			print "\033[31mError\033[0m creating directory \033[32m%s\033[0m." % (directory)
			sleep(settings.FAILTIME)
			continue

	return False

def getDirectories(a_dir):
    return [name for name in os.listdir(a_dir)
        if os.path.isdir(os.path.join(a_dir, name))]

def signal_handler(signal, frame):
	os.system("pkill -9 python")
	sys.exit(0)



signal.signal(signal.SIGINT, signal_handler)

thread = Thread(target = sync, args = ())
thread.start()

main()

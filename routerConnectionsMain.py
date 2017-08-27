#Important libraries
import telnetlib
import time
import datetime
import os

#Actual class file
import roomate

#Top secret variables and names ;)
import connectionInfo
#Devices is a dictionary of mac addresses (string) correlating to device names(strings)
#macX is the mac address of roomate X's phone (string)
from association import devices,macD,macM,macB,macG,macA

def main():
	#Change this to stop visualization
	VISUALIZE = True

	dataFolder = os.path.join(os.getcwd(),"Data")
	if not os.path.exists(dataFolder):
		os.makedirs(dataFolder)
		os.makedirs(os.path.join(dataFolder,'Logs'))
		os.makedirs(os.path.join(dataFolder,'Charts'))

	logFolder = os.path.join(dataFolder,'Logs')
	chartFolder = os.path.join(dataFolder,'Charts')

	rm1 = roomate.Roomates(macD)
	rm2 = roomate.Roomates(macM)
	rm3 = roomate.Roomates(macB)
	rm4 = roomate.Roomates(macG)
	rm5 = roomate.Roomates(macA)

	roomies = [rm1,rm2,rm3,rm4,rm5]

	#Attempt to connect to router
	try:
		tn = telnetlib.Telnet('192.168.1.1')
		connectDriver = connectionInfo.connect()

		user = connectDriver.get_user()
		passW = connectDriver.get_pass()

		tn.read_until(b"login: ")
		tn.write(user.encode('ascii')+b"\n")

		tn.read_until(b"Password: ")
		tn.write(passW.encode('ascii')+b"\n")

		tn.write(b"wl -i eth1 assoclist | cut -d' ' -f2\n")
		tn.write(b"wl -i eth2 assoclist | cut -d' ' -f2\n")
		tn.write(b"exit\n")

		allText=(tn.read_all().decode('ascii'))

		macAdr = list([x for x in allText.replace('\n','').split('\r') if len(x)==17])
		macStr = ''
		for adr in macAdr:
			macStr+=str(adr)+', '
		macStr=macStr[:-2]
		connectionError = False

	#If program could not connect to router
	except OSError:
		connectionError = True
		print("Connection Error")

	#Get date and time info
	now = datetime.datetime.now()
	today = now.strftime('%Y-%m-%d')
	currTime = now.strftime('%H:%M:%S')

	#Check if today's log file exists
	try:
		file = open(os.path.join(logFolder,today+'-logs.txt'),'r')

		lines = file.readlines()
		file.close()
		
		#Get information on who was justs previously here and not here
		prevStatus = lines[-1]
		prev = True

	#If no log file for today exists
	except FileNotFoundError:
		yesterday = (now - datetime.timedelta(days = 1)).strftime('%Y-%m-%d')
		print("Need %s data" % yesterday)
		print('Creating new file')
		prev = False

#Create a visualization chart
#----------------------------------------------------------------------------------------------------
	if VISUALIZE:
		try:
			vis = open(os.path.join(chartFolder,today+'-chart.txt'),'r')
			vis.close()
			vis = open(os.path.join(chartFolder,today+'-chart.txt'),'a')

		except FileNotFoundError:
			vis = open(os.path.join(chartFolder,today+'-chart.txt'),'a')
			vis.write(' Time | Davi | Matt | Brnt | Gabe | Andy |\n')
			vis.write('------------------------------------------\n')

#----------------------------------------------------------------------------------------------------

	#Create today's log file
	file = open(os.path.join(logFolder,today+'-logs.txt'),'a')
	#If connected to router
	if not connectionError:

#----------------------------------------------------------------------------------------------------
		#Fill out visualization chart
		if VISUALIZE:
			vis.write(currTime[:-3]+' ')
			if prev:
				for friendo in roomies:
					friendo.update(prevStatus,macAdr,currTime)
					if friendo.is_here():
						vis.write('|      ')
					else:
						vis.write('|XXXXXX')
				vis.write('|\n')

#----------------------------------------------------------------------------------------------------			

		#If previous status data exists
		if prev:
			for friend in roomies:
				friend.update(prevStatus,macAdr,currTime)
				if friend.is_here():
					print(devices[friend.get_mac()],'is here')

					if friend.just_arrived():
						print(devices[friend.get_mac()],'just got home')

				else:
					print(devices[friend.get_mac()],'is away')
					if friend.just_left():
						print(devices[friend.get_mac()],'just left')

		#Wait till next check
		else:
			print('Gathering info')

		#Update the log file with present MAC addresses
		file.write(currTime+', '+macStr+'\n')

		#Visual que
		if prev:
			print("data saved at ",currTime,'\n')

	#Update log file with no connection error
	else: 
		file.write(currTime+',!Server could not be reached\n')
	vis.close()
	file.close()

#Tester until cron file
while(True):
	main()
	time.sleep(30)
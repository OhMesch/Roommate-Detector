#Important libraries
import telnetlib
import time
import datetime

#Actual class file
import roomate

#Top secret variables and names ;)
import connectionInfo
from association import devices,macD,macM,macB,macG,macA

def main():

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
		file = open(today+'-logs.txt','r')
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

	#Create today's log file
	file = open(today+'-logs.txt','a')

	#If connected to router
	if not connectionError:

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
					# print(devices[friend.get_mac()],'last seen:'+friend.last_seen())
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
	file.close()

#Tester until cron file
while(True):
	main()
	time.sleep(30)
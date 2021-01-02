import sys
import socket
import struct

serverIP=sys.argv[1]
serverPort=int(sys.argv[2])

serSocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serSocket.bind((serverIP, serverPort))

dnsDict={}
with open("dns-master.txt") as f:
	for line in f:
		lineSplit=line.split(" ")
				
		if len(lineSplit)==5:			
			dnsDict[lineSplit[0]]=[lineSplit[1], lineSplit[2], lineSplit[3], lineSplit[4]]	
			

while True:
	data, addr=serSocket.recvfrom(1024)		
	cliMsgType, cliRetCode, cliMsgId, cliQuestLen, cliAnsLen, cliQuestion=struct.unpack('>HHIHH'+str((len(data)-12))+'s', data)
	serAns=""
	
	dnsLookup=dnsDict.get(cliQuestion.decode().split(" ")[0])
		
	if dnsLookup==None:
		cliRetCode=1
		#print("oh no big yikes")
	else:
		cliRetCode=0	
		serAns=cliQuestion.decode()+" "+dnsLookup[2]+" "+dnsLookup[3]	
		
	serSocket.sendto(struct.pack('>HHIHH'+str((len(data)-12))+'s'+str(len(serAns))+'s',2, cliRetCode, cliMsgId, cliQuestLen, len(serAns), cliQuestion, serAns.encode()), addr)
	
	
	
	

	

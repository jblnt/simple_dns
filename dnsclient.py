import sys
import socket
import struct
import random

destServerIP=sys.argv[1]
destServerPort=int(sys.argv[2])
destQuery=(sys.argv[3])+" A IN"
destQueryLen=len(destQuery)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.settimeout(1)

msgId=random.randrange(1,101)
verbose=timedOut=True
serMsgType=serRetCode=serMsgId=serQuestLen=serAnsLen=0
serQuestion=serAns=""

def printOut(mId, qL, q):
	print("\n"+"Message ID: "+str(mId)+"\nQuestion Length: "+str(qL)+" bytes\nAnswer Length: 0 bytes\nQuestion: "+q)
	
def printIn(dsi, dsp, rtCode, mId, qL, aL, q, a):
	print("\nReceived Response from: "+dsi+", "+str(dsp))
	
	if rtCode==0:
		print("Return Code: "+str(rtCode)+" (No Errors)")
		
	else:
		print("Return COde: "+str(rtCode)+" (Name does not exist)")
		
	
	print("Message ID: "+str(mId)+"\nQuestion Length: "+str(qL)+" bytes\nAnswer Length: "+str(aL)+" bytes\nQuestion: "+q.decode())
	
	if aL!=0:
		print("Answer: "+a.decode(), end='')
		

for i in range (3):	
	print("Sending Request to: "+destServerIP+", "+str(destServerPort), end='')
	
	if verbose:
		printOut(msgId, destQueryLen, destQuery)
		
	clientSocket.sendto((struct.pack('>HHIHH'+str(destQueryLen)+'s',1,0,msgId,destQueryLen,0,destQuery.encode())),(destServerIP,destServerPort))
	
	try:
		data, addr=clientSocket.recvfrom(1024)
		serMsgType, serRetCode, serMsgId, serQuestLen, serAnsLen, serQuestion, serAns=struct.unpack('>HHIHH'+str(destQueryLen)+'s'+str(len(data)-(12+destQueryLen))+'s', data)
						
	except:
		print("\nServer Timedout...")
		verbose=False
		continue
	
	timedOut=False
	break

if timedOut==False:
	printIn(destServerIP, destServerPort, serRetCode, serMsgId, serQuestLen, serAnsLen, serQuestion, serAns)	

clientSocket.close()





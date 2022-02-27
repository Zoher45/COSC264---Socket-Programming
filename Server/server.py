""" 
This is the server code for socket programming. It's job is to communication with the client and provide the required assistance. It follows the transmission control protocol (TCP).

Author : Zoher Hussein
"""

import socket
import datetime
import sys


def packetFileResponse():
    """
    This function processes the files into required packets.
    """
    pass

def connectionProcessing(s, port):
    """
    Does the process after a connection is established. Essentially an infine loop unit closed or some error has occured.
    """
    currentTime = datetime.datetime.now()
    while True:
        print("\nServer is waiting for incoming connection")
        client, address = s.accept()
        
        client.settimeout(1) #Ensuring no gaps will occur
        
        print("Connection received at {0}. IP address {1}. Port Number {2}".format(currentTime.strftime('%H:%M'), address, port))
        
        #The bytearray of information about the file type --> Header + 1024 (max length of the file name)
        receivedPacket = client.recv(1029)
        
        if len(receivedPacket) <= 5:
            print("The packet header does not match the minimum required bytes")
            client.close()
            
        else:
            #header parts 
            magicNo = receivedPacket[0] << 8 | (receivedPacket[1] & 0xFF)
            fileLen = receivedPacket[3] << 8 | (receivedPacket[4] & 0xFF)
            
            if magicNo!= 0x497E:
                print("The 'MagicNo' provided is incorrect")
                client.close()                
        
            elif receivedPacket[2] != 1:
                print("The 'Type' provided is incorrect")
                client.close()
                
            elif (fileLen < 1 or fileLen > 1024):
                print("The filename length given is not within the range (1 - 1024)")
                client.close()
                
            #The header has the correct information
            else:
                #Find the file name
                filename = receivedPacket[5:].decode('utf-8')
                statusCode = 0x1
                
                
                
                try:
                    openFile = open(filename, "rb")
                    byteTransferFile = openFile.read()
                
                except OSError as osErr:
                    statusCode = 0x0
                    print("OS error occured:", osErr)
            
                
                except BufferError as buffErr:
                    statusCode = 0x0
                    print("Buffer error occured:", buffErr)
                
                    
                except:
                    statusCode = 0x0
                    print("Error occured, client socket will be closed")
                    
                    
                    
                #Header
                magicNo = 0x497E
                
                
                bytearrayList = bytearray()
                
                bytearrayList.append((magicNo >> 8))
                bytearrayList.append((magicNo & 0xFF))
                bytearrayList.append((0x2))
                bytearrayList.append((statusCode))
             
                    
                if statusCode == 0:
                    client.send(bytearrayList)
                    
                else:
                    #The content of the file
                    fileDataBytes = bytearray(byteTransferFile)                    
                    
                    fileDataLen = len(fileDataBytes)
                    
                    bytearrayList.append((fileDataLen >> 24))
                    bytearrayList.append((fileDataLen >> 16 & 0xFF))
                    bytearrayList.append((fileDataLen >> 8 & 0xFF))
                    bytearrayList.append((fileDataLen & 0xFF))   
                    
                    
                    client.send((bytearrayList + fileDataBytes))
                    openFile.close()
                    print("\nThe total amount of bytes transerfered was - {} Bytes".format(fileDataLen))
                    
                    
                   
                client.close()
                
                
def getPortNumber():
    """
    Gets the port number from the user
    """
    portNumber = sys.argv
    
    try:
        portNumber = int(portNumber[1])
        
        
    except:
        print("Port number given was not a number")
        sys.exit()
        
    else:
        if portNumber < 1024 or portNumber > 64000:
            print("Port number not within range")
            sys.exit()
        
    return portNumber

def createSocket():
    """
    Create the socket. If error occurs make the users aware of error and exit.
    """
    
    try:
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as error:
        print("Socket Creation failed: {}".format(error))
        sys.exit()
    print("Socket creation was successful")
    return new_socket

 
    
def main():
    """
    main fuction for the server. This is where all the functionality is controlled.
    """
    
    #Users port number
    portNumber = getPortNumber()
    
    #Creating socket
    soc = createSocket()
    
    #Error handling when binding
    try:
        #Bind the port number to the socket
        soc.bind(('', portNumber))
    except:
        print("An error has occured while binding")
        sys.exit()
    
    #Error handling when listening
    try:
        #Socket gorslistening mode
        soc.listen()
    except:
        print("An error has occured while listening for client")
        soc.close()
        sys.exit()
        
    connectionProcessing(soc, portNumber)
    
main()
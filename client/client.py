""" 
This is the client code for socket programming. The cilent side tries to connect with the server and retrive required data. It follows the transmission control protocol (TCP).

Author : Zoher Hussein
"""

import socket 
import sys
import os.path

def startConnection():
    """
    This funciton is for user input about there host name. If errors occur, there will be an error message. Then after the program will close.
    """
    userInfo = sys.argv
   
    #Checks in user input is the required inputs
    if len(userInfo) > 4 or len(userInfo) <= 3:
        print("Parameters does not match the requirement (IP, portnumber and file)")
        sys.exit()
    else:
        #check if the port number given is correct
        try:
            portNumber = int(userInfo[2])
            
            
        except:
            print("Port number given was not a number")
            sys.exit()
            
        else:
            if portNumber < 1024 or portNumber > 64000:
                print("Port number not within range")
                sys.exit()        
        
        #check if the given IP/hostname is valid
        try:
            ip = socket.gethostbyname(userInfo[1])
        except:
            print("Wrong IP/hostname provided")
            sys.exit()
            
        
        if os.path.isfile(str(userInfo[3])):
            print("File is already in directory")
            sys.exit()
            
    
        
        #Caputres the addres information
        addressInformation = socket.getaddrinfo(ip, portNumber)
        
            
        return addressInformation, ip, portNumber, userInfo[3]

def createSocket():
    """
    Creates the socket. If error occurs, notify user.
    """
    try:
        newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        newSocket.settimeout(1)
    except socket.error as error:
        print("Socket Creation failed: {}".format(error))
        sys.exit()
    else:
        print("Socket creation was successful")
    
    return newSocket
        
def establishConnection(soc, ipAddress, portNum):
    """
    This function is used to connect to the server. If connection fails then print error message
    """
    try:
        soc.connect((ipAddress, portNum))
    except:
        print("Connection failed")
        sys.exit()
        
def fileRequestPackaging(file):
    """
    This function is where the file request for the server gets prepared
    """
    
    magicNo = 0x497E
    filenameBytes = file.encode('utf-8')
    filenameLen = len(filenameBytes)
    
    
    bytearrayList = bytearray()
    
    bytearrayList.append((magicNo >> 8))
    bytearrayList.append((magicNo & 0xFF))
    bytearrayList.append((0x01))
    bytearrayList.append((filenameLen >> 8))
    bytearrayList.append((filenameLen & 0xFF))
    
    return  bytearrayList + filenameBytes

    
    
    
    

def main():
    """
    main fuction for the client. This is where all the functionality is controlled.
    """
    
    #Gets initial inputs from the user
    addressInfo, ip, port, filename = startConnection()
    
    #Creates the socket
    soc = createSocket()
    
    #Trys to connect to the server 
    establishConnection(soc, ip, port)
    
    packagedRequest = fileRequestPackaging(filename)
    
    
    #send file request
    soc.send(packagedRequest)
    
    #the file response -> the header
    receivedPacket = soc.recv(8)

    
    if receivedPacket[3] == 0:
        print("Error occured when requesting for file")
        
    else:
        if len(receivedPacket) < 8:
            print("The packet header does not match the minimum required bytes")
            soc.close()
            
        else:
            #header parts 
            magicNo = receivedPacket[0] << 8 | (receivedPacket[1] & 255)
            
            
            if magicNo!= 0x497E:
                print("The 'MagicNo' provided is incorrect")
                soc.close()
                sys.exit()
        
            elif receivedPacket[2] != 2:
                print("The 'Type' provided is incorrect")
                soc.close()
                sys.exit()
                
            elif (receivedPacket[3] != 1):
                print("Incorrect 'StatusCode' given")
                soc.close()
                sys.exit()
                
            #The header has the correct information
            else:
                
                packetLength = receivedPacket[4] << 24 | receivedPacket[5] << 16 | receivedPacket[6] << 8 | receivedPacket[7]
                
              
                bytesGotten = 0
                dataByteArray = bytearray()
                
                try:
                    for i in range(0, packetLength, 4096):
                        local_recv = soc.recv(4096)
                        bytesGotten += len(local_recv)
                        dataByteArray += local_recv
                except:
                    print("Error occured while getting data from server")
                    soc.close()
                    sys.exit()
                    
                if packetLength != bytesGotten:
                    print("Error: the dataLength ({0}) does not match the bytes gotten ({1})".format(packetLength, bytesGotten))
                    soc.close()
                    sys.exit()                    
                    
                    
         
                file = open(filename, "wb")
                file.write(dataByteArray)
                file.close()
                
                
                print("\nThe total bytes received - {} Bytes".format(bytesGotten))
                soc.close()
                sys.exit()
            


main()
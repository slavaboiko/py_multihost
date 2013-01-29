
# Create a TCP socket
s = socket(AF_INET, SOCK_STREAM)    
# bind it to the server port
s.bind((serverIP, serverPort))   
# Configure it to accept up to N simultaneous Clients waiting...
s.listen(maxConn)                        

viewdesk.colored_write("Hello",1)

# Run forever
while 1:
        viewdesk.colored_write("Hello",1)
        #wait new Client Connection
        connection, address = s.accept() 
        while 1:
                viewdesk.colored_write("Hello",1)
                # receive message
                isoStr = connection.recv(2048) 
                if isoStr:
                        isoStr = ByteToHex(isoStr[2:])
                        print ("\nInput ASCII |%s|" % isoStr)
                        pack = ISO8583(debug=True)
                        #parse the iso
                        try:
                                #if bigEndian:
                                #        pack.setNetworkISO(isoStr)
                                #else:
                                #        pack.setNetworkISO(isoStr,False)
                        
                                pack.setIsoContent(isoStr)
                                v1 = pack.getBitsAndValues()
                                for v in v1:
                                        text.colored_write ('Bit %s of type %s with value = %s' % (v['bit'],v['type'],v['value']), 0)
                                        
                                if pack.getMTI() == '0800':
                                        text.colored_write ("\tThat's great !!! The client send a correct message !!!", 2)
                                else:
                                        text.colored_write ("The client dosen't send the correct message!", 1)  
                                        break
                                        
                                        
                        except InvalidIso8583, ii:
                                text.colored_write (ii, 1)
                                break
                        except:
                                text.colored_write ('Something happened!!!!', 2)
                                break
                        
                        #send answer
                        pack.setMTI('0810')
                        
                        if bigEndian:
                                ans = pack.getNetworkISO()
                        else:
                                ans = pack.getNetworkISO(False)
                                
                        print ('Sending answer %s' % ans)
                        connection.send(ans)
                        
                else:
                        break
        # close socket          
        connection.close()             
        print ("Closed...")
import socket,sys,threading,time 
def scan(info,port):  
    s = socket.socket()
    s.settimeout(0.2)
    if s.connect_ex((info, port)) == 0:  
        print "[+]",port,'is open'
    else:
        print "[-]",port,'is close'
    s.close()
def main(info,port):
          map(scan,port)
if __name__ == '__main__':  
    info = str(raw_input("Url/ip:"))
    '''info = sys.argv[1]'''
    portlist = [80,135,137,138,139,445,593,1025,2745,3127,3389,4489,]
    threading=[threading.Thread(target=scan,args=(info,port)) for port in portlist]
    for thread in threading:
              thread.start()
              time.sleep(0.5)
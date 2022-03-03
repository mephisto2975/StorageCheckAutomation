import datetime,time
import paramiko, re, platform
from plyer import notification

#station names
windows = {1:'Auriga', 2:'Ganga', 3:'Indus', 4:'Kaveri'}
#2. Ganga
linux = {1:'Austine-c1'}

#ssh credentials
username = 'username'
password = 'password'

#creating ssh connection with user-given host
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#identify the OS running this script
thisOS = platform.system()
for i in windows:
    try:
        ssh.connect(windows[i], username=username, password=password)
        #executing command for disk usage detection on the remote host
        stdin, stdout, stderr = ssh.exec_command('fsutil volume diskfree c:')
        lines = stdout.readlines() 
        #lines = ['Total free bytes        : 9,18,86,24,75,264 (855.8 GB)\r\n', 'Total bytes             : 9,99,61,04,94,976 (931.0 GB)\r\n', 'Total quota free bytes  : 9,18,86,24,75,264 (855.8 GB)\r\n']
        
        #extracting the usage in usable format
        use = re.split(r'[ :)()]',lines[0])
        #use = ['Total', 'free', 'bytes', '', '', '', '', '', '', '', '', '', '9,18,86,24,75,264', '', '855.8', 'GB', '\r\n']
        
        #comparing with required value
        if(float(use[-3]) < 50 ): #use[-3] = 3rd value from the end of string i.e 855.8
            output = "Storage almost full. Please delete some files.\nLocation: {0}".format(windows[i])
            if(thisOS.lower() == 'Windows'.lower()):
                notification.notify(title = "Storage Check Alert!",message=" Storage almost full.\nLocation: {0}".format(windows[i]), timeout=5) #posting a notification for the user
        else:
            output = "No issues in {}.\n".format(windows[i])
        #printing the status and creating a log file
        print("Available storage in {0} = {1} {2}".format(windows[i], use[-3], use[-2]))
        with open("StorageCheckLog.txt", "a+") as f:
            f.write("\n"+ str(datetime.datetime.now()) + " ")
            f.write(output)
            f.write("\nAvailable storage: {1} {2} \n".format(windows[i], use[-3], use[-2]))
    except Exception as e:
        with open("StorageCheckLog.txt", "a+") as f:
            f.write("\n"+ str(datetime.datetime.now()) + " Something went wrong in station " + windows[i] + ".\nTry again. \n ")
        print("\n"+ str(datetime.datetime.now()) + " Something went wrong in station " + windows[i] + ".\nTry again. \n ")
        pass
for i in linux:
    try:
        ssh.connect(linux[i], username=username, password=password)
        #executing command for disk usage detection on the remote host
        stdin, stdout, stderr = ssh.exec_command('df -h /')
        lines = stdout.readlines()
        #Lines = ['Filesystem                               Size  Used Avail Use% Mounted on\n', '/dev/mapper/fedora_localhost--live-root  203G  163G   30G  85% /\n']
        #extracting the usage in usable format
        use =  re.split(r'[ /]',lines[1])
        #use = ['', 'dev', 'mapper', 'fedora_localhost--live-root', '', '203G', '', '163G', '', '', '30G', '', '85%', '', '\n']
                
        #comparing with required value
        if(float(use[-5][:-1]) < 20 ): #use([-5][:-1]) = [-5] is 5th value from the end [:-1] exclude the last character from the [-5]th value i.e 30
            output = "Storage almost full. Please delete some files.\nLocation: {0}".format(linux[i])
        else:
            output = "No issues in {}.\n".format(linux[i])
            
        #printing the status and creating a log file
        print("Available storage in {0} = {1} GB ".format(linux[i], use[-5][:-1] ))
        with open("StorageCheckLog.txt", "a+") as f:
            f.write("\n"+ str(datetime.datetime.now()) + " ")
            f.write(output)
            f.write("\nAvailable storage: {1} GB \n".format(linux[i], use[-5][:-1]))
    except Exception as e:
        with open("StorageCheckLog.txt", "a+") as f:
            f.write("\n"+ str(datetime.datetime.now()) + " Something went wrong in station " + linux[i] + ".\nTry again. \n ")
        print("\n"+ str(datetime.datetime.now()) + " Something went wrong in station " + linux[i] + ".\nTry again. \n ")
        pass

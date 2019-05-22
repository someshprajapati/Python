#!/usr/bin/python

##############################################################################################
# To run use: python ssh_run_command_mulitple_host.py "server_list" "command"                #
##############################################################################################
# example: python ssh_run_command_mulitple_host.py server_list "uname"                       #
##############################################################################################

'''
Author: Somesh K Prajapati
----------------------------
I want to run the same shell command on a few different deployed machines. Please write a script that Accepts two sets of arguments:
    1. An arbitrary number of target servers for SSH
    2. A shell command
SSHs into all the target servers, and executes the command on them in parallel.
'''

import sys
import paramiko
import socket
from multiprocessing import Pool
from getpass import getpass

# Check the required argument parameters are passed or not
if len(sys.argv) < 2:
  print('Missing the 2 compulsory command line arguments : (1) server_list (2) command')
  sys.exit(1)
else:
  server_file = sys.argv[1]
  command = sys.argv[2]

# Ask user to enter username and password on runtime
username = getpass("Enter Username: ")
password = getpass("Enter Password: ")

# Call the function for creating the connection to host and run the command
def processFunc(server):
    try:
        print('Establish the SSH Connection...on Server:  %s'%server)
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(server.strip(), username=username, password=password)
        stdin, stdout, stderr = client.exec_command(command)
        for line in stdout:
            print("Output of command entered by User: " + command)
            print(line.strip('\n'))
        client.close()

    except paramiko.AuthenticationException as error:
        print(error)
        pass
    
    except paramiko.PasswordRequiredException as error:
        print(error)
        pass
        
    except socket.timeout as error:
        print(error)
        pass
 
    except IOError as error:
        print(error)
        pass


# Main function for creating the parallel process
if __name__=='__main__':
    with open(server_file) as f:
        content = f.readlines()
    pool = Pool(len(content))
    pool.map(processFunc, content, 1)
    pool.close()
    pool.join()


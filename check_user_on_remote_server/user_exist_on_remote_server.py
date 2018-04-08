#!/usr/bin/python

#####################################################################################
# To run use: python user_exist_on_remote_server.py "server_file"  username         #
#####################################################################################
# example: python user_exist_on_remote_server.py server_file username               #
#####################################################################################

import pexpect
import sys

ssh_newkey = 'Are you sure you want to continue connecting'

server_file = sys.argv[1]
user = sys.argv[2]

password_input = raw_input("Enter the password:")

# Read input file with the servers details
in_server_file = open(server_file,'r')

# Write the list of servers where user doesn't exist into output file 
user_notexist = open('user_not_exist_out.dat','w')

# Write the list of servers where user exist into output file
user_exist = open('user_exist_out.dat','w')

# Check the user exist or not one by one for the input servers list
for server_name in in_server_file.readlines():
    p = pexpect.spawn('ssh somesh@%s'%server_name)

    res = p.expect([ssh_newkey,'ssword:',pexpect.EOF])

    if res==0:
        p.sendline('yes')

        result = p.expect([ssh_newkey,'ssword:',pexpect.EOF])
    if res==1:
        p.sendline("%s"%password_input)
        p.sendline('id %s'%user)
        
        result = p.expect(['uid', 'no such user' , pexpect.EOF])
    	if result==0:
            user_exist.write(server_name)
            p.sendline("exit")
    	
        elif result==1:
            user_notexist.write(server_name)
	    p.sendline("exit")

        p.sendline("exit")

p.close()

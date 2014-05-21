import pexpect
# If you want to use following function , be ware you should use install 3rd pexpect.#
#*************sendcontent******************#
#Need: IP of EP,  Source of content,
#      m >1 , will run mute near off and mute near on
#      this func need a password for EP
def sendcontent(ip,so,m):
	print "%s will send content\n" %ip

	child = pexpect.spawn('telnet '+ip+' '+'24')
	child.logfile = sys.stdout
	time.sleep(3)
	child.expect('Password:')
	child.sendline(userpass)
	child.sendline('\r\n')
	time.sleep(3)
	child.expect('->')
	if m > 0 :
		child.send('mute near off')
		child.sendline('\r\n')
		time.sleep(3)
		child.sendline('\r\n')
	child.send('vcbutton play '+str(so))
	child.sendline('\r\n')
	time.sleep(5)
	child.expect('->')
	time.sleep(20)
	child.sendline('vcbutton stop')
	child.sendline('\r\n')
	time.sleep(3)
	if m > 0 :
		child.send('mute near on')
		child.sendline('\r\n')
		time.sleep(3)
		child.sendline('\r\n')    
	child.expect('->')
	child.sendline('exit')
	child.sendline('\r\n')
	print ip + 'send content finish!\n'
#*************sendcontent******************#
#Need: IP of EP,  Source of content,
#      m >1 , will run mute near off and mute near on
#      this func no need  password for EP
def sendcontent_nop(ip,so,m):

	print "%s will send content\n" %ip
	child = pexpect.spawn('telnet '+ip+' '+'24')
	child.logfile = sys.stdout
	time.sleep(3)
	#child.expect('Password:')
	#child.sendline('Polycom!12')
	child.sendline('\r')
	time.sleep(3)
	child.expect('->')
	if m > 0 :
		child.send('mute near off')
		child.sendline('\r\n')
		time.sleep(3)
		child.sendline('\r\n')
	child.send('vcbutton play '+str(so))
	child.sendline('\r\n')
	time.sleep(5)
	child.expect('->')
	time.sleep(25)
	child.sendline('vcbutton stop')
	child.sendline('\r\n')
	time.sleep(3)
	if m > 0 :
		child.send('mute near on')
		child.sendline('\r\n')
		time.sleep(3)
		child.sendline('\r\n')       
	child.expect('->')
	child.sendline('exit')
	child.sendline('\r\n')
	print ip + ' send content finish!\n'
#**********************************
#input: HDX IP #
#action: send content from HDX #
#time : 30 seconds
'''def sendcontent(ip,so):
	print "%s will send content\n" %ip

	runtime = int(runtime)
	child = pexpect.spawn('telnet '+ip+' '+'24')
	child.logfile = sys.stdout
	time.sleep(3)
	child.expect('Password:')
	child.sendline(userpass)
	child.sendline('\r\n')
	time.sleep(3)
	child.expect('->')
	child.send('vcbutton play '+str(so))
	child.sendline('\r\n')
	time.sleep(5)
	child.expect('->')
	time.sleep(20)
	child.sendline('vcbutton stop')
	child.sendline('\r\n')
	time.sleep(3)
	child.expect('->')
	child.sendline('exit')
	child.sendline('\r\n')
	print 'send content finish!\n'
#**********************************
#input: HDX IP #
#action: send content from HDX #
#time : 30 seconds
def sendcontent_nop(ip,so):
	
	print "%s will send content\n" %ip
	child = pexpect.spawn('telnet '+ip+' '+'24')
	child.logfile = sys.stdout
	time.sleep(3)
	#child.expect('Password:')
	#child.sendline('Polycom!12')
	child.sendline('\r\n')
	time.sleep(3)
	child.expect('->')
	child.send('vcbutton play '+str(so))
	child.sendline('\r\n')
	time.sleep(5)
	child.expect('->')
	time.sleep(25)
	child.sendline('vcbutton stop')
	child.sendline('\r\n')
	time.sleep(3)
	child.expect('->')
	child.sendline('exit')
	child.sendline('\r\n')
	print 'send content finish!\n'''


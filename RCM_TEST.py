from RCM_classes import RCM,MyList,Meeting,Participants
import xlrd
from ConfigParser import ConfigParser
import os 
from sys import argv
import time
def del_schedule_meeting(rcmadd,meetingID,token):
	url_del_meeting = rcmadd+'meetings/'+str(meetingID)+'?token='+token
	print url_del_meeting 
	del_meeting = requests.delete(url_del_meeting,headers=headers)
	print del_meeting.text
def sub_content(ep,so,m):
	if len(ep)>0:
		eplist = ep.split(',')	
		print 'eplist is %s' %eplist
		sp = len(ep)
		for i in eplist:
			print '%s will send content' %i
			EP.sendcontent_nop(i,so,m)
def sub_content_p(ep,so,m):
	if len(ep)>0:
		eplist = ep.split(',')
		print 'eplist is %s' %eplist
		
		for i in eplist:
			print '%s will send content' %i
			EP.sendcontent(i,so,m)	
def content_test():
	testname = 'content_test'
	EPpass = config.get('EP','password') # from rcm.ini
	ep2 = config.get('EP','ep2')
	ep3 = config.get('EP','ep3')
	ep4 = config.get('EP','ep4')
	
	epp2 = config.get('EP','epp2')
	epp3 = config.get('EP','epp3')
	epp4 = config.get('EP','epp4')
	m = config.get('sound','m')
	sub_content(ep2,2,m)
	sub_content(ep3,3,m)
	sub_content(ep4,4,m)
	sub_content_p(epp2,2,m)
	sub_content_p(epp3,3,m)
	sub_content_p(epp4,4,m)
def letcture_test(token,meetingID,endidlist,interval,rcmadd,rcmapi) :
	testname = 'letcture_test'
	participant = Participants(rcmadd,token,meetingID)
	for id in endidlist :
		time.sleep(15)
		participant.set_lecture(id,rcmapi)
		meeting = Meeting(rcmadd,token)
		meeting.lecture_one_roll(meetingID,interval,rcmapi)
		num = len(endidlist)
		print num 
		time_delay = 15*num + 10
		time_delay = int(time_delay)
		time.sleep(time_delay)
	
def layout_test(token,meetingID,rcmadd,layoutlist,rcmapi):
	participant = Participants(rcmadd,token,meetingID)
	for layout in layoutlist:
		time.sleep(10)
		participant.set_lecture_layout(layout,rcmapi)
def call_and_hangup(token,meetingID,endidlist,rcmadd):
	participant = Participants(rcmadd,token,meetingID)
	for id in endidlist :
		participant.disconnect(id)
		time.sleep(10)
		participant.connect(id)
		time.sleep(10)
def test(rcmadd,userpass,T_F,master,runtime,layoutlist,rcmapi,layout_test_count,interval) :
	rcm =RCM(rcmadd)
	token = rcm.get_token(userpass)
	endpointlist = rcm.get_endpointlist(token,T_F)
	if len(master) > 0 :
		masterID = rcm.get_masterID(token,master)
		meetingID =rcm.create_meeting_masterID(token,endpointlist,masterID)
	meetingID = rcm.create_meeting(token,endpointlist,runtime)  
	time.sleep(20)
	meeting = Meeting(rcmadd,token)
	time.sleep(30)
	endidlist = meeting.get_all_id(meetingID)
	time.sleep(40)
	meeting.muteAll(meetingID)
	time.sleep(40)
	meeting.unmuteAll(meetingID)
	time.sleep(5)
	#content_test()
	
	for tet in range(layout_test_count):
		layout_test(token,meetingID,rcmadd,layoutlist,rcmapi)

	letcture_test(token,meetingID,endidlist,interval,rcmadd,rcmapi)
	call_and_hangup(token,meetingID,endidlist,rcmadd)
	time.sleep(100)
	meeting.terminate(meetingID)
	time.sleep(45)
def test_1_for(rcmadd,ends,userpass,T_F,runtime) :
	rcm =RCM(rcmadd)
	token = rcm.get_token(userpass)
	endpointlist = rcm.get_endpointlist(token,T_F)
	num_end = len(endpointlist)
	print 'num_end is %s\n' %num_end
	s = int(ends) # define the endpoints of per meeting 
	meeting_id_list = MyList()
	for i in range (s,num_end,s):
		print 'i is %s\n' %i
		endlist = endpointlist[i-s:i]
		print endlist
		print type(endlist)
		meetingID = rcm.create_meeting(token,endlist,runtime)  
		time.sleep(1)	
		meeting_id_list.append(meetingID) # use class Mylist
		print meeting_id_list
	meeting = Meeting(rcmadd,token)
	
	time.sleep(900)
	for meetid in meeting_id_list:
		time.sleep(1)
		meeting.terminate(meetid)
def main():	
	script,filename = argv	
	#filename = os.path.join('.', 'rcm.ini')
	config = ConfigParser()
	config.read(filename)
	#script,userpass,run_times = argv
	userpass = config.get('RCM','userpass') #from rcm.ini
	print "%s \n" %(userpass)
	runtime = config.get('TIME', 'runtime')  #from rcm.ini
	print runtime
	waittime = config.get('TIME','waittime') #from rcm.ini 
	rcmadd = config.get('URL', 'rcmadd') # from rcm.ini 
	rcmapi = config.get('URL', 'rcmapi') # from rcm.ini
	interval = config.get('TIME','interval')
	T_F = config.get('endpoint', 'T_F')  #from rcm.ini
	master = config.get('endpoint','master') #from rcm.ini
	ends = config.get('endpoint','ends')
	m = config.get('sound','m') #from rcm.ini
	runtime = int(runtime)
	waittime = runtime + int(waittime) # consider the send content time is 30*3, and time.slee(30)
	runtime = runtime*1000
	#layoutlist = ['TWO_BY_TWO','AUTO','LAND_SEVER','THREE_BY_THREE','LAND_FIVE','FOUR_BY_FOUR','LAND_TWO_HOR']
	layout_test_count = config.get('RCM','layout_test_count')
	layout_test_count = int(layout_test_count)
	layoutlist_str = config.get('RCM','layoutlist')
	layoutlist = layoutlist_str.split(',') 
	print runtime
	while 1 :
		test_1_for(rcmadd,ends,userpass,T_F,runtime)
		time.sleep(10)
		test(rcmadd,userpass,T_F,master,runtime,layoutlist,rcmapi,layout_test_count,interval)
	print 'test finish!'
if __name__ == "__main__": 
	main()
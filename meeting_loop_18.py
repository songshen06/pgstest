#!/usr/bin/env python
# -*- coding: utf-8 -*-
#written by Shen Song, email shen.song@polycom.com#
#internal use only***************#
#0.5 change all parms to rcm.ini #
#0.6 change : add a gettoken function for fixing token invalid,comment out get unit from script#
#0.7 change the waittime = runtime+waittime
#0.8 add a token protection 
#0.9 add send content action 
#1.0 add three hdx send content, and write function sendcont2 for hdx6000
#1.01 change rcm.ini to argv
#1.02 update for content section 
#1.03 combine content function
#1.04 updte send content function
#1.05 added some class to replace function
#1.06 rewrire the script , add RCM,Meeting  class
#1.07 added rcm.create_meeting
#1.08 import EP.py and add send content action
import json  #for json data #
import requests # for http action #
import time  # for time  #
from sys import argv # python meeting_loop_4.py RMX1800 1  
from ConfigParser import ConfigParser# support rcm.ini
import os
#import pexpect # for control EP
#import sys
#----define a class to add number value ------#
#import EP

class MyList(list):
    def append(self, value):
        super(MyList, self).append(value)
        return self
class RCM(object):
	def __init__(self, link):
		self.link = link 
	def get_token(self):
		rcmadd = self.link
		print rcmadd
		user_pass = {'account':userpass ,'password':userpass}
		#print user_pass
		#open('endoint.text', 'a').write("MCU is %s\n" %userpass)
		user_pass_json = json.dumps(user_pass)
		print user_pass_json
		urllogin = rcmadd+'login'
		r = requests.put(urllogin,data=user_pass_json)
		print r.text
		r_dict = json.loads(r.text) #decode 
		print "r_dict is %s\n"  %(type(r_dict))
		if r.status_code == 200 or 201:
			token = r_dict['token']
		else:		
			print r.status_code
		print token
		return str(token) 
# this method depend on the login user, 
		
	def get_endpointlist(self,token):
		start = int(time.time())
		end = int(start + 3600*1000)
		#token = self.get_token()
		self.token = token
		token = self.token
		rcmadd = self.link
		print token
		url_endpoints=rcmadd+'endpoints?token='+token+'&startTime='+str(start)+'&endTime='+str(end)+'&includeSubUnit='+T_F
		print url_endpoints
		endlist = requests.get(url_endpoints)
		endlist_json=json.loads(endlist.text)
		endpointlist = MyList()
		print endpointlist
		for unit in endlist_json:
			#print unit
			#print type(unit)
			#print unit['ip']
			#endpointIP = unit['ip']
			print unit['id']
			endpointID = unit['id']
			#print type(endpointID)
			endpointlist.append(endpointID) # use class Mylist
		#print 'endpoint list print in endpoint.text!!'
		print endpointlist
		return endpointlist
	def get_masterID(self,token,master):
		start = int(time.time())
		end = int(start + 3600*1000)
		#token = self.get_token()
		self.token = token
		token = self.token
		self.master = master
		master = self.master
		rcmadd = self.link
		print token
		url_endpoints=rcmadd+'endpoints?token='+token+'&startTime='+str(start)+'&endTime='+str(end)+'&includeSubUnit='+T_F
		print url_endpoints
		endlist = requests.get(url_endpoints)
		endlist_json=json.loads(endlist.text)
	
	
		for unit in endlist_json:
			#print unit
			#print type(unit)
			#print unit['ip']
			endpointIP = unit['ip']
			if endpointIP == master :
				print 'endpointIP is %s\n' %endpointIP
				print unit['id']
				masterID = unit['id']
			#print type(endpointID)
		print 'master is %s\n' %masterID
		return masterID
	def create_meeting(self,token,endpointlist):
		print 'create_meeting\n'
		self.token = token
		token = self.token
		self.endpointlist= endpointlist
		endpointlist = self.endpointlist
		rcmadd = self.link
		url_meetings=rcmadd+'meetings?token='+token
		print url_meetings
		name = time.ctime()
		endpoints = {'startTime':0,'duration':runtime,'endpointIds':endpointlist,'name':name}
		print endpoints
		endpoints_json = json.dumps(endpoints) # dump to json format
		print endpoints_json
		headers = {'Content-type': 'application/json','Accept': 'text/plain'}
		meetings=requests.post(url_meetings,data=endpoints_json,headers=headers)
		#print meetings.text
		meetinglist_dict=json.loads(meetings.text)
		print "meeinglist is %s" %meetinglist_dict
		print type(meetinglist_dict)
		print meetinglist_dict['id']
		meetingID = meetinglist_dict['id']
		return meetingID
	def create_meeting_masterID(self,token,endpointlist,masterID):
		print 'create_meeting_masterID\n'
		self.token = token
		token = self.token
		self.endpointlist= endpointlist
		endpointlist = self.endpointlist
		self.masterID = masterID
		masterID = int(self.masterID)
		rcmadd = self.link
		url_meetings=rcmadd+'meetings?token='+token
		print url_meetings
		name = time.ctime()
		layout = '1and5'
		endpoints = {'startTime':0,'duration':runtime,'layout':layout,'endpointIds':endpointlist,'name':name,'masterEndpointId':masterID}
		print endpoints
		endpoints_json = json.dumps(endpoints) # dump to json format
		print endpoints_json
		headers = {'Content-type': 'application/json','Accept': 'text/plain'}
		meetings=requests.post(url_meetings,data=endpoints_json,headers=headers)
		print meetings.text
		meetinglist_dict=json.loads(meetings.text)
		print "meeinglist is %s" %meetinglist_dict
		print type(meetinglist_dict)
		print meetinglist_dict['id']
		meetingID = meetinglist_dict['id']
		return meetingID
	def get_meetingID(self,token):
		start = int(time.time()*1000 - 100*1000)
		end = int(time.time()*1000 + 7200*1000)
		#token = self.get_token()
		self.token = token
		token = self.token
		rcmadd = self.link
		print token
		url_meetings=rcmadd+'meetings?token='+token+'&startTime='+str(start)+'&endTime='+str(end)	
		print url_meetings
		meetinglist = requests.get(url_meetings)
		meetinglist_dict=json.loads(meetinglist.text)
		print "meeinglist is %s" %meetinglist_dict
		print type(meetinglist_dict)
		print meetinglist_dict[0]['id']
		meetingID = meetinglist_dict[0]['id']
		return meetingID
	def get_units(self):
		url_units=rcmadd+'units?token='+token
		print url_units
		u = requests.get(url_units)
		u_dict = json.loads(u.text)
		print type(u_dict)
		print u_dict
	# just list here for 
		for unit in u_dict:
			print unit
			print type(unit)
			print unit['id']
			unitID = unit['id']
			unitNAME = unit['name']
			print "%s unid id is %s\n" %(unitID,unitNAME)

#---------------------------------------------#
class Meeting(object):
	def __init__(self,link,token):
		self.link = link 
		self.token = token
	def terminate(self,meetingID):
		token = self.token
		rcmadd = self.link
		self.meetingID = meetingID
		meetingID = self.meetingID
		url_terminate = rcmadd+'meetings/'+str(meetingID)+'/control/terminate?token='+token
		print url_terminate
		headers = {'Content-type': 'application/json','Accept': 'text/plain'}
		meeting_terminate = requests.put(url_terminate,headers=headers)
		print meeting_terminate.text
	def get_all_id(self,meetingID):
		token = self.token
		rcmadd = self.link
		self.meetingID = meetingID
		meetingID = self.meetingID
		url = rcmadd+'meetings/'+str(meetingID)+'/participants?token='+token
		print url 
		headers = {'Content-type': 'application/json','Accept': 'text/plain'}
		meeting = requests.get(url,headers=headers)
		print meeting.text
		endlist_json=json.loads(meeting.text)
		print type(endlist_json)
		endidlist = MyList()
		print endidlist
		for end in endlist_json:
			print end['id']
			endpointID = end['id']
			#print type(endpointID)
			endidlist.append(endpointID) # use class Mylist
		#print 'endpoint list print in endpoint.text!!'
		print endidlist
		return endidlist
	def muteAll(self,meetingID):
		token = self.token
		rcmadd = self.link
		self.meetingID = meetingID
		meetingID = self.meetingID
		url = rcmadd+'meetings/'+str(meetingID)+'/control/muteAll?token='+token
		print url
		headers = {'Content-type': 'application/json','Accept': 'text/plain'}
		meeting_terminate = requests.put(url,headers=headers)
		print meeting_terminate.text
	def unmuteAll(self,meetingID):
		token = self.token
		rcmadd = self.link
		self.meetingID = meetingID
		meetingID = self.meetingID
		url = rcmadd+'meetings/'+str(meetingID)+'/control/unmuteAll?token='+token
		print url
		headers = {'Content-type': 'application/json','Accept': 'text/plain'}
		meeting_terminate = requests.put(url,headers=headers)
		print meeting_terminate.text
	def lecture_one_roll(self,meetingID,interval):
		print 'lecture_one_roll'
		token = self.token
		rcmadd = self.link
		self.meetingID = meetingID
		meetingID = self.meetingID
		self.interval = interval
		interval = self.interval
		url = rcmapi+'meetings/'+str(meetingID)+'/control/oneClickPoll?credential='+token+'&interval='+interval
		#PUT /api/rest/meetings/173662/control/oneClickPoll?credential=2097014321&interval=30 
		print url
		headers = {'Content-type': 'application/json','Accept': 'text/plain'}
		meeting_terminate = requests.put(url,headers=headers)
		print meeting_terminate.text
class Participants(object):
	def __init__(self,link,token,meetingID):
		self.link = link 
		self.token = token
		self.meetingID = meetingID

	def muteAudio(self,endpointID):
		token = self.token
		rcmadd = self.link
		self.endpointID= endpointID
		endpointID= self.endpointID
		meetingID = self.meetingID
		url = rcmadd+'meetings/'+str(meetingID)+'/participants/'+str(endpointID)+'/control/muteAudio?token='+token
		print url
		headers = {'Content-type': 'application/json','Accept': 'text/plain'}
		meeting_terminate = requests.put(url,headers=headers)
		print meeting_terminate.text
	def unmuteAudio(self,endpointID):
		token = self.token
		rcmadd = self.link
		meetingID = self.meetingID
		self.endpointID= endpointID
		endpointID= self.endpointID
		url = rcmadd+'meetings/'+str(meetingID)+'/participants/'+str(endpointID)+'/control/unmuteAudio?token='+token
		print url
		headers = {'Content-type': 'application/json','Accept': 'text/plain'}
		meeting_terminate = requests.put(url,headers=headers)
		print meeting_terminate.text
	def disconnect(self,endpointID):
		token = self.token
		rcmadd = self.link
		meetingID = self.meetingID
		self.endpointID= endpointID
		endpointID= self.endpointID
		url = rcmadd+'meetings/'+str(meetingID)+'/participants/'+str(endpointID)+'/control/disconnect?token='+token
		print url
		headers = {'Content-type': 'application/json','Accept': 'text/plain'}
		meeting_terminate = requests.put(url,headers=headers)
		print meeting_terminate.text
	def connect(self,endpointID):
		token = self.token
		rcmadd = self.link
		meetingID = self.meetingID
		self.endpointID= endpointID
		endpointID= self.endpointID
		url = rcmadd+'meetings/'+str(meetingID)+'/participants/'+str(endpointID)+'/control/connect?token='+token
		print url
		headers = {'Content-type': 'application/json','Accept': 'text/plain'}
		meeting_terminate = requests.put(url,headers=headers)
		print meeting_terminate.text
	def set_lecture(self,endpointID):
		token = self.token
		rcmadd = self.link
		meetingID = self.meetingID
		self.endpointID= endpointID
		endpointID= self.endpointID
		url = rcmapi+'meetings/'+str(meetingID)+'/participants/'+str(endpointID)+'/control/setLecturer?credential='+token
		print url
		headers = {'Content-type': 'application/json','Accept': 'text/plain'}
		meeting_terminate = requests.get(url,headers=headers)
		print meeting_terminate.text
	def set_lecture_layout(self,layout):
		token = self.token
		rcmadd = self.link
		meetingID = self.meetingID
		self.layout = layout
		layout = self.layout
		url = rcmapi+'meetings/'+str(meetingID)+'/control/setVideoLayout?credential='+token
		print url
		layout_data = {'videoLayout':layout}
		print layout
		layout_json = json.dumps(layout_data) # dump to json format
		print layout_json
		headers = {'Content-type': 'application/json','Accept': 'text/plain'}
		meeting_terminate = requests.put(url,data=layout_json,headers=headers)
		print meeting_terminate.text
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
def create_meeting_test(rcmadd,token):
	## input : rcmadd and token ##
	## output: meetingID ##
	
	testname = 'create_meeting_test'
	
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
def letcture_test(token,meetingID,endidlist,interval) :
	testname = 'letcture_test'
	participant = Participants(rcmadd,token,meetingID)
	for id in endidlist :
		time.sleep(15)
		participant.set_lecture(id)
		meeting = Meeting(rcmadd,token)
		meeting.lecture_one_roll(meetingID,interval)
		num = len(endidlist)
		print num 
		time_delay = 15*num + 10
		time_delay = int(time_delay)
		time.sleep(time_delay)
	
def layout_test(token,meetingID):
	participant = Participants(rcmadd,token,meetingID)
	for layout in layoutlist:
		time.sleep(10)
		participant.set_lecture_layout(layout)
def call_and_hangup(token,meetingID,endidlist):
	participant = Participants(rcmadd,token,meetingID)
	for id in endidlist :
		participant.disconnect(id)
		time.sleep(10)
		participant.connect(id)
		time.sleep(10)
def test() :
	rcm =RCM(rcmadd)
	token = rcm.get_token()
	endpointlist = rcm.get_endpointlist(token)
	if len(master) > 0 :
		masterID = rcm.get_masterID(token,master)
		meetingID =rcm.create_meeting_masterID(token,endpointlist,masterID)
	meetingID = rcm.create_meeting(token,endpointlist)  
	time.sleep(20)
	#meetingID = rcm.get_meetingID(token)
	meeting = Meeting(rcmadd,token)
	time.sleep(30)
	endidlist = meeting.get_all_id(meetingID)
	time.sleep(40)
	meeting.muteAll(meetingID)
	time.sleep(40)
	meeting.unmuteAll(meetingID)
	time.sleep(5)
	#content_test()
	
	
	layout_test(token,meetingID)
	letcture_test(token,meetingID,endidlist,interval)
	call_and_hangup(token,meetingID,endidlist)
	time.sleep(100)
	meeting.terminate(meetingID)
	time.sleep(45)
def test_1_for() :
	rcm =RCM(rcmadd)
	token = rcm.get_token()
	endpointlist = rcm.get_endpointlist(token)
	num_end = len(endpointlist)
	print 'num_end is %s\n' %num_end
	s = int(ends( # define the endpoints of per meeting 
	meeting_id_list = MyList()
	for i in range (s,num_end,s):
		print 'i is %s\n' %i
		endlist = endpointlist[i-5:i]
		print endlist
		print type(endlist)
		meetingID = rcm.create_meeting(token,endlist)  
		meeting_id_list.append(meetingID) # use class Mylist
		print meeting_id_list
	meeting = Meeting(rcmadd,token)
	
	time.sleep(300)
	for meetid in meeting_id_list:
		time.sleep(1)
		meeting.terminate(meetid)
#### main script start here####	
	
script,filename = argv	
#filename = os.path.join('.', 'rcm.ini')
config = ConfigParser()
config.read(filename)
#script,userpass,run_times = argv
userpass = config.get('RCM','userpass') #from rcm.ini

counter = config.get('RCM','counter')	#from rcm.ini
print "%s %s \n" %(userpass,counter)
runtime = config.get('TIME', 'runtime')  #from rcm.ini
waittime = config.get('TIME','waittime') #from rcm.ini 
meeting_counter = int(counter)
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
layoutlist = ['TWO_BY_TWO','AUTO','LAND_SEVER','THREE_BY_THREE']

#print runtime
#print type(runtime)
#print waittime
while 1 :
	test_1_for()
	time.sleep(10)
	#test()
print 'test finish!'


















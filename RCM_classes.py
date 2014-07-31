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
	def get_token(self,userpass):
		rcmadd = self.link
		print rcmadd
		self.userpass = userpass
		userpass = self.userpass
		user_pass = {'account':userpass ,'password':userpass}
		#print user_pass
		#open('endoint.text', 'a').write("MCU is %s\n" %userpass)
		user_pass_json = json.dumps(user_pass)
		print user_pass_json
		urllogin = rcmadd+'login'
		r = requests.put(urllogin,data=user_pass_json)
		print r.text
		print r.json
		r_dict = json.loads(r.text) #decode 
		print "r_dict is %s\n"  %(type(r_dict))
		if r.status_code == 200 or 201:
			token = r_dict['token']
		else:		
			print r.status_code
		print token
		return str(token) 
# this method depend on the login user, 
		
	def get_endpointlist(self,token,T_F):
		start = int(time.time())
		end = int(start + 3600*1000)
		#token = self.get_token()
		self.token = token
		token = self.token
		self.T_F = T_F
		T_F = self.T_F
		rcmadd = self.link
		print token
		url_endpoints = rcmadd+'endpoints?token='+token+'&startTime='+str(start)+'&endTime='+str(end)+'&includeSubUnit='+str(T_F)
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
	def get_masterID(self,token,master,T_F):
		start = int(time.time())
		end = int(start + 3600*1000)
		#token = self.get_token()
		self.token = token
		token = self.token
		self.master = master
		master = self.master
		rcmadd = self.link
		print token
		url_endpoints=rcmadd+'endpoints?token='+token+'&startTime='+str(start)+'&endTime='+str(end)+'&includeSubUnit='+ str(T_F)
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
	def create_meeting(self,token,endpointlist,runtime):
		print 'create_meeting\n'
		self.token = token
		token = self.token
		self.endpointlist= endpointlist
		endpointlist = self.endpointlist
		self.runtime = runtime
		runtime = self.runtime
		rcmadd = self.link
		url_meetings=rcmadd+'meetings?token='+token
		print url_meetings
		name = time.ctime()
		print runtime
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
	def get_units(self,token):
		rcmadd = self.link
		self.token = token
		token = self.token
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
	def add_endpoints(self,token,d_excel):
		rcmadd = self.link
		self.d_excel = d_excel
		d_excel = self.d_excel
		url = rcmadd+'managedEndpoints?token='+token
		print url
		d_excel_json= json.dumps(d_excel) # dump to json format
		print d_excel_json
		headers = {'Content-type': 'application/json','Accept': 'text/plain'}
		rcm_feedback = requests.put(url,data=d_excel_json,headers=headers)
		print rcm_feedback.text
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
			#print end['id']
			if end['type'] != 'LINK' :
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
	def lecture_one_roll(self,meetingID,interval,rcmapi):
		print 'lecture_one_roll'
		token = self.token
		rcmadd = self.link
		self.meetingID = meetingID
		meetingID = self.meetingID
		self.interval = interval
		interval = self.interval
		self.rcmapi = rcmapi
		rcmapi = self.rcmapi
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
	def set_lecture(self,endpointID,rcmapi):
		token = self.token
		rcmadd = self.link
		meetingID = self.meetingID
		self.endpointID= endpointID
		endpointID= self.endpointID
		self.rcmapi= rcmapi
		rcmapi= self.rcmapi
		url = rcmapi+'meetings/'+str(meetingID)+'/participants/'+str(endpointID)+'/control/setLecturer?credential='+token
		print url
		headers = {'Content-type': 'application/json','Accept': 'text/plain'}
		meeting_terminate = requests.get(url,headers=headers)
		print meeting_terminate.text
	def set_lecture_layout(self,layout,rcmapi):
		token = self.token
		rcmadd = self.link
		self.rcmapi = rcmapi
		rcmapi = self.rcmapi
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
















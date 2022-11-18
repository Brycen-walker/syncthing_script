import subprocess
import os

files = []

os.system("mkdir scripts")
os.chdir("scripts/")

sec_script = 0

for sec in range(228,231):

	script_it = 0

	for i in range(1,255):
		ip_ad = "192.168." + str(sec) + "." + str(i) 
		name = "script-" + str(sec_script) + str(script_it) + ".py"
		script_it += 1
		files.append(name)
		with open(name,"w") as file:
			file.write(f"""
import os
import requests
import re

def scan(ip):
	url = f'http://{{ip}}:8384'
	session = requests.Session()
	response = session.get(url)
	session_cookie = session.cookies.get_dict()
	
	cookie_1 = session_cookie.keys()
	cookie_1 = list(cookie_1)
	cookie_1 = cookie_1[0]
	cookie_1 = re.sub('CSRF-Token-','',cookie_1)
	csrf_header = f'X-CSRF-Token-{{cookie_1}}'

	cookie_2 = session_cookie.values()
	cookie_2 = list(cookie_2)
	cookie_2 = cookie_2[0]

	scan_url = url+"/rest/db/scan?folder=SYNCED_FILES"
	requests.post(scan_url, cookies=session_cookie, headers={{csrf_header: cookie_2}})


def reset(ip):
	url = f'http://{{ip}}:8384'
	session = requests.Session()
	response = session.get(url)
	session_cookie = session.cookies.get_dict()
	
	cookie_1 = session_cookie.keys()
	cookie_1 = list(cookie_1)
	cookie_1 = cookie_1[0]
	cookie_1 = re.sub('CSRF-Token-','',cookie_1)
	csrf_header = f'X-CSRF-Token-{{cookie_1}}'

	cookie_2 = session_cookie.values()
	cookie_2 = list(cookie_2)
	cookie_2 = cookie_2[0]

	reset_url = url+"/rest/db/revert?folder=SYNCED_FILES"
	requests.post(reset_url, cookies=session_cookie, headers={{csrf_header: cookie_2}})
scan("{ip_ad}")
reset("{ip_ad}")
""")

	sec_script +=1 

for f in files:
	subprocess.Popen(["python3",str(f)])
	print(f"trying {f}")

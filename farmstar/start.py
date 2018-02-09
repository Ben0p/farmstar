import sys
import subprocess
import os
import time


#django server binding 
ip = '127.0.0.1'
port = ':8000'

#Python file paths
scripts = os.path.join('backend','scripts','run.py')
webui = os.path.join('frontend', 'django', 'manage.py ')

#Args
webui_args = ' runserver '+ip+port

#Commands to run
scripts_run = 'python '+scripts
webui_run = 'python '+webui+webui_args

#Entire command
scripts_cmd = 'start cmd /K '+scripts_run
webui_cmd = 'start cmd /K '+webui_run

#Chrome windows
chrome = '"c:\progra~2\Google\Chrome\Application\chrome.exe" --kiosk '


os.system(scripts_cmd)
os.system(webui_cmd)
time.sleep(5)
os.system(chrome+ip+port+'\map')





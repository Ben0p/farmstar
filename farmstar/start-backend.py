import sys
import subprocess
import os
import time


#Python file paths
scripts = os.path.join('backend','scripts')
data = os.path.join('data')
dicts = os.path.join('backend','scripts','dicts')
backup = os.path.join('backup')

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

def main():
    os.system(scripts_cmd)
    os.system(webui_cmd)
    time.sleep(5)
    os.system(chrome+ip+port+'\map')

if __name__ = '__main__':
    main()





import os
import subprocess
from config import config_dir

def test_connection(maa_core, adb_device):
    ping_filepath = os.path.join(config_dir, 'ping.py')
    ping_code = f"""
import json
import pathlib
import time
import sys

sys.path.append('{maa_core}/Python')

from asst.asst import Asst
from asst.utils import InstanceOptionType

path = '{maa_core}'
Asst.load(path=path, user_dir='{config_dir}')
asst = Asst()
asst.set_instance_option(InstanceOptionType.touch_type, 'maatouch')
if asst.connect('adb', '{adb_device}'):
    print('连接成功')
else:
    print('连接失败')
"""

    with open(ping_filepath, 'w') as f:
        f.write(ping_code)

    result = subprocess.run(['python', ping_filepath], capture_output=True, text=True)
    return result.stdout.strip() == '连接成功'

def start_tasks(tasks, config):
    maa_core = config['maa_core']
    adb_device = config['adb_device']

    task_filepath = os.path.join(config_dir, 'run.py')
    task_core_code = "\n".join(map(lambda task: f"asst.append_task('{task.type}', {repr(task.config)})", tasks))
    task_code = f"""
import json
import time
import sys

sys.path.append('{maa_core}/Python')

from asst.asst import Asst
from asst.utils import Message, Version, InstanceOptionType
from asst.updater import Updater

path = '{maa_core}'

# Updater(path, Version.Stable).update()

@Asst.CallBackType
def my_callback(msg, details, arg):
    m = Message(msg)
    d = json.loads(details.decode('utf-8'))
    print(m, d, arg, flush=True)

Asst.load(path=path, user_dir='{config_dir}')
asst = Asst(callback=my_callback)
asst.set_instance_option(InstanceOptionType.touch_type, 'maatouch')
if not asst.connect('adb', '{adb_device}'):
    exit(1)

{task_core_code}

asst.start()
while asst.running():
    time.sleep(0)
"""
    
    with open(task_filepath, 'w') as f:
        f.write(task_code)

    return subprocess.Popen(['python', task_filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

import os
import json

config_dir = ""
if os.name == 'nt':  # Windows
    config_dir = os.path.join(os.environ['APPDATA'], 'Maa-Gtk')
else:  # Linux/Mac
    config_dir = os.path.expanduser('~/.config/maa-gtk')

os.makedirs(config_dir, exist_ok=True)

config_file = os.path.join(config_dir, 'config.json')

def read_maa_gtk_config():
    if not os.path.isfile(config_file):
        print("配置文件不存在")
        return None

    try:
        # 读取配置文件内容
        with open(config_file, 'r') as f:
            config_data = json.load(f)
            return config_data
    except json.JSONDecodeError:
        print("配置文件解析失败")
        return None
    except Exception as e:
        print("配置文件读取失败:", str(e))
        return None
    
def save_maa_gtk_config(config):
    try:
        with open(config_file, 'w') as f:
            f.write(json.dumps(config))
    except:
        print("写入配置文件失败")

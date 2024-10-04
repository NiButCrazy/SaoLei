"""
用来读取配置文件
"""

import json
import os
from tkinter import messagebox


# 把当前目录设置为工作目录，防止外部运行某个脚本无法定位目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def error_message(message):
    # 创建一个简单的Tkinter警告弹窗
    messagebox.showerror("别乱改配置文件", message)

def get_config(key: str) -> any:
    """
    读取配置文件的至
    :param key: 配置的键
    :return:
    """
    return data[key]

def get_config_all() -> dict:
    """
    获取配置的字典对象本身
    :return: 一个字典
    """
    return data

def write_config(key: str, value: any) -> bool:
    """
    写入/修改配置
    :param key: 配置的键
    :param value: 配置的值
    :return:
    """
    data[key] = value
    try:
        with open("config.json", 'w', encoding='utf-8') as f:
            # noinspection PyTypeChecker
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        messagebox.showerror("丸辣", "写入配置文件失败\n" + str(e))
        return False

def get_rank() -> bool | dict[str, list[list[int, str, int]]]:
    """
    读取排名数据
    :return: 返回一个布尔值或者所有地图的排名字典
    """
    try:
        with open("user.rank", 'r', encoding='utf-8') as f:
            rank_data = f.read().strip().split("\n")
            rank_dict = {"10x10":[], "15x15":[], "20x20":[],"30x30":[],"40x40":[],"50x50":[],"自定义":[]}
            for rank in rank_data:
                name, map_size, bomb_number, time = rank.split(" ")
                if map_size not in rank_dict:
                    map_size = "自定义"
                rank_dict[map_size].append([int(bomb_number),name, int(time)])
            for map_size, rank_list in rank_dict.items():
                if rank_list:
                    rank_list.sort(key = lambda x: (x[0],-x[2]),reverse = True)
                    rank_dict[map_size] = rank_list[:10] if len(rank_list) >= 10 else rank_list

            return rank_dict
    except Exception as e:
        messagebox.showerror("丸辣", "读取排行文件失败\n" + str(e))
        return False

def save_config() -> bool:
    """
    保存配置，和 write_config 二选一
    :return:返回是否保存成功
    """
    try:
        with open("config.json", 'w', encoding='utf-8') as f:
            # noinspection PyTypeChecker
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        messagebox.showerror("丸辣", "写入配置文件失败\n" + str(e))
        return False

try:
    with open("config.json", 'r', encoding='utf-8',) as file:
        data = json.load(file)

except FileNotFoundError:
    error_message("未找到配置文件")
except json.JSONDecodeError:
    error_message("配置文件不是有效的 JSON 格式")

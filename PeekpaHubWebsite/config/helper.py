# encoding: utf-8
__author__ = 'lianggao'
__date__ = '2019/10/25 6:01 PM'
import json
import os

PWD_PATH = os.getcwd()

FILE_PATH = PWD_PATH + '/config/config.json'

def read_config_from_configfile():
    with open(FILE_PATH, 'r') as load_f:
        load_json = json.load(load_f)
        print("Config_utils_read_config_from_configfile:::")
        print(load_json)
    return load_json

import datetime
import json


class Logger:
    def __init__(self):
        self.json_file = 'json_history/history.json'
        self.log_dir = 'logs'
        self.base_name = f'logger_{datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.log'
        self.filename = f'{self.log_dir}/{self.base_name}'
        self.log_status = False

    def start_log(self):
        key = input('Did you want to log this session?\nType y/n: ')
        if key in ['y', 'yes', 'Y', 'YES', 'Yes']:
            self.log_status = True
        else:
            self.log_status = False
            return
        with open(self.filename, 'w') as log_file:
            log_file.write(f'Start logging at: {datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}\n\n')

    def write(self, message):
        if not self.log_status:
            return
        with open(self.filename, 'a') as log_file:
            log_file.write(f'{datetime.datetime.now().strftime("%H:%M:%S")} | {message}\n')

    def write_json(self, obj):
        if not self.log_status:
            return
        with open(self.json_file, 'a', encoding='utf-8') as json_file:
            json.dump(obj, json_file, ensure_ascii=False)
            json_file.write('\n')

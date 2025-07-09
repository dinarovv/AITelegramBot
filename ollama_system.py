import ollama

from exceptions import AdminException
from logger import Logger


class OllamaSystem:
    def __init__(self, model):
        self.model = model
        self.logger = Logger()

    def connect_logger(self):
        self.logger.start_log()

    def switch_model(self, model, user):
        if user.admin_rules:
            self.model = model
        else: raise AdminException(f'You dont have access to the command.')

    def make_question(self, message):
        response = ollama.chat(model=self.model, messages=[{'role' : 'user', 'content' : message}])
        return response['message']['content']

if __name__ == '__main__':
    sys = OllamaSystem(model='gemma3:latest')
    print(str(sys.make_question('привет')))
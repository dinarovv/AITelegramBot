from exceptions import AdminException
from ollama_system import OllamaSystem
from _private_info import _password


class User:
    def __init__(self, logger, admin_rules=False):
        self.logs = logger
        self.model = 'gemma3:latest'
        self.system = OllamaSystem(model=self.model)
        self.username = '<User is unknown>'
        self.admin_rules = admin_rules
        self.user_input_password = None

    def prompt(self) -> str:
        if not self.admin_rules:
            message = input()
            return message
        else:
            raise AdminException('Switch admin rules before prompt!')

    @property
    def password_is_true(self) -> bool:
        return self.user_input_password == _password

    def be_admin(self) -> str:
        if self.password_is_true:
            self.admin_rules = True
            return 'Success! You have admin rules right now!\nType /admin_shell to use your new features'
        return 'Password is wrong!'

    def exit_admin(self) -> str:
        self.admin_rules = False
        return 'You are leave admin rules now!'
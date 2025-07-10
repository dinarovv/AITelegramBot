def _get_password() -> str:
    try:
        password = ''
        with open('extensions/password.txt', 'r') as file:
            password = file.readline()
            print(f'Password set successfully! Password is: {password}')
        return password
    except FileNotFoundError as _ex:
        print('Password is empty!')
        return ''

def _get_token() -> str:
    try:
        token= ''
        with open('extensions/token.txt', 'r') as file:
            token = file.readline()
            print(f'Token set successfully! Your token is: {token}')
        return token
    except FileNotFoundError as _ex:
        print('File is not found!')
        print('The system shuts down..')
        exit(0)
    except Exception as _ex:
        print(_ex)
        print('The system shuts down..')
        exit(0)

_password = _get_password()
_token = _get_token()
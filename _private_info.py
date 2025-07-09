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

_password = _get_password()
_token = '8095147953:AAFU-AtAVKUVNkXgUmISVKWjTy4jtv1Hk0E'
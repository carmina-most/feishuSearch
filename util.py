import os
cookie_file = './cookie.txt'
windows_chrome_path = ["C:\Program Files\Google\Chrome\Application\chrome.exe", "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]


def check_cookie():
    if os.path.exists(cookie_file):
        with open(cookie_file, 'r') as f:
            cookie_f = f.read()
            if cookie_f != '':
                return True
            return False
    else:
        return False


def save_cookie(cookies):
    try:
        with open(cookie_file, 'w') as f:
            cookie_str = ''
            for cookie_pair in cookies:
                name = cookie_pair['name']
                value = cookie_pair['value']
                cookie_str += name+'='+value+'; '
            f.write(cookie_str)
        return True
    except:
        return False


def read_cookie():
    if os.path.exists(cookie_file):
        with open(cookie_file, 'r') as f:
            cookie_f = f.read()
            if cookie_f != '':
                return cookie_f


def ob_chrome_path():
    for path in windows_chrome_path:
        if os.path.exists(path):
            return path

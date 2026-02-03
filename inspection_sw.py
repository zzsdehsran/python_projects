from paramiko import SSHClient,AutoAddPolicy
from time import sleep

ips = ['10.0.103.1','10.0.116.1','10.0.0.6','10.0.117.1','10.0.121.1','10.0.134.1']

for ip in ips:
    hosts = {
    'hostname': ip,
    'username': 'python',
    'password': 'Bosum@2025',
    }
    try:
        print(f"正在连接{ip}。。。")
        ssh_client = SSHClient()
        ssh_client.set_missing_host_key_policy(AutoAddPolicy)
        ssh_client.connect(**hosts)
        print(f"{ip}连接成功！")

        
        print("~~~~~~~~~~开始巡检~~~~~~~~~~：")
        commands = [
                'screen-length 0 temporary\n',
                'display version\n',
                'display cpu-usage\n',
                'display memory-usage\n',
                'display power\n',
                'display eth-trunk\n',
                ]
        set_command = ssh_client.invoke_shell()
        
        output = b""
        for cmd in commands:
            set_command.send(cmd)
            sleep(2)
            while True:
                if set_command.recv_ready():
                    chunk = set_command.recv(65535)
                    output += chunk
                else:
                    sleep(0.5)
                    if not set_command.recv_ready():
                        break
        result_text = output.decode('utf-8',errors='ignore')
        print(result_text)

        with open(f"{ip}.txt","w") as f:
            f.write(output.decode('utf-8'))
        
        ssh_client.close()
    
    except Exception as e:
        print(f"Error Code:{e}")

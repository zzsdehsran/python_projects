from paramiko import SSHClient, AutoAddPolicy
from time import sleep
from params import *

def add_address(ssh):

    collects = []
    i = 0

    command_grp = ['"CT_Address0"', '"CT_Address1"', '"CT_Address2"', '"CT_Address3"', '"CT_Address4"', '"CT_Address5"', '"CT_Address6"']

    

    try:
        # ssh远程连接防火墙
        print("正在连接FotiGate 100F")
        ssh_client = SSHClient()
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.connect(**ssh)
        print("连接成功")

        shell = ssh_client.invoke_shell()
        shell.send("config system console\nset output standard\nend\n")
        sleep(1)
        shell.send("show firewall address\n")
        sleep(5)

        output_buffer = b""

        # 将大量条目列出来
        while True:
            sleep(0.5)
            if shell.recv_ready():
                chunk = shell.recv(65535)
                output_buffer += chunk
            else:
                break
        full_output = output_buffer.decode('utf-8', errors='ignore')
        ips = full_output.strip().split('\n')

        # 数据清洗
        for ip in ips:
            if "CT_" in ip and len(ip)>0:
                ip = ip.strip().split()[-1]
                collects.append(ip)
        sleep(1)

        # 分组配置
        batch_size = 600
        shell.send(f"config firewall addrgrp\n")
        sleep(0.5)

        for i, group_name in enumerate(command_grp):
            
            start_index = i * batch_size
            end_index = start_index + batch_size

            current_batch = collects[start_index:end_index]

            if not current_batch:
                print(f"警告：第{i}组数据为空，跳过")
                continue
            members_str = " ".join(current_batch)

            print(f"正在配置组{group_name}, 添加{len(current_batch)}个成员...")

            shell.send(f"edit {group_name}\n")
            sleep(0.2)

            shell.send(f"set member {members_str}\n")
            sleep(2)
            shell.send("next\n")
            sleep(0.5)
        shell.send("end\n")
        print("配置完成")
                        
        ssh_client.close()


    except Exception as e:
        print(f"Error Code： {e}")

        # 打印详细错误栈，方便调试
        import traceback
        traceback.print_exc()
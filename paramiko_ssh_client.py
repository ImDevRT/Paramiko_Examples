import sys
import socket
import time
import paramiko

if len(sys.argv) != 4:
    print("Please provide valid arguments!\n"
          "Usage: \n"
          "python paramiko_ssh_client.py <IP_ADDRESS> <USERNAME> <PASSWORD>")
    sys.exit(1)

shell = None


def connect_remote_server(HOST_ADDRESS, USERNAME, PASSWORD):
    global shell
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=HOST_ADDRESS, username=USERNAME, password=PASSWORD)
    shell = client.invoke_shell()
    shell.settimeout(10)


def send_command(cmd):
    command = cmd + "\n"
    shell.send(command)


def get_output():
    output = ""
    while True:
        try:
            data = shell.recv(1).decode("utf-8")
            output += data
        except socket.timeout:
            break
        time.sleep(0.3)
    return output


if __name__ == "__main__":
    HOST_ADDRESS = sys.argv[1]
    USERNAME = sys.argv[2]
    PASSWORD = sys.argv[3]

    # Send a command and get the output:
    send_command("help")
    output = get_output()
    print(output)

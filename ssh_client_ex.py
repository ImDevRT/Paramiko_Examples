import sys
import time
import socket
import paramiko


class SSHClient:

    def __init__(self, host_address, username, password):
        self.host_address = host_address
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=self.host_address,
                            username=self.username,
                            password=self.password)
        self.shell = self.client.invoke_shell()
        self.shell.settimeout(10)

    def send_command(self, cmd):
        command = cmd + "\n"
        self.shell.send(command)

    def get_output(self):
        output = ""
        while True:
            try:
                data = self.shell.recv(1).decode("utf-8")
                output += data
            except socket.timeout:
                break
            time.sleep(0.3)
        return output

    def close_ssh_client(self):
        self.shell.close()


if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Please provide valid arguments.\n\n"
              "Usage:\n"
              "python ssh_client.py <HOST_ADDRESS> <USERNAME> <PASSWORD>")
        sys.exit(1)

    else:
        host_address = sys.argv[1]
        username = sys.argv[2]
        password = sys.argv[3]
        shell = SSHClient(host_address, username, password)

        # Send commands to the remote server
        shell.send_command("ifconfig")
        shell.send_command("man cat")

        # Read output of the executed commands
        output = shell.get_output()
        print(output)

        # Hangup SSH connection
        shell.close_ssh_client()

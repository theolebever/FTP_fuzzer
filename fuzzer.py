import socket


class Fuzzer:
    def __init__(self, ip, port, username, password, commands, buffer):
        # Initialize the fuzzer with target ip, port, credentials, list of commands to fuzz, and a buffer of payloads
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.commands = commands
        self.buffer = buffer

    def send_command(self, command, payload):
        # Create a new socket and send a single command with the given payload
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                # Connect to the server
                sock.connect((self.ip, self.port))
                sock.recv(1024)

                # If the command is not 'USER', we need to authenticate first
                if command != "USER":
                    sock.send(("USER " + self.username + "\r\n").encode())
                    sock.recv(1024)
                    sock.send(("PASS " + self.password + "\r\n").encode())
                    sock.recv(1024)

                # Send the command with the payload
                sock.send((command + " " + payload + "\r\n").encode())

                # Receive the response
                response = sock.recv(1024)

                # Finally, send the QUIT command to terminate the connection
                sock.send(("QUIT\r\n").encode())
            except ConnectionResetError:
                # If the server resets the connection, print a crash message
                print(f"Command: {command} Buffer: {payload} => CRASH")
            except Exception as e:
                # Print any other exceptions that occur
                print(f"Error: {e}")

    def fuzz(self):
        # Iterate over each command and each payload in the buffer
        for command in self.commands:
            for payload in self.buffer:
                # Print the command and length of payload being fuzzed
                print(f"Fuzzing {command} with length: {len(payload)}")

                # Send the command with the payload
                self.send_command(command, payload)


def main():
    # The IP and port of the target FTP server
    ip = "127.0.0.1"
    port = 21

    # The credentials to authenticate to the FTP server
    username = "test"
    password = "test"

    # The buffer of payloads to send. Start with a single 'A', and add a new 'A' * counter each iteration
    buffer = ["A"]
    counter = 20
    while len(buffer) <= 30:
        buffer.append("A" * counter)
        counter = counter + 100

    # The list of FTP commands to fuzz
    commands = [
        "ABOR",
        "ACCT",
        "ADAT",
        "ALLO",
        "APPE",
        "AUTH",
        "CCC",
        "CDUP",
        "CONF",
        "CWD",
        "DELE",
        "ENC",
        "EPRT",
        "EPSV",
        "FEAT",
        "HELP",
        "LANG",
        "LPRT",
        "LPSV",
        "MDTM",
        "MIC",
        "MKD",
        "MLSD",
        "MLST",
        "MODE",
        "NLST",
        "NOOP",
        "OPTS",
        "PASV",
        "PBSZ",
        "PORT",
        "PROT",
        "PWD",
        "REIN",
        "REST",
        "RMD",
        "RNFR",
        "RNTO",
        "SITE",
        "SIZE",
        "SMNT",
        "STAT",
        "STOU",
        "STRU",
        "SYST",
        "TYPE",
        "XCUP",
        "XMKD",
        "XPWD",
        "XRCP",
        "XRMD",
        "XRSQ",
        "XSEM",
        "XSEN",
    ]

    # Create a new fuzzer and start fuzzing
    fuzzer = Fuzzer(ip, port, username, password, commands, buffer)
    fuzzer.fuzz()


if __name__ == "__main__":
    main()

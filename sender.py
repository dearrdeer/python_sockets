import socket
import tqdm
import os
import sys
import time

SEPARATOR = " "
BUFFER_SIZE = 4096 # send 4096 bytes each time step

filename = sys.argv[1]
host = sys.argv[2]
port = int(sys.argv[3])

filesize = os.path.getsize(filename)
BUFFER_SIZE = min(BUFFER_SIZE)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

s.send(f"{filename}{SEPARATOR}{filesize}".encode())

# start sending the file
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024, leave=True)
with open(filename, "rb") as f:
    while True:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
   		s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))

# close the socket

s.close()


import socket 
import tqdm
import os
from threading import Thread

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8800
BUFFER_SIZE = 4096
SEPARATOR = " "

def get_file(client_socket):
	received = client_socket.recv(BUFFER_SIZE).decode()
	filename, size = received.split(SEPARATOR)
	filename = os.path.basename(filename)
	size = int(size)

	progress = tqdm.tqdm(range(size), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)

	tempname = filename
	copy = 0
	
	while os.path.isfile(tempname):
		copy += 1
		base = filename.split('.')[0]
		type = filename.split('.')[1]
		tempname = base + '_copy' + str(copy) + '.' + type

	filename = tempname
	
	with open(filename, "wb") as f:
		while True:
			bytes_read = client_socket.recv(BUFFER_SIZE)
			if not bytes_read:
				break
			f.write(bytes_read)
			progress.update(len(bytes_read))

	print("File received")
	client_socket.close()


def main():
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((SERVER_HOST, SERVER_PORT))

	server_socket.listen(5)

	print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

	while True:
		client_socket, address = server_socket.accept()
		print(f"[+] {address} is connected.")
		Thread(target=get_file, args=[client_socket]).start()


if __name__ == "__main__":
    main()
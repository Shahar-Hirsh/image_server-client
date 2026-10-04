import socket
import threading
from PIL import Image
import os

images_dir = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(images_dir, exist_ok=True)

def recv_image_data(client_socket, file_name, file_data_len):
    """
    receive the image data and save the image
    :param client_socket: the client socket
    :param file_name:  the image file name
    :param file_data_len: the length of the image data
    :return:None
    """

    data = b''
    while len(data) < file_data_len:
        slice = file_data_len - len(data)
        if slice > 1024:
            data += client_socket.recv(1024)
        else:
            data += client_socket.recv(slice)
            break

    # create the path
    image_path = os.path.join(images_dir, file_name)

    # create the image file
    with open (image_path, "wb") as f:
        f.write(data)

    with Image.open(image_path) as im:
        im.show()

server_soc = socket.socket()
server_soc.bind(("0.0.0.0", 1450))
server_soc.listen(3)


while True:
    client_socket, addr = server_soc.accept()
    print(f"{addr[0]} - connected")

    while True:
        try:
            file_name_len = int(client_socket.recv(2).decode())
            file_name = client_socket.recv(file_name_len).decode()
            file_data_len = int(client_socket.recv(6).decode())
            recv_image_data(client_socket, file_name, file_data_len)
        except Exception as e:
            print(f"client {addr[0]} disconnected due to {str(e)}")
            client_socket.close()
            break

    print(f"{addr[0]} - disconnected")
    client_socket.close()

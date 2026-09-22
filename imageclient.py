import socket
import os

my_soc = socket.socket()
try:
    my_soc.connect(("127.0.0.1", 1450))
except Exception as e:
    print(f"{str(e)} - server is down - try again later")
    my_soc.close()
    exit()

while True:
    file_path = input("enter image file path or q to end ")
    if file_path.lower() == "q":
        break
    if file_path.split(".")[-1] not in ["jpg","png","jpeg","bmp"]:
        print("not a valid image file - try again")
        continue
    if not os.path.isfile(file_path):
        print("image file not exist - try again")
        continue

    # the image file is exist
    file_name = file_path.split("\\")[-1]
    file_name_len = str(len(file_name)).zfill(2)
    print(f"file name = {file_name}")
    # open and read the file as binary data
    with open(file_path, "rb") as f:
        file_data = f.read()
    file_data_len = str(len(file_data)).zfill(6)

    try:
        my_soc.send(file_name_len.encode())
        my_soc.send(file_name.encode())
        my_soc.send(file_data_len.encode())
        my_soc.send(file_data)
        print("the image file successfully send to the server")
    except Exception as e:
        print(f"{str(e)} - problem send / receive data - try again later")
        break

my_soc.close()
print("bye bye")

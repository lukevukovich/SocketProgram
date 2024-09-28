import socket

HOST = "DRACO1"

def get_port() -> int:
    """
    Get the port number from the user.
    """
    good_port = False
    while not good_port:
        port = input("Enter the port number (0 to exit): ")
        try:
            port = int(port)
            if 0 <= port <= 65535:
                good_port = True
            else:
                print("Port number must be between 0 and 65535")
        except ValueError:
            print("Port number must be an integer")

    return port

def main():
    """
    Main function to connect to the server.
    """
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get the port number
    port = get_port()
    if port == 0:
        print("Exit Program")
        return
    
    try:
        # connect to the server on local computer
        client_socket.connect((HOST, port))

        # receive data from the server
        print(f"Server: {client_socket.recv(1024).decode()}")

    except Exception as e:
        print(f"Socket Program Error: {e}")

    finally:
        # close the connection
        client_socket.close()
        print("Connection Closed")

if __name__ == '__main__':
    main()
import socket

HOST = "DRACO1"

def get_port() -> int:
    """
    Get the port number from the user. The port number must be between 0 and 65535. 0 will exit the program.
    """
    good_port = False
    while not good_port:
        port = input(f"Enter port number for host {HOST} (0 to exit): ")
        try:
            port = int(port)
            if 0 <= port <= 65535:
                good_port = True
            else:
                print("Port number must be between 0 and 65535")
        except ValueError:
            print("Port number must be an integer")

    return port

def get_client_input() -> str:
    """
    Get the code and message from client in format: {code}#{message}. 0 will exit the program. Code must be 1 or 2.
    """
    good_input = False
    while not good_input:
        client_input = input("Client Input (0 to exit): ")
        if client_input == "":
            print("Input cannot be blank\n")
        elif client_input == "0":
            return 0, None
        else:
            try:
                code_message = client_input.split("#")
                code = code_message[0]
                message = code_message[1]
                if code != "1" and code != "2":
                    print("Invalid code\n")
                else:
                    if message == "":
                        print("Message cannot be blank\n")
                    else:
                        good_input = True
                
            except Exception:
                print("Invalid Input: Must be in format: {code}#{message}\n")

    return code, message

def main():
    """
    Main function to handle client-server communication. Client will connect and send messages to the server.
    """
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket Created")

    # Get the port number
    port = get_port()
    if port == 0:
        print("Exit Program")
        return
    
    try:
        # Client connects to the server
        client_socket.connect((HOST, port))

        # Receive initial message from the server
        print(f"Server Output: {client_socket.recv(1024).decode()}")

        # Control loop for client-server communication
        exit = False
        while not exit:
            # Get code and message from client
            code, message = get_client_input()

            # Exit program if code is 0
            if code == 0:
                print("Exit Program")
                exit = True
                continue

            # Send message to server
            client_socket.sendall(message.encode())
            print(f"Message Received by Server")
            if code == "1":
                # Echo message from server if code is 1
                print(f"Server Output: {client_socket.recv(1024).decode()}\n")
            else:
                print("")

    except Exception as e:
        # Handle any errors that occur
        print(f"Socket Program Error: {e}")

    finally:
        # close the connection
        client_socket.close()
        print("Connection Closed")

if __name__ == '__main__':
    main()
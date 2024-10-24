import socket
import sys

"""
CMSM-3180-001
Luke Vukovich, Adir Turgeman
SocketProgram.py

NOTE: 'hostname' parameter accepted as command line argument.
"""

def get_port(HOST: str) -> int:
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
                    print("Invalid Code: Code must be: 1 (echo) or 2 (no echo)\n")
                else:
                    if message == "":
                        print("Message cannot be blank\n")
                    else:
                        good_input = True
                
            except Exception:
                print("Invalid Input: Input must be in format: {code}#{message}\n")

    return code, message

def main():
    """
    Main function to handle client-server communication. Client will connect and send messages to the server.
    """
    # Get the host name from the command line argument, exit if missing
    try:
        HOST = sys.argv[1]
    except IndexError:
        print("Socket Program Error: Missing HOSTNAME command line argument")
        sys.exit(1)

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket Created")

    # Get the port number
    port = get_port(HOST)
    if port == 0:
        print("Exit Program")
        return
    
    try:
        # Client connects to the server
        client_socket.connect((HOST, port))
        print(f"Connected to {HOST} on port {port}")

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

            # Receive message from server
            echo = client_socket.recv(1024).decode()
            if code == "1":
                # Echo message from server if code is 1
                print(f"Server Output: {echo}\n")
            else:
                print("")

    except Exception as e:
        # Handle any errors that occur
        print(f"Socket Program Error: {e}")
        sys.exit(1)

    finally:
        # close the connection
        client_socket.close()
        print("Connection Closed")

if __name__ == '__main__':
    main()
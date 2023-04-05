BYTES_TO_RECEIVE = 4096
LENGTH_DATA_SEPARATOR = "|"


def send_data(socket, data):
    """
    Helper function that sends data via a socket, including the data length.
    The data length and the data are separated by the LENGTH_DATA_SEPARATOR.
    """
    data_length = len(data)
    data_with_length = f"{data_length}{LENGTH_DATA_SEPARATOR}{data}"
    socket.send(data_with_length.encode())


def receive_data(socket):
    """
    Helper function that receives variable length data via a socket.
    Uses the LENGTH_DATA_SEPARATOR to identify the data length.
    """
    message = ""
    remaining_message_length = None

    while True:
        data = socket.recv(BYTES_TO_RECEIVE).decode()
        if len(data) == 0:
            return

        if remaining_message_length is None:  # Initial data segment
            message_length, message_segment = data.split(LENGTH_DATA_SEPARATOR, 1)
            remaining_message_length = int(message_length)
        else:
            message_segment = data

        message += message_segment
        remaining_message_length -= len(message_segment)
        if remaining_message_length == 0:
            return message


import time
import os
import sys


def tail_mode(path_file, deep=10):
    """
    Printing new lines in the file
    """
    with open(path_file, "r") as f:
        lines = f.read().splitlines()
        for line in range(-deep, 0):
            last_line = lines[line]
            print(last_line)


def get_last_n_lines(file_name, N):
    # Create an empty list to keep the track of last N lines
    list_of_lines = []
    # Open file for reading in binary mode
    with open(file_name, 'rb') as read_obj:
        # Move the cursor to the end of the file
        read_obj.seek(0, os.SEEK_END)
        # Create a buffer to keep the last read line
        buffer = bytearray()
        # Get the current position of pointer i.e eof
        pointer_location = read_obj.tell()
        # Loop till pointer reaches the top of the file
        while pointer_location >= 0:
            # Move the file pointer to the location pointed by pointer_location
            read_obj.seek(pointer_location)
            # Shift pointer location by -1
            pointer_location = pointer_location -1
            # read that byte / character
            new_byte = read_obj.read(1)
            # If the read byte is new line character then it means one line is read
            if new_byte == b'\n':
                # Save the line in list of lines
                list_of_lines.append(buffer.decode("utf-8", "ignore")[::-1])
                # If the size of list reaches N, then return the reversed list
                if len(list_of_lines) == N+1:
                    return list(reversed(list_of_lines))
                # Reinitialize the byte array to save next line
                buffer = bytearray()
            else:
                # If last read character is not eol then add it in buffer
                buffer.extend(new_byte)
        # As file is read completely, if there is still data in buffer, then its first line.
        if len(buffer) > 0:
            list_of_lines.append(buffer.decode("utf-8", "ignore")[::-1])
    # return the reversed list
    return list(reversed(list_of_lines))


def follow_mode(path_file):
    """
    Waiting and printing new lines in the file
    """
    path_file.seek(0, os.SEEK_END)
    while True:
        line = path_file.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


def check_flags(args):
    """
    Check of the input parameters
    """
    num_lines = 10
    follow = False
    warning_string = 'Use Two Arguments: 1) Path File, 2) "f" or Number of Lines at the End (Default==10)'

    if len(args) == 2:
        return [args[1], num_lines, follow]
    elif len(args) > 3:
        print(warning_string)
        exit()
    elif len(args) == 3:
        try:
            if args[2] == 'f':
                num_lines = 0
                follow = True
                return [args[1], num_lines, follow]
            elif isinstance(int(args[2]), int):
                num_lines = int(args[2])
                return [args[1], num_lines, follow]
        except:
            return warning_string
    else:
        return warning_string


def row_counter(path_file):
    """
    Count rows
    """
    return sum(1 for line in open(path_file))


def check_file(path_file):
    """
    Check of the path_file argument
    """
    if not os.access(path_file, os.F_OK):
        print("File '%s' does not exist" % (path_file))
        exit()
    if not os.access(path_file, os.R_OK):
        print("File '%s' not readable" % (path_file))
        exit()
    if os.path.isdir(path_file):
        print("File '%s' is a directory" % (path_file))
        exit()
    else:
        return path_file


def file_is_small(path_file):
    is_small = False
    if os.stat(path_file).st_size < 1000000:
        is_small = True
    return is_small


if __name__ == '__main__':

    parameters = check_flags(sys.argv)
    
    path_file = parameters[0]
    lines_at_the_end = parameters[1]
    mode = parameters[2]

    path_file = check_file(path_file)
    
    file_is_small = file_is_small(path_file)
    if file_is_small:
        rows_count_in_file = row_counter(path_file)
        if rows_count_in_file < lines_at_the_end:
            print("Rows less than ", lines_at_the_end)
            print("In file rows ", rows_count_in_file)
            exit()

    if mode:
        for line in get_last_n_lines(path_file, 10):
            print(line)
        for line in follow_mode(open(path_file, "r")):
            print(line)
    else:
        for line in get_last_n_lines(path_file, lines_at_the_end):
            print(line)
        exit()

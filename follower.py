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


if __name__ == '__main__':

    parameters = check_flags(sys.argv)

    path_file = parameters[0]
    lines_at_the_end = parameters[1]
    mode = parameters[2]

    path_file = check_file(path_file)

    rows_count_in_file = row_counter(path_file)

    if rows_count_in_file == 0:
        print("File no have rows")
        exit()

    if rows_count_in_file < lines_at_the_end:
        print("Rows less than ", lines_at_the_end)
        print("In file rows ", rows_count_in_file)
        exit()

    if mode:
        if rows_count_in_file > 10:
            tail_mode(path_file)
        else:
            tail_mode(path_file, rows_count_in_file)

        for line in follow_mode(open(path_file, "r")):
            print(line)
    else:
        tail_mode(path_file, lines_at_the_end)

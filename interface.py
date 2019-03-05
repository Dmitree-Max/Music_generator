import sys


def choose_working_mode():
    """
    Function has input with common checks
    :return: (string) function returns each string input
    """
    attempt = 0
    while attempt < 5:
        try:
            mode = input("""
Press 
P - play 
S - safe 
B - both
"""
                         )
            break
        except EOFError:
            if i < 4:
                print("EOFError")
                i += 1
            else:
                print("we ran into System crash")
                sys.exit(-1)
    return mode


def correct_int_input(messege):
    """
    Function has input with common checks
    :param messege: (string) what should user input
    :return: (int) returns input, if it can be converted into int
    """
    while True:
        value = input(messege)
        if str.isnumeric(value):
            return_value = int(value)
            if return_value >= 0:
                break
            print("please write positive number")
        else:
            print("please write a number")

    return return_value

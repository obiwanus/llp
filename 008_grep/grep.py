#!/usr/bin/python3

def grep(expression, input_file):
    if not is_valid(expression):
        return None, "Invalid expression"

    try:
        input_file = open(input_file, 'r')
    except OSError:
        return None, f"Cannot open file {input_file}"

    return True, None


def is_valid(expression):
    return True


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 3:
        print("Usage: grep.py '<expression>' <input_file>")
        sys.exit(1)

    expression, input_file = sys.argv[1], sys.argv[2]
    result, error = grep(expression, input_file)
    if error is not None:
        print(error)
        sys.exit(1)

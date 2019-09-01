#!/usr/bin/python3

def grep(expression, input_file):
    automata = parse(expression)
    if not automata:
        return None, "Invalid expression"

    try:
        input_file = open(input_file, 'r')
    except OSError:
        return None, f"Cannot open file {input_file}"

    return True, None


class ParseError(Exception):
    pass


class RegEx:

    def __init__(self, expression):
        self.subregex_list = []
        self.parse(expression)

    def parse(expression):
        if len(expression) < 1:
            return None

        brackets = {'(': ')', '[': ']'}
        expecting_bracket = None
        subexpr = []

        chars = list(expression)
        while len(chars) > 0:
            char = chars.pop(0)
            if char not in '()[]+*?':
                self.subregex_list.append(Char(char))
            elif char in brackets:
                expecting_bracket = brackets[char]
            elif expecting_bracket:
                if char != expecting_bracket:
                    subexpr.append(char)
                else:
                    # TODO: handle square brackets
                    self.subregex_list.append(RegEx(''.join(subexpr)))
                    expecting_bracket = None
            elif char == '+':
                # TODO:

        if expecting_bracket:
            raise ParseError(f"Expected closing bracket: {expecting_bracket}")





class State:
    READY = 0
    MATCH = 1
    MISMATCH = 2


class Char:

    def __init__(self, char):
        self.char = char
        self.state = State.READY

    def take(self, char):
        assert self.state == State.READY
        if char == self.char:
            self.state = State.MATCH
        else:
            self.state = State.MISMATCH


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

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

    def parse(self, expression):
        if not expression:
            return None

        brackets = {'(': ')', '[': ']'}
        expecting_bracket = None
        subexpr = []

        chars = list(expression)
        while chars:
            char = chars.pop(0)
            if char not in '()[]+*?':
                self.subregex_list.append(Char(char))
            elif char in brackets:
                expecting_bracket = brackets[char]
            elif expecting_bracket:
                if char != expecting_bracket:
                    subexpr.append(char)
                else:
                    subexpr = ''.join(subexpr)
                    if expecting_bracket == ')':
                        subregex = RegEx(subexpr)
                    else:
                        assert expecting_bracket == ']'
                        subregex = RangeRegEx(subexpr)
                    self.subregex_list.append(subregex)
                    expecting_bracket = None
            elif char in '+*?':
                try:
                    prev_regex = self.subregex_list.pop()
                except IndexError:
                    raise ParseError(f"Expected expression before {char}")
                char_to_regex = {
                    '+': OneOrMoreExpr,
                    '*': ZeroOrMoreExpr,
                    '?': ZeroOrOneExpr,
                }
                subregex = char_to_regex[char](prev_regex)
                self.subregex_list.append(subregex)


        if expecting_bracket:
            raise ParseError(f"Expected closing bracket: {expecting_bracket}")


class RangeRegEx(RegEx):

    def parse(self, expression):
        pass


class OneOrMoreExpr:

    def __init__(self, regex):
        self.regex = regex


class ZeroOrMoreExpr:

    def __init__(self, regex):
        self.regex = regex


class ZeroOrOneExpr:

    def __init__(self, regex):
        self.regex = regex



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

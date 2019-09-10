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
        self.start = None
        subregex_list = self.parse(expression)
        self.start_state, self.end_state = self.construct_automaton(subregex_list)

    def parse(self, expression):
        if not expression:
            raise ParseError("Empty expression")

        subregex_list = []

        brackets = {'(': ')', '[': ']'}
        expecting_bracket = None
        subexpr = []

        for i, char in enumerate(expression):
            if expecting_bracket:
                if char != expecting_bracket:
                    subexpr.append(char)
                else:
                    subexpr = ''.join(subexpr)
                    if expecting_bracket == ')':
                        subregex = RegEx(subexpr)
                    else:
                        assert expecting_bracket == ']'
                        subregex = RangeRegEx(subexpr)
                    subregex_list.append(subregex)
                    expecting_bracket = None
                    subexpr = []
            elif char in brackets:
                expecting_bracket = brackets[char]
            elif char in brackets.values():
                raise ParseError(f"Unexpected closing bracket {char} at position {i}")
            elif char in '+*?':
                try:
                    prev_regex = subregex_list.pop()
                except IndexError:
                    raise ParseError(f"Expected expression before {char}")
                char_to_regex = {
                    '+': OneOrMoreExpr,
                    '*': ZeroOrMoreExpr,
                    '?': ZeroOrOneExpr,
                }
                subregex = char_to_regex[char](prev_regex)
                subregex_list.append(subregex)
            else:
                subregex_list.append(Char(char))

        if expecting_bracket:
            raise ParseError(f"Expected closing bracket: {expecting_bracket}")

        return subregex_list

    @staticmethod
    def construct_automaton(subregex_list):
        assert subregex_list, "Empty regex list"
        start_state = State(PASSTHROUGH, out=None)
        end_state = State(MATCH, out=None)
        current_state = start_state

        # Connect all fragments
        while subregex_list:
            # TODO: pipe regex
            next_fragment = subregex_list.pop(0)
            current_state.out = next_fragment.start_state
            current_state = next_fragment.end_state
        current_state.out = end_state

        # Rewire to delete all passthrough states (they were used only for convenience)
        def rewire(state):

            # TODO: debug this!!!!!!!!!!!!! (draw a picture)
            while state.out is not None:
                if state.out.c == PASSTHROUGH:
                    state.out = state.out.out
                if state.c == SPLIT:
                    assert state.out1 is not None
                    rewire(state.out1)
                state = state.out
        rewire(start_state)

        return start_state, end_state


ANY_CHAR = 0
SPLIT = 1
MATCH = 2
PASSTHROUGH = 3


class State:
    def __init__(self, c, out, out1=None):
        self.c = c
        self.out = out
        self.out1 = out1


class Char:
    def __init__(self, c):
        if c == '.':
            c = ANY_CHAR
        self.start_state = State(c, out=None)
        self.end_state = self.start_state


class RangeRegEx(RegEx):

    def parse(self, expression):
        return
        # raise NotImplementedError


class OneOrMoreExpr:

    def __init__(self, regex):
        self.start_state = regex.start_state
        self.end_state = State(SPLIT, out=None, out1=self.start_state)
        regex.end_state.out = self.end_state


class ZeroOrMoreExpr:

    def __init__(self, regex):
        self.start_state = State(SPLIT, out=None, out1=regex.start_state)
        self.end_state = self.start_state
        regex.end_state.out = self.start_state


class ZeroOrOneExpr:

    def __init__(self, regex):
        self.end_state = State(PASSTHROUGH, out=None)
        self.start_state = State(SPLIT, out=regex.start_state, out1=self.end_state)
        regex.end_state.out = self.end_state


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

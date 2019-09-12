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
        self.start, self.end = self.construct_automaton(subregex_list)

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
        start = State(PASSTHROUGH, out=None)
        end = State(MATCH, out=None)
        current = start

        # Connect all fragments
        while subregex_list:
            # TODO: pipe regex
            next_fragment = subregex_list.pop(0)
            current.out = next_fragment.start
            current = next_fragment.end
        current.out = end

        def rewire(state, seen):
            """
            Delete all passthrough states (they were used only for convenience)
            """
            if state in seen:
                return
            seen.add(state)

            while state.out is not None:
                if state.out.c == PASSTHROUGH:
                    state.out = state.out.out
                if state.c == SPLIT:
                    assert state.out1 is not None
                    if state.out1.c == PASSTHROUGH:
                        state.out1 = state.out1.out
                    rewire(state.out1, seen)
                state = state.out

        rewire(start, seen=set())
        start = start.out

        return start, end


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
        self.start = State(c, out=None)
        self.end = self.start


class RangeRegEx(RegEx):

    def parse(self, expression):
        return
        # raise NotImplementedError


class OneOrMoreExpr:

    def __init__(self, regex):
        self.start = regex.start
        self.end = State(SPLIT, out=None, out1=self.start)
        regex.end.out = self.end


class ZeroOrMoreExpr:

    def __init__(self, regex):
        self.start = State(SPLIT, out=None, out1=regex.start)
        self.end = self.start
        regex.end.out = self.start


class ZeroOrOneExpr:

    def __init__(self, regex):
        self.end = State(PASSTHROUGH, out=None)
        self.start = State(SPLIT, out=regex.start, out1=self.end)
        regex.end.out = self.end


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

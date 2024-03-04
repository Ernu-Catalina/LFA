import random


class Grammar:
    def __init__(self, non_terminals, terminals, productions):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions


def generate_strings(grammar, num_strings):
    valid_strings = []
    for _ in range(num_strings):
        valid_strings.append(generate_string(grammar, 'S'))
    return valid_strings


def generate_string(grammar, symbol):
    if symbol in grammar.terminals:
        return symbol
    else:
        production = random.choice(grammar.productions[symbol])
        generated_string = ''.join(generate_string(grammar, s) for s in production)
        return generated_string


class FiniteAutomaton:
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.initial_state = None
        self.accepting_states = set()

    def convert_from_grammar(self, grammar):
        for non_terminal in grammar.non_terminals:
            self.states.add(non_terminal)
        for terminal in grammar.terminals:
            self.alphabet.add(terminal)

        for non_terminal, productions in grammar.productions.items():
            for production in productions:
                if len(production) == 1:  # Singleton production
                    self.transitions.setdefault(non_terminal, {}).setdefault(production, 'ε')
                else:
                    self.transitions.setdefault(non_terminal, {}).setdefault(production[0], production[1])

        self.initial_state = 'S'
        self.accepting_states = grammar.terminals

    def __str__(self):
        transitions_str = "\n".join([f"{state}: {transitions}" for state, transitions in self.transitions.items()])
        return f"States: {self.states}\nAlphabet: {self.alphabet}\nTransitions:\n{transitions_str}"

    def check_string(self, input_string):
        current_state = self.initial_state
        for symbol in input_string:
            if symbol not in self.transitions.get(current_state, {}):
                return False
            current_state = self.transitions[current_state].get(symbol)
            if current_state is None:
                return False
        return current_state in self.accepting_states


if __name__ == "__main__":
    # Grammar definition
    non_terminals = {'S', 'B', 'L'}
    terminals = {'a', 'b', 'c'}
    productions = {
        'S': ['aB'],
        'B': ['bB', 'cL'],
        'L': ['cL', 'aS', 'b']
    }
    grammar = Grammar(non_terminals, terminals, productions)

    # Generating and printing valid strings
    valid_strings = generate_strings(grammar, 5)
    print("Valid Strings:")
    for string in valid_strings:
        print(string)

    # Convert Grammar to Finite Automaton
    fa = FiniteAutomaton()
    fa.convert_from_grammar(grammar)
    print("\nFinite Automaton:")
    print(fa)

    # Checking strings with Finite Automaton
    input_strings = ["abbc", "cabc", "acbcc"]
    for string in input_strings:
        if fa.check_string(string):
            print(f"'{string}' is accepted.")
        else:
            print(f"'{string}' is not accepted.")

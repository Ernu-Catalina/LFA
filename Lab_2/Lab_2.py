import random


class Grammar:
    def __init__(self, non_terminals, terminals, productions):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions

    def __str__(self):
        productions_str = "\n".join([f"{non_terminal} -> {' | '.join(productions)}" for non_terminal, productions in self.productions.items()])
        return f"Non-terminals: {self.non_terminals}\nTerminals: {self.terminals}\nProductions:\n{productions_str}"

    def classify_chomsky(self):
        # Check if the grammar is regular
        regular = all(len(production) <= 2 and (len(production) == 1 or production[0] in self.non_terminals)
                      for productions in self.productions.values() for production in productions)

        # Check if the grammar is context-free
        context_free = all(len(production) == 1 for productions in self.productions.values() for production in productions)

        # Check if the grammar is context-sensitive
        context_sensitive = not regular and not context_free

        # If none of the above are True, the grammar is unrestricted
        if not any([regular, context_free, context_sensitive]):
            return "Type 0 : Unrestricted"
        elif regular:
            return "Type 3 : Regular"
        elif context_free:
            return "Type 2 : Context-Free"
        elif context_sensitive:
            return "Type 1 : Context-Sensitive"


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


def fa_to_regular_grammar(fa):
    non_terminals = set()
    terminals = fa.alphabet
    productions = {}

    # Add non-terminals
    for state in fa.states:
        non_terminal = f'N_{state}'
        non_terminals.add(non_terminal)
        productions[non_terminal] = []

    # Add productions
    for state in fa.transitions:
        for symbol, next_state in fa.transitions[state].items():
            if next_state in fa.accepting_states:
                productions[f'N_{state}'].append(symbol)
            else:
                productions[f'N_{state}'].append(symbol + f'N_{next_state}')

    return Grammar(non_terminals, terminals, productions)


def is_deterministic(fa):
    for state in fa.transitions:
        for symbol, next_state in fa.transitions[state].items():
            if isinstance(next_state, set):
                return False
    return True


def draw_fa_graph(fa):
    print("\nFinite Automaton Graph:")
    for state, transitions in fa.transitions.items():
        for symbol, next_state in transitions.items():
            if isinstance(next_state, str):
                print(f"{state} -- {symbol} --> {next_state}")
            else:
                for s in next_state:
                    print(f"{state} -- {symbol} --> {s}")


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

    # Convert FA to regular grammar
    rg = fa_to_regular_grammar(fa)
    print("\nRegular Grammar:")
    print(rg)

    # Determine if FA is deterministic
    if is_deterministic(fa):
        print("\nThe Finite Automaton is deterministic.")
    else:
        print("\nThe Finite Automaton is non-deterministic.")

    # Draw FA graphically
    draw_fa_graph(fa)

    # Classify Grammar based on Chomsky Hierarchy
    grammar_classification = grammar.classify_chomsky()
    print(f"Grammar Classification: {grammar_classification}")

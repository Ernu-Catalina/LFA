class CNFConverter:
    def __init__(self):
        pass

    def convert_to_cnf(self, grammar_str):
        # Parse the input grammar string
        productions = {}
        for production in grammar_str.split(','):
            left, right = production.strip().split(':')
            left = left.strip()
            right = right.strip()
            if left not in productions:
                productions[left] = []
            productions[left].append(right)

        cnf_grammar = {}

        self.eliminate_epsilon(productions, cnf_grammar)
        self.eliminate_unit_productions(productions, cnf_grammar)
        self.eliminate_terminals(productions, cnf_grammar)
        self.introduce_new_nonterminals(productions, cnf_grammar)
        for symbol in productions.keys():
            cnf_grammar[symbol] = []
        self.convert_to_cnf_form(productions, cnf_grammar)

        return cnf_grammar

    def eliminate_epsilon(self, productions, cnf_grammar):
        # Step 1: Identify non-terminals that can derive ε
        epsilon_nonterminals = set()
        for nonterminal, symbols in productions.items():
            if "ε" in symbols:
                epsilon_nonterminals.add(nonterminal)

        # Step 2: For each epsilon-producing non-terminal, generate new productions
        for nonterminal, symbols in productions.items():
            new_productions = []
            for symbol in symbols:
                if symbol != "ε":
                    for epsilon_set in self.power_set(epsilon_nonterminals):
                        new_production = symbol
                        for epsilon_symbol in epsilon_set:
                            new_production = new_production.replace(epsilon_symbol, "")
                        if new_production:
                            new_productions.append(new_production)
            cnf_grammar[nonterminal] = new_productions

    def eliminate_unit_productions(self, productions, cnf_grammar):
        # Step 1: Identify and eliminate unit productions
        for nonterminal, symbols in productions.items():
            unit_productions = [symbol for symbol in symbols if len(symbol) == 1 and symbol.isupper()]
            while unit_productions:
                unit = unit_productions.pop(0)
                if unit in productions:
                    for unit_symbol in productions[unit]:
                        if unit_symbol not in cnf_grammar[nonterminal]:
                            cnf_grammar[nonterminal].append(unit_symbol)
                            if len(unit_symbol) == 1 and unit_symbol.isupper():
                                unit_productions.append(unit_symbol)
                elif unit not in cnf_grammar[nonterminal]:
                    cnf_grammar[nonterminal].append(unit)

    def eliminate_terminals(self, productions, cnf_grammar):
        # Step 1: Identify and replace terminals with corresponding non-terminals
        terminal_productions = [(nonterminal, symbol) for nonterminal, symbols in productions.items() for symbol in symbols if len(symbol) == 1 and not symbol.isupper()]
        terminal_symbols = set(symbol for _, symbol in terminal_productions)

        # Introduce new non-terminal symbols for terminals
        new_nonterminals = {}
        for symbol in terminal_symbols:
            new_nonterminal = f"{symbol}_NT"
            new_nonterminals[symbol] = new_nonterminal
            cnf_grammar[new_nonterminal] = [symbol]

        # Replace terminals with corresponding non-terminals
        for nonterminal, symbol in terminal_productions:
            if symbol in cnf_grammar[nonterminal]:
                cnf_grammar[nonterminal].remove(symbol)
                cnf_grammar[nonterminal].append(new_nonterminals[symbol])

        # Ensure introduced non-terminals are in all productions
        for _, symbol in terminal_productions:
            for nonterminal in cnf_grammar:
                if symbol not in cnf_grammar[nonterminal]:
                    cnf_grammar[nonterminal].append(new_nonterminals[symbol])

    def introduce_new_nonterminals(self, productions, cnf_grammar):
        # Introduce new non-terminal symbols for any remaining terminal symbols
        terminal_symbols = set(symbol for symbols in productions.values() for symbol in symbols if len(symbol) == 1 and not symbol.isupper())
        for symbol in terminal_symbols:
            if symbol not in cnf_grammar:
                new_nonterminal = f"{symbol}_NT"
                cnf_grammar[new_nonterminal] = [symbol]

    def convert_to_cnf_form(self, productions, cnf_grammar):
        # Convert productions to Chomsky Normal Form
        for nonterminal, symbols in productions.items():
            new_productions = []
            for symbol in symbols:
                if len(symbol) > 2:
                    # Split the production into binary productions
                    for i in range(len(symbol) - 1):
                        binary_production = symbol[i:i + 2]
                        if binary_production not in new_productions:
                            new_productions.append(binary_production)
                else:
                    # If the production has at most two symbols, add it unchanged
                    if symbol not in new_productions:
                        new_productions.append(symbol)

            # Replace symbols with corresponding non-terminals
            for i in range(len(new_productions)):
                if len(new_productions[i]) == 1 and not new_productions[i].isupper():
                    if new_productions[i] in cnf_grammar:
                        new_productions[i] = f"{new_productions[i]}_NT"

            # Update the CNF grammar
            cnf_grammar[nonterminal] = new_productions

    def power_set(self, s):
        s = list(s)
        return [set(s[j] for j in range(len(s)) if (i >> j) & 1) for i in range(2 ** len(s))]


def get_input_grammar():
    grammar_str = input("Enter the grammar (in the format 'S:bA, S:BC, A:a, ...'): ")
    return grammar_str


# Test the CNFConverter class
if __name__ == "__main__":
    converter = CNFConverter()
    input_grammar_str = get_input_grammar()
    cnf_grammar = converter.convert_to_cnf(input_grammar_str)
    print("Input Grammar:")
    print(input_grammar_str)
    print("CNF Grammar:")
    print(cnf_grammar)

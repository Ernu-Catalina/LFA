import random

def generate_combinations(regex):
    combinations = []
    for _ in range(1):  # Limiting to 5 combinations as requested
        combination = ''
        print("Generating combinations for regex:", regex)
        for char in regex:
            if char == 'M':
                combination += 'M' if random.choice([True, False]) else ''
            elif char == 'N':
                combination += 'N' * 2
            elif char == 'O':
                combination += 'O' * 3
            elif char == 'P':
                combination += 'P' * 3
            elif char == 'Q':
                combination += 'Q' if random.choice([True, False]) else ''
            elif char == 'R':
                combination += 'R' if random.choice([True, False]) else ''
            elif char in ['X', 'Y', 'Z']:
                rand_char = random.choice(['X', 'Y', 'Z'])
                combination += rand_char
            elif char == '8':
                combination += '8'
            elif char in ['9', '0']:
                rand_digit = random.choice(['9', '0'])
                combination += rand_digit
            elif char in ['H', 'i']:
                rand_hi = random.choice(['H', 'i'])
                combination += rand_hi
            elif char in ['J', 'K']:
                rand_jk = random.choice(['J', 'K'])
                combination += rand_jk
            elif char == 'L':
                combination += 'L' * random.randint(0, 5)  # Limiting to 5 occurrences
            elif char == 'N':
                combination += 'N' if random.choice([True, False]) else ''
            print(combination)
        combinations.append(combination)
    return combinations

# Generate combinations
regex1 = "M?N^2(O|P)^3Q*R*"
regex2 = "(X|Y|Z)^38+(9|0)"
regex3 = "(H|i)(J|K)L*N?"

combinations1 = generate_combinations(regex1)
combinations2 = generate_combinations(regex2)
combinations3 = generate_combinations(regex3)

print("Combinations for ex1:", combinations1)
print("Combinations for ex2:", combinations2)
print("Combinations for ex3:", combinations3)

def process_sequence(regex):
    sequence = []
    for char in regex:
        if char == '(':
            sequence.append("Start processing group")
        elif char == ')':
            sequence.append("End processing group")
        elif char in ['?', '*', '+', '{']:
            sequence.append(f"Apply repetition quantifier {char}")
        elif char == '|':
            sequence.append("Start processing alternate")
            sequence.append("End processing alternate")
        else:
            sequence.append(f"Process character {char}")
    return sequence

# Example regular expressions
regex1 = "M?N^2(O|P)^3Q*R*"
regex2 = "(X|Y|Z)^38^+(9|0)"
regex3 = "(H|i)(J|K)L*N?"

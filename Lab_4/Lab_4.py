import random


def generate_string(regex):
    generated_string = ''
    for char in regex:
        if char == 'M':
            generated_string += 'M' if random.choice([True, False]) else ''
        elif char == 'N':
            generated_string += 'N' if random.choice([True, False]) else ''
        elif char == 'O':
            generated_string += 'O' * 3
        elif char == 'P':
            generated_string += 'P' * 3
        elif char == 'Q':
            generated_string += 'Q' if random.choice([True, False]) else ''
        elif char == 'R':
            generated_string += 'R' if random.choice([True, False]) else ''
        elif char in ['X', 'Y', 'Z']:
            generated_string += random.choice(['X', 'Y', 'Z'])
        elif char == '8':
            generated_string += '8'
        elif char in ['9', '0']:
            generated_string += random.choice(['9', '0'])
        elif char in ['H', 'i']:
            generated_string += random.choice(['H', 'i'])
        elif char in ['J', 'K']:
            generated_string += random.choice(['J', 'K'])
        elif char == 'L':
            generated_string += 'L' * random.randint(0, 5)  # Limiting to 5 occurrences
    return generated_string


def generate_strings(regex):
    generated_strings = []
    for _ in range(3):  # Generate 3 strings
        generated_string = generate_string(regex)
        generated_strings.append(generated_string)
    return generated_strings


# Prompt user for regular expression input
user_regex = input("Enter a regular expression: ")

# Generate strings complying with the input regular expression
generated_strings = generate_strings(user_regex)
print("Generated strings:", generated_strings)

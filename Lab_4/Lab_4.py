import random


def generate_string(regex):
    generated_string = ''
    i = 0
    while i < len(regex):
        print("Current state of generated string:", generated_string)
        print("Current character in regex:", regex[i])
        if regex[i] == '?':
            if random.choice([True, False]):
                print("Optional character, skipping back")
                i -= 1
            else:
                print("Optional character, proceeding")
            i += 1
        elif regex[i] == '^':
            power = int(regex[i + 1])
            generated_string += generated_string[-1] * (power - 1)
            print("Repeating last character", power, "times")
            i += 2
        elif regex[i] == '(':
            options = ''
            i += 1
            while regex[i] != ')':
                options += regex[i]
                i += 1
            options_list = options.split('|')
            chosen_option = random.choice(options_list)
            generated_string += chosen_option
            print("Choosing from options:", options_list, "Chosen:", chosen_option)
            i += 1
        elif regex[i] == '*':
            times = random.randint(0, 5)
            generated_string += generated_string[-1] * times
            print("Repeating last character", times, "times")
            i += 1
        elif regex[i] == '+':
            times = random.randint(1, 5)
            generated_string += generated_string[-1] * times
            print("Repeating last character (at least once)", times, "times")
            i += 1
        else:
            generated_string += regex[i]
            print("Appending character to generated string:", regex[i])
            i += 1

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

def non_repeat_func(name):
    str_count = {}

    for character in name:
        if character in str_count:
            str_count[character] += 1

        else:
            str_count[character] = 1

    for character in name:

        if str_count[character] == 1:
            return character

    return None

user_input = str(input("Enter the input String : "))
output = non_repeat_func(user_input)
print(f'The first non-repeating character is : {output}')

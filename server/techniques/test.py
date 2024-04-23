numbers = [*range(1, 9)]


def get_sets_of_n(sets, remaining_elements, pair, n):
    if (len(pair) == n):
        sets.append(pair)
    for i in range(len(remaining_elements)):
        picked = remaining_elements[i]
        get_sets_of_n(sets, remaining_elements[i+1:], pair + [picked], n)
    return sets


def create_sets_of_n(elements, n):
    sets = []
    for i in range(len(elements)):
        picked = elements[i]
        remaining_elements = elements[i+1:]
        get_sets_of_n(sets, remaining_elements, [picked], n)
    return sets


sets2 = get_sets_of_n([], numbers, [], 2)

print(sets2)
print(len(sets2))

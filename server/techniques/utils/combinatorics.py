from models.square import Square


class Combinatorics:
    def get_sets_of_n(sets, remaining_elements, pair, n) -> list[list]:
        if (len(pair) == n):
            sets.append(pair)
        for i in range(len(remaining_elements)):
            picked = remaining_elements[i]
            Combinatorics.get_sets_of_n(
                sets, remaining_elements[i+1:], pair + [picked], n)
        return sets

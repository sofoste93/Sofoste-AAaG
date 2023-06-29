import itertools


def generate_anagrams(chars, size, num):
    anagrams = [''.join(p) for p in itertools.permutations(chars, size)]
    return anagrams[:num]

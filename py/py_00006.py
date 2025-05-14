# Comment: Predictable random number generator, independent from python versions
def not_so_random(seed):
    
    # see https://en.wikipedia.org/wiki/Linear_congruential_generator
    m = 2**31
    a = 1103515245
    c = 12345
    while True:
        seed = (a * seed + c) % m
        yield float(seed) / float(m)





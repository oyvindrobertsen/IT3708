def tuple_add(*tuples):
    return tuple(map(sum, zip(*tuples)))
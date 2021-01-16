import math


def binary(probability):
    zero = -probability * math.log2(probability)
    one = -(1 - probability) * math.log2(1 - probability)
    return zero + one

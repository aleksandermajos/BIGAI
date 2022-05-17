scores=[10 ,5, 20, 20, 4, 5, 2, 25, 1]

import sys
import math
import os
import random
import re


def breakingRecords1(scores):
    minimum, maximum = scores[0], scores[0]
    records = [0, 0]
    for score in scores[1:]:
        if score > maximum:
            maximum = score
            records[0] += 1
        if score < minimum:
            minimum = score
            records[1] += 1

    return records

def breakingRecords2(scores):
    high = scores[0]
    low = high
    counter_highs = 0
    counter_lows = 0
    for score in scores:
        if score > high:
            high = score
            counter_highs += 1
        elif score < low:
            low = score
            counter_lows += 1
    return [counter_highs, counter_lows]


def breakingRecords3(scores):
    ma = scores[0]
    mac = 0
    mi = scores[0]
    mic = 0
    for i in scores:
        if i > ma:
            mac += 1
            ma = i
        elif i < mi:
            mic += 1
            mi = i

    rez = []
    rez.append(mac)
    rez.append(mic)

    return rez

if __name__ == '__main__':
    n = int(input())
    breakingRecords1(scores)
    breakingRecords2(scores)
    breakingRecords3(scores)
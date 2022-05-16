arr=[1,2,3,4,5]

import sys
import math
import os
import random
import re

def miniMaxSum(arr):
    arr.sort()
    hold = [None] * int(len(arr) - 3)
    for i in range(0, len(arr) - 3):
        temp = 0
        for j in range(i, i + 4):
            temp = temp + arr[j]
        hold[i] = temp

    print(hold[0], hold[-1])

def miniMaxSum2(arr):
    arr.sort()
    print(sum(arr[0:4]), end = " ")
    print(sum(arr[1:]))

def miniMaxSum3(arr):
    s = sum(arr)
    print(f"{s - max(arr)} {s - min(arr)}")

if __name__ == '__main__':
    n = int(input())
    miniMaxSum(arr)
    miniMaxSum2(arr)
    miniMaxSum3(arr)


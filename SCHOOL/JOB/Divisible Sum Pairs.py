ar=[1, 3, 2, 6, 1, 2]

import math
import os
import random
import re
import sys


def divisibleSumPairs1(n,k,ar):
    acc = 0
    for i, e in enumerate(ar):
        for j in range(i + 1, len(ar)):
            acc += (e + ar[j]) % k == 0
    return acc




def divisibleSumPairs2(n, k, ar):
    # Write your code here
    count = 0
    for i in range (0,n):
        for number in ar[i+1:]:
            if (ar[i] + number) % k ==0:
                count+=1
    return(count)


def divisibleSumPairs4(n, k, ar):
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if i < j and not (ar[i] + ar[j]) % k:
                count += 1

    return count

if __name__ == '__main__':
    n = int(input())

    #arr = list(map(int, input().rstrip().split()))

    divisibleSumPairs1(6,3,ar)

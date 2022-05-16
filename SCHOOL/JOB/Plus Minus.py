arr=[-4, 3, -9, 0, 4, 1]

import math
import os
import random
import re
import sys

# Complete the plusMinus function below.
def plusMinus1(arr):
    x,z,y=0,0,0
    for i in range(0,len(arr)):
        if arr[i]>0:
            x = x + 1
        elif arr[i]<0:
            y = y + 1
        else:
            z = z + 1
    print(x/len(arr))
    print(y/len(arr))
    print(z/len(arr))

def plusMinus2(arr):
    # Write your code here
    count1=0
    count2=0
    count3=0
    for i in arr:
        if i>0:
            count1+=1
        elif i<0:
            count2+=1
        elif i==0:
            count3+=1
        else:
            pass
    div1=count1/n
    div2=count2/n
    div3=count3/n
    print(div1)
    print(div2)
    print(div3)

def plusMinus3(arr):
    posi,nega,z=0,0,0
    for element in arr:
        if element == 0 :
            z += 1
        elif element > 0 :
            posi += 1
        else :
            nega += 1
    print(posi/len(arr))
    print(nega/len(arr))
    print(z/len(arr))

if __name__ == '__main__':
    n = int(input())

    #arr = list(map(int, input().rstrip().split()))


    plusMinus1(arr)
    plusMinus2(arr)
    plusMinus3(arr)

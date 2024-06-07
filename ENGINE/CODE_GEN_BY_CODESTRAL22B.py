'''
    This function sorts an array using the Bubble Sort algorithm.
'''
'''
This function sorts an array using the Bubble Sort algorithm.
It takes as input a list of numbers (array), and then uses two loops to compare each number in the array with the next one.
If the current number is greater than the next one, it swaps them. This process repeats until the array is sorted in ascending order.
'''
def BubbleSort(array):
    # Get the length of the array
    n = len(array)

    # Loop over all elements in the array
    for i in range(n):
        # Loop over elements that have not been sorted yet
        for j in range(0, n-i-1):
            # If current element is greater than the next one
            if array[j] > array[j+1]:
                # Swap the elements
                array[j], array[j+1] = array[j+1], array[j]

                # Print out the swapped elements for debugging purposes
                print(array[j], array[j+1])

                # Print out the current state of the array for debugging purposes
                print(array)

array = [64, 34, 25, 12, 22, 11, 90]
BubbleSort(array)
print("Sorted array is:", array)
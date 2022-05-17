inputData = "S;V;iPad C;M;mouse pad C;C;code swarm S;C;OrangeHighlighter"



import sys


# Read input lines and remove '\n' and '\r' characters to avoid bugs
inputData = [line.rstrip('\n\r') for line in sys.stdin.readlines()]

# Loop through all the input lines and print each resulting string
for inputString in inputData:

    # Extract the words without the S/C and M/C/V indicators
    wordsString = inputString[4:]

    # Split branch
    if inputString[0] == 'S':

        # Initialize an empty list to put all the words in
        wordList = []
        word = ''
        # Add a '(' character at the end of the words string to indicate end of string and to reduce the number of if/else statements
        wordsString += '('
        # Loop through all the character indexes of the words string
        for i in range(len(wordsString)):
            # Add the current character to the current word
            word += wordsString[i]
            # When the next character is uppercase, that means we reached the last letter of a word, add that word to the list and reset the word variable
            if wordsString[i + 1].isupper():
                wordList.append(word)
                word = ''
            # When the next character is '(' that means we reached the last letter of the last word, add that word to the list and break from the loop
            elif wordsString[i + 1] == '(':
                wordList.append(word)
                break
        # Join all the words from our word list with spaces in between them and lowercase all of the letters
        result = ' '.join(wordList).lower()

    # Combine branch
    else:

        # Create a word list and populate it with all the words from our words string
        wordList = wordsString.split(' ')
        # If the words represent a class name, capitalize the first word
        if inputString[2] == 'C':
            wordList[0] = wordList[0].capitalize()
        # Loop through all the words except the first one and capitalize them
        for i in range(1, len(wordList)):
            wordList[i] = wordList[i].capitalize()
        # Join all the words together and put a pair of brackets at the end if the words represent a method name
        result = ''.join(wordList)
        if inputString[2] == 'M':
            result += '()'

    print(result)
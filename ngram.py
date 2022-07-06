# This program generates a number of sentences using text files and an Ngram model. The degree of the Ngram model is specified by the
# user.
# 
# To use, type: "python ngram.py n m [file name(s)]" into the terminal, where n is the Ngram model and m is the number of sentences you want to generate. To use 
# multiple files, list all their names one after the other.

import random
import sys
import re

def main() :

    n = int(sys.argv[1])
    m = int(sys.argv[2])

    print("This program generates random sentences based on an Ngram model and was created by Anna Ho.")
    print("Command line settings: " + sys.argv[0] + " " + str(n) + " " + str(m) + "\n")
    
    total_words = 0 # stores the total number of words in the string. used for if the user wanted a unigram
    ngram_array = [] # array of ngrams
    history_dict = {} # stores the number of times the history was seen
    ngram_dict = {} # stores the number of times a word appears after the history
    freq_table = {} # stores the relative frequencies


    # adds the appropriate number of start tags to the start variable depending on the n gram model
    start_variable = ""
    for i in range(0, n - 1):
        start_variable += "<s> " 

    # opens each one of the text files from the command line arguments
    for i in range(3, len(sys.argv)): 

        book = open(str(sys.argv[i]))
        book_string = book.read().lower()
        
        book_string = book_string.replace("\n", " ") 
        
        # splits the text up into sentences 
        sentences = re.findall(r".*?[\.|\!|\?]", book_string) 
        
        for sentence in sentences: 
            
            # split sentences into words based on white space
            words = sentence.split()
            
            # if the length of the sentence is less than n, get rid of it
            if (len(words) < n):
                book_string = book_string.replace(sentence, '')
        
        # searches for end punctuation and adds start and end tags
        book_string = re.sub(r"\!", " ! <end> " + start_variable, book_string)
        book_string = re.sub(r"\.", " . <end> " + start_variable, book_string)
        book_string = re.sub(r"\?", " ? <end> " + start_variable, book_string)        
        
        # searches for other types of punctuation that can appear mid sentence and adds a space to both sides of the punctuation so 
        # it can be tokenized
        book_string = re.sub(r",\s?", " , ", book_string)
        book_string = re.sub(r"-", " - ", book_string)
        book_string = re.sub(r"‐", " ‐ ", book_string)
        book_string = re.sub(r":", " : ", book_string)
        book_string = re.sub(r"\(", " ( ", book_string)
        book_string = re.sub(r"\)", " ) ", book_string)
        book_string = re.sub(r"_", " _ ", book_string)
        
        # searches for quotes and semicolons and removes them from the string so that the sentences make more sense
        book_string = re.sub(r"[“”\";]", "", book_string)

        # adds start tags to beginning of book string and removes the start tags from end of the book string
        book_string = start_variable + book_string
        book_string = book_string[::-1].replace(start_variable[::-1], '', 1)[::-1]
        
        # splits the string based on white space and puts that into an array
        book_array = book_string.split()
        
        # loops through each element in the book array and adds it to the ngram array
        for element in book_array: 
            
            ngram_array.append(element)

            # if the length of the array equals n, update the frequency of the word in the dictionaries
            if (len(ngram_array) == n):
                
                # creates the ngram dictionary for unigrams
                if (n == 1): 
                    
                    # updates frequency of element in ngram_dict
                    if (element in ngram_dict): 
                        ngram_dict[element] += 1
                    else:
                        ngram_dict[element] = 1
                    total_words += 1
                
                # creates ngrams and calculates frequency of the history and word for n > 1 
                else:                 

                    word = ngram_array[-1]
                    history = tuple(ngram_array[-n:len(ngram_array)-1])

                    # checks if the history is already a key in the history dictionary. if it is, add 1 to the frequency. 
                    # if not, initialize the frequency to 1
                    if (history in history_dict): 
                        history_dict[history] += 1
                    else:
                        history_dict[history] = 1

                    # checks if the history is already a key in the ngram dictionary. if it doesn't create an empty nested dictionary 
                    # as for that key's value and set the frequency of seeing that word following the history to 1
                    if (history in ngram_dict):  
                        # checks if the word is a key in the ngram dictionary. if it is, add 1 to frequency. if not, intialize frequency to 1
                        if (word in ngram_dict[history]):  
                            ngram_dict[history][word] += 1
                        else: 
                            ngram_dict[history][word] = 1
                    else: 
                        ngram_dict[history] = {}
                        ngram_dict[history][word] = 1
                
                # removes the 1st element of the array so we can continue making ngrams from the book_array
                ngram_array.pop(0)
            
        book.close()

    # calculates frequency of seeing a word in the entire work for when n = 1
    if (n == 1): 
        for word in ngram_dict:
            freq_table[word] = ngram_dict[word]/total_words
    
    # calculates the relative frequencies of seeing each word coming after the history for ngrams where n > 1
    else: 
        for history in ngram_dict:
            freq_table[history] = {} # creates an empty list as the value for each key
            for word in ngram_dict[history]:
                freq_table[history][word] = ngram_dict[history][word]/history_dict[history]

    # formats start tag so it's the same format as the history column of the frequency table
    start_variable = []
    for i in range(0, n - 1):
        start_variable.append("<s>")

    start_variable = tuple(start_variable)

    # creates and prints the number of sentences specified by the user
    for i in range (0, m): 

        sentence = ""
        history = start_variable # start from the start variable
        flag = True # flag for when we've seen the end tag so we know when to exit the while loop

        # chooses the words for a sentence by generating a random number and adding the frequencies of each word to a count variable until count is larger than
        # the random number then that word is chosen
        while (flag == True): 

            # generates a random number 
            num = random.random()
            count = 0
            
            # generates sentences for unigrams. randomly selects a word and adds it to a sentence based on its frequency without using any history
            if (n == 1): 

                for word in freq_table: 

                    count += freq_table[word]

                    if (count > num):
                        
                        # if the word is an end tag, print out the sentence and start creating a new sentence
                        if (word == "<end>"): 
                            print(sentence + "\n")
                            flag = False
                        
                        # adds the word to the sentence
                        else: 
                            # if the word is end punctuation, it adds the word to the end of the sentence without the space so that
                            match = re.match(r"\!|\.|\?", word)
                            if (match): 
                                sentence = ''.join([sentence, word])
                            else: 
                                sentence = ' '.join([sentence, word])
                        
                        break # break to avoid picking more words after count is already greater than the random num
            
            # generates sentences for if n > 1. randomly selects a word based on the frequency that it appears following the history and adds it to the sentence
            else: 

                for word in freq_table[history]:
                    
                    count += freq_table[history][word]

                    if (count > num):

                        # if the word is an end tag, print out the sentence and start creating a new sentence
                        if (word == "<end>"): 
                            print(sentence + "\n")
                            flag = False
                        
                        # adds the word to the sentence and updates the history to begin looking for the next word
                        else: 
                            
                            # if the word is end punctuation, it adds the word to the end of the sentence without the space so that it looks more like a normal sentence
                            match = re.match(r"\!|\.|\?", word)
                            
                            if (match): 
                                sentence = ''.join([sentence, word])
                            
                            # if the history was the start variable, then the word is capitalized and a space isn't added in front
                            elif (history == start_variable):
                            
                                sentence = ''.join([sentence, word.capitalize()])
                            
                            else: 
                                
                                sentence = ' '.join([sentence, word])
                            
                                # changes history to a list so it can be modified 
                                history = list(history)
                                
                                # updates history by removing the first word and adding the chosen word to the end of the list
                                history.pop(0)
                                history.append(word)

                                history = tuple(history)
                    
                        break # breaks to avoid picking words after count is greater than the random num


if __name__ == '__main__':
    main()
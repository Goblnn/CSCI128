# Isaac Lane
# CSCI 128 - Section K
# Assessment 8
# References: None
# Time: 2 hours

import math

def dot_product(v1, v2):
    product = 0
    for i in range(len(v1)):
        product += v1[i] * v2[i]

    return int(product)

def magnitude(v):
    sum = 0
    for num in v:
        sum += num**2

    mag = math.sqrt(sum)
    print(v)
    print(mag)
    return mag

def cosine(v1, v2):
    dot = dot_product(v1, v2)
    mag1 = magnitude(v1)
    mag2 = magnitude(v2)

    if(mag1 == 0 or mag2 == 0):
        return 0.00
    else:
        cosine = dot / (mag1 * mag2)

        return cosine

def words_to_vector(index_array, word_array):
    frequency = []

    for i in range(len(index_array)):
        frequency.append(0) 

    print(index_array)

    for word in word_array:
        print(word)
        if word in index_array:
            word_index = index_array.index(word)
            frequency[word_index] += 1

    print("")
    return frequency 

def join_frequency_vectors(fv1, fv2):
    final = []

    for i in range(len(fv1)):
        final.append(fv1[i] + fv2[i])

    return final

def get_document():
    docu = []
    lines = int(input("NUM LINES> "))

    for i in range(lines):
        line = input(f"Line {i+1}> ")
        line = line.split()
        docu.append(line)

    return docu

def clean_document_line(line):
    to_remove = ".,:;?!1234567890"
    to_split = "-_"

    i = 0
    while i < len(line):
        for char in to_remove:
            line[i] = line[i].replace(char, "")

        line[i] = line[i].replace('"', "")
        line[i] = line[i].replace("'", "")
        
        for char in to_split:
            if(char in line[i]):
                temp = line[i].split(char)
                for j in range(len(temp)):
                    if(j == 0):
                        line[i] = temp[j].lower()
                    else:
                        line.insert(i + j, temp[j].lower())

        line[i] = line[i].lower()
        i += 1

    i = 0
    while i < len(line):
        word = line[i]  
        if word == "":
            line.pop(i)
            if not line:
                break
        else:
            i += 1

    return line

def create_index_array(doc_1, doc_2):
    unique = []

    for line in doc_1:
        for word in line:
            if word not in unique:
                unique.append(word)

    for line in doc_2:
        for word in line:
            if word not in unique:
                unique.append(word)

    return unique

if __name__ == "__main__":
    doc1 = get_document()
    doc2 = get_document()

    for i in range(len(doc1)):
        doc1[i] = clean_document_line(doc1[i])

    for i in range(len(doc2)):
        doc2[i] = clean_document_line(doc2[i])

    empty = True
    i = 0
    while i < len(doc1):
        for word in doc1[i]:
            if word != "":
                empty = False
        
        if empty == True:
            doc1.pop(i)
            if not doc1:
                break
        else:
            i += 1
        

    empty = True
    i = 0
    while i < len(doc2):
        for word in doc2[i]:
            if word != "":
                empty = False
        
        if empty == True:
            doc2.pop(i)
            if not doc2:
                break
        else:
            i += 1

    if doc1 == [] or doc2 == []:
        print("OUTPUT ERROR: At least one document is empty!")
    else:
        index_array = create_index_array(doc1, doc2)

        frequency1 = []
        for i in index_array:
            frequency1.append(0)

        for line in doc1:
            tempf = words_to_vector(index_array, line)
            frequency1 = join_frequency_vectors(frequency1, tempf)

        frequency2 = []
        for i in index_array:
            frequency2.append(0)

        for line in doc2:
            tempf = words_to_vector(index_array, line)
            frequency2 = join_frequency_vectors(frequency2, tempf)
            
        print("")
        print(index_array)
        print(doc1)
        print(doc2)
        print(frequency1)
        print(frequency2)

        frequency_final = join_frequency_vectors(frequency1, frequency2)

        cos = cosine(frequency1, frequency2)

        print(f"OUTPUT {cos*100:.2f}%")
        
        if(cos > .75):
            print("OUTPUT Very Similar")
        elif(cos > .5):
            print("OUTPUT Similar")
        elif(cos > .25):
            print("OUTPUT Not Very Similar")
        else:
            print("OUTPUT Not Similar")
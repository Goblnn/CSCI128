# Code Review 8

def dot_product(v1, v2):
    dotProduct = 0
    for i in range(len(v1)):
        dotProduct += v1[i] * v2[i]
    return dotProduct


def magnitude(vector):
    square_sum = 0
    for num in vector:
        square_sum += num**2
    return square_sum**0.5


def cosine(v1, v2):
    return dot_product(v1, v2) / (magnitude(v1) * magnitude(v2))


def words_to_vector(index_array, word_array):
    freq_vect = []
    for word in index_array:
        freq_vect.append(word_array.count(word))
    return freq_vect


def join_frequency_vectors(freq_vect1, freq_vect2):
    joint_counts = []
    for i in range(len(freq_vect1)):
        joint_counts.append(freq_vect1[i] + freq_vect2[i])
    return joint_counts


def get_document():
    num_lines = int(input("NUM LINES> "))
    document = []
    for i in range(num_lines):
        line = input(f"LINE {i+1}> ").split()
        document.append(line)
    return document


def clean_document_line(line):
    # this loop will split the words into two words if there are dashes
    # and underscore
    split_words = []
    for word in line:
        # replace the _ and - with a space and then split on space
        temp_word = word.replace("_", " ").replace("-", " ").split()
        split_words.extend(temp_word)
    
    # this loop will remove all invalid characters and then add
    # the clean word to the output
    bad_chars = [".", ",", ";", ":", "\'", "\"", "?", "!"]
    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    clean_line = []
    for word in split_words:
        clean_word = ""
        for char in word:
            # handle if character should be skipped (bad_char or number)
            if char in bad_chars or char in digits:
                continue
            # char is valid add to output
            clean_word += char
        # add clean_word to clean_line 
        if clean_word != "":
            clean_line.append(clean_word.lower())
    return clean_line


def create_index_array(d1, d2):
    array = []
    for line in d1:
        for word in line:
            if word not in array:
                array.append(word)
    for line in d2:
        for word in line:
            if word not in array:
                array.append(word)
    return array


if __name__ == "__main__":
    # get 2 documents
    doc_1 = get_document()
    doc_2 = get_document()
    # clean doc 1
    clean_doc_1 = []
    for line in doc_1:
        clean_line = clean_document_line(line)
        # check that the line is not empty
        if len(clean_line) != 0:
            clean_doc_1.append(clean_line)
    # clean doc 2
    clean_doc_2 = []
    for line in doc_2:
        clean_line = clean_document_line(line)
        # check that the line is not empty
        if len(clean_line) != 0:
            clean_doc_2.append(clean_line)
    if clean_doc_1 == [] or clean_doc_2 == []:
        print("OUTPUT ERROR: At least one document is empty!")
    else:
        # compute the index array
        idx_arr = create_index_array(clean_doc_1, clean_doc_2)
        # convert documents to vectors
        doc_vec1 = words_to_vector(idx_arr, clean_doc_1[0])
        for i in range(len(clean_doc_1)):
            if(i == 0):
                continue
            else:
                doc_vec1 = join_frequency_vectors(doc_vec1, words_to_vector(idx_arr, clean_doc_1[i]))

        doc_vec2 = words_to_vector(idx_arr, clean_doc_2[0])
        for i in range(len(clean_doc_2)):
            if(i == 0):
                continue
            else:
                doc_vec2 = join_frequency_vectors(doc_vec2, words_to_vector(idx_arr, clean_doc_2[i]))
        # join the frequency vectors
        freq_counts = join_frequency_vectors(doc_vec1, doc_vec2)
        # compute the cosine similarity
        similarity = cosine(doc_vec1, doc_vec2)
        print(f"OUTPUT {(similarity*100):.2f}%")
        if similarity > 0.75:
            print("OUTPUT Very Similar")
        elif similarity > 0.5:
            print("OUTPUT Similar")
        elif similarity > 0.25:
            print("OUTPUT Not Very Similar")
        else:
            print("OUTPUT Not Similar")
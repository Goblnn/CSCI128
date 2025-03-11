doc1 = [[''], ['']]
doc2 =  [['ants', 'like', 'apples']]

empty = True
i = 0
while i < len(doc1):
    print(f"start {doc1}")
    for word in doc1[i]:
        print(word)
        if word != "":
            empty = False
            print("uh oh")
        print("")
    
    if empty == True:
        print(f"remove {doc1}")
        doc1.pop(i)
        if not doc1:
            break
    else:
        i += 1
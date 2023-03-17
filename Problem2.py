# Function to that froups 2 elements of a string as a list element
def Diagraph(text):
    Diagraph = []
    group = 0
    for i in range(2, len(text), 2):
        Diagraph.append(text[group:i])
        group = i
    Diagraph.append(text[group:])
    return Diagraph

# Function to fill a letter in a string element if 2 letters in the same string matches
def pairing(text):
    k = len(text)
    new_word = ''
    text = text.lower()
    if k % 2 == 0: # If the string is even handler
        for i in range(0, k, 2):
            if text[i] == text[i + 1]: #if both chars are in a pair
                new_word = text[0:i + 1] + str('x') + text[i + 1:] #Replaces with x
                new_word = pairing(new_word) # recersive call to repeat with new value
                break
            else:
                new_word = text
    else: # Odd hanndler
        for i in range(0, k - 1, 2):
            if text[i] == text[i + 1]: #if both chars are in a pair
                new_word = text[0:i + 1] + str('x') + text[i + 1:]
                new_word = pairing(new_word) # recersive call to repeat with new value
                break
            else:
                new_word = text
    return new_word

# Fuction that looks through 5x5 matrix for element then returns the location
def search(mat, element):
    for x in range(5):
        for y in range(5):
            if (mat[x][y] == element):
                return x, y

#List of all characters
list1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm',
         'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Function to generate the 5x5 square matrix using key
def generateTable(word, list1):
    key_letters = []
    compElements = []
    word = word.lower()

    # adds to key letters of not in word
    for i in word:
        if i not in key_letters:
            key_letters.append(i)

    #If not in the key letters then add to comp element
    for i in key_letters:
        if i not in compElements:
            compElements.append(i)

    #adds all missing elements to the comp list
    for i in list1:
        if i not in compElements:
            compElements.append(i)

    #returns the finale matrix as a 5x5
    matrix = []
    while compElements != []:
        matrix.append(compElements[:5])
        compElements = compElements[5:]
    return matrix

#Applied the spec 2 the row handler
def encryptRow(matr, e1r, e1c, e2r, e2c):
    char1 = ''
    if e1c == 4:
        char1 = matr[e1r][0]
    else:
        char1 = matr[e1r][e1c + 1]

    char2 = ''
    if e2c == 4:
        char2 = matr[e2r][0]
    else:
        char2 = matr[e2r][e2c + 1]
    return char1, char2

#applies spec 3 the colum handler
def encryptColumn(matr, e1r, e1c, e2r, e2c):
    char1 = ''
    if e1r == 4:
        char1 = matr[0][e1c]
    else:
        char1 = matr[e1r + 1][e1c]

    char2 = ''
    if e2r == 4:
        char2 = matr[0][e2c]
    else:
        char2 = matr[e2r + 1][e2c]

    return char1, char2

#applies spec 4 the rect rule
def encryptRectangle(matr, e1r, e1c, e2r, e2c):
    char1 = matr[e1r][e2c]
    char2 = matr[e2r][e1c]
    return char1, char2

def encrypt(Matrix, plainList):
    CipherList = []
    if len(plainList[-1]) != 2:
        plainList[-1] = plainList[-1] + 'z'
    for i in range(0, len(plainList)):
        c1 = 0
        c2 = 0
        ele1_x, ele1_y = search(Matrix, plainList[i][0])    #Finds index in matrix
        ele2_x, ele2_y = search(Matrix, plainList[i][1])

        if ele1_x == ele2_x:  # Row rule
            c1, c2 = encryptRow(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)
            # Get 2 letter cipherText
        elif ele1_y == ele2_y: # Column rule
            c1, c2 = encryptColumn(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)
        else: #Rect rule
            c1, c2 = encryptRectangle(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)

        cipher = c1 + c2
        CipherList.append(cipher)

        CipherText = ""
        for i in CipherList:
            CipherText += i
    return CipherText

# Decrption
def decrypt(Cipher, Key):
    plain_text = ""
    plain_text = str(plain_text)
    for i in range(len(Cipher)): # looks through the Cipher spilt into pairs
        if i%2 == 0:
            (elm1_x, elm1_y) = search(Key, Cipher[i]) # finds index
            (elm2_x, elm2_y) = search(Key, Cipher[i+1])

            if elm1_x == elm2_x:    # Row rule
                plain_text = plain_text + str(Key[elm1_x][(elm1_y-1)%5])
                plain_text = plain_text + str(Key[elm1_x][(elm2_y-1)%5])

            elif elm1_y == elm2_y:  # Column rule
                plain_text = plain_text + str(Key[(elm1_x-1)%5][elm1_y])
                plain_text = plain_text + str(Key[(elm2_x-1)%5][elm1_y])

            else:   #Rect rule
                plain_text = plain_text + str(Key[elm1_x][elm2_y])
                plain_text = plain_text + str(Key[elm2_x][elm1_y])

    if(plain_text[-1] == 'z' and len(plain_text)%2 == 0): #removes last index if added
        plain_text = plain_text[:-1]
    return plain_text

def Decryption(CipherText, key, list1):
    matrix = generateTable(key, list1)
    return decrypt(CipherText, matrix)

key = "Monarchy"
print("Key text:", key)
Matrix = generateTable(key, list1)

text_Plain = 'instruments'
text_Plain = text_Plain.lower()
PlainTextList = Diagraph(pairing(text_Plain))

print("Plain Text:", text_Plain)
CipherText = encrypt(Matrix, PlainTextList)

print("CipherText:", CipherText)
print("DepyrptText:", Decryption(CipherText, key, list1))


text_Plain = 'electrical'
text_Plain = text_Plain.lower()
PlainTextList = Diagraph(pairing(text_Plain))

print("Plain Text:", text_Plain)
CipherText = encrypt(Matrix, PlainTextList)

print("CipherText:", CipherText)
print("DepyrptText:", Decryption(CipherText, key, list1))

text_Plain = 'python'
text_Plain = text_Plain.lower()
PlainTextList = Diagraph(pairing(text_Plain))

print("Plain Text:", text_Plain)
CipherText = encrypt(Matrix, PlainTextList)

print("CipherText:", CipherText)
print("DepyrptText:", Decryption(CipherText, key, list1))
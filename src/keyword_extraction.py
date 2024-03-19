import csv

BloomstaxonomieDE = [[], [], [], [], [], []]
BloomstaxonomieEN = [[], [], [], [], [], []]


def Initialize():
    with open('bloom_keywords_en_de.csv', 'r', encoding='utf-8') as csv_datei:
        csv_reader = csv.reader(csv_datei, delimiter=';')
        next(csv_reader)
        rowNumber = 0
        for row in csv_reader:
            if rowNumber == 0:
                for i in range(0, 6):
                    BloomstaxonomieDE[i].extend([element.strip() for element in row[i].split(',')])
            if rowNumber == 1:
                for i in range(0, 6):
                    BloomstaxonomieEN[i].extend([element.strip() for element in row[i].split(',')])
            rowNumber += 1



def IsInBloom(KeyWord):
    Initialize()
    KeyWord = KeyWord.capitalize()
    print(KeyWord)
    for i in range(0, 6):
        print(BloomstaxonomieEN[i])
        if KeyWord in BloomstaxonomieDE[i] or KeyWord in BloomstaxonomieEN[i]:
            return i
    return 'N'

# Takes a string and split it into a list removing all seperators 
# Returns a List of strings
def tokenize(text):
    separators = ['.', ',', ':', ';', '!', '?', ' ', '#']
    for sep in separators:
        text = text.replace(sep, '|')
    return text.split('|')

# Takes a question of type string and returns the Blooms Category of this question
def getBloom(question :str):
    tokenList = tokenize(question)
    for token in tokenList:


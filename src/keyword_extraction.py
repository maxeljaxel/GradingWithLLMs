import csv

BloomstaxonomieDE = [[], [], [], [], [], []]
BloomstaxonomieEN = [[], [], [], [], [], []]


def Initialize():
    """This function will take the data from the file bloom_keywords_en_de.csv and 
        fill both arrays - BloomstaxonomieDE und BloomstaxonomieEN with the corresponding data.
        Both arrays consist of 6 subarrays, each one is reserved for exactly one category
        in the bloostaxonomie

        Parameters
        ----------
        no Parameters

        Output
        --------
        filled arrays BloomstaxonomieDE and BloomstaxonomieEN

        """
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


#TODO   What if in more than one category?

def isInBloom(keyWord):
    """Will compare a string keyWord to each word from the bloomstaxonomie,
        and if the Keyword matches a word from the tax., will return the corresponding
        category

        Parameters
        ----------
        keyWord : str, required
            The string that will be checked.

        Output
        ------
        a number between 0 and 5, if KeyWord is in the tax. category 0-5
        N -> if KeyWord is not in a tax. category
        """

    #initialize bloomstaxonomie in the english and german version
    Initialize()
    #since the csv contains words with the first letter capitalized -> do the same for the keyWord
    keyWord = keyWord.capitalize()
    #checke if the word is in the english or german version of the taxonomie
    for i in range(0, 6):
        for word in BloomstaxonomieDE[i] + BloomstaxonomieEN[i]:
            if word[:len(keyWord)] == keyWord:
                return i
    #if keyword is abbreviation, check if the abbreviation is in the taxonomie
            if keyWord[len(keyWord)-1] == '.':
                if word[:len(keyWord)-1] == keyWord[:len(keyWord)-1]:
                    return i
    #if not -> return N
    return 'N'





import os
from os.path import isfile, join
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import sys


nltk.download('punkt')




ROOT = './'
EXTENSION = ".txt"
BEGIN = "lib"

dataDict = {}#definicion del diccionario


def readFiles():#leemos todos los archivos y los agregamos en una lista
    listFiles = []
    for base, dir, files in os.walk(ROOT):
        for file in files:
            fich = join(base, file)
            if fich.endswith(EXTENSION) and BEGIN in fich:
                listFiles.append(fich)
    return listFiles


def removeChars(txt):#eliminamos las punctuaciones
    txt = re.sub('[%s]' % re.escape(string.punctuation), ' ', txt)
    return txt



def cleanText(txt):
    rootList=[]
    stm = SnowballStemmer('spanish')
    cleanData = removeChars(txt)
    tokens = nltk.word_tokenize(cleanData)
    cleanTokens = nltk.word_tokenize(cleanData)
    #obtenemos el stoplist del archivo
    ostoplist = open("stoplist.txt", "r")
    stoplist = ostoplist.read()
    ostoplist.close()
    

    #recorremos los tokens y removemos todos los stopwords
    for token in tokens:
        if token in stoplist:
                cleanTokens.remove(token)

    #guardamos en una nueva lista la raiz de los tokens limpios
    for token in cleanTokens:
        rootList.append(stm.stem(token))
            
    return rootList



def build(listFiles):
	dict={}
    #recorremos todos los archivps
	for file in listFiles:
        #limpiamos el archivo a analizar
		tokens = cleanText((open(file, encoding='utf-8').read().lower()))
		
        #llenamos el diccionario del indice invertido
		for token in tokens:
			if token not in dict:
				dict[token] = {}
				dict[token]['lib'] = []
			if file not in dict[token]['lib']:
				dict[token]['lib'].append(file)

        #ordenamos de acuerdo al tamaño de creciente a decreciente y sacamos los 500 terminos mas frecuentes
        #de toda la coleccion
		newDic = sorted(dict, key=lambda token: len(dict[token]['lib']), reverse=True)[:500]

		#finalmente los filtramos
		for token in newDic:
			if token not in dataDict:
				dataDict[token] = []
			dataDict[token] = dict[token]['lib']
    
    #retornamos el diccionario con sus items ya ordenados
	return sorted(dataDict.items())



def saveFile(save, dataDict):#guardamos la dataDict en el archivo
	
    out = open(save, 'w')
    out.reconfigure(encoding='utf-8')

    for key, value in dataDict:
        print(key,":",value, file=out)


def recovery(txt):
    print(txt)

def L(key):
    stm = SnowballStemmer('spanish')
    token = stm.stem(key.lower())
    return dataDict[token]


def AND(a, b):
    ans = []
    minLen = min(len(a), len(b))
    n = 0
    i = 0
    j = 0
    while(n < minLen):
        if(a[i] == b[j]):
            ans.append(a[i])
            i += 1
            j += 1
        elif(int(a[i][-5]) > int(b[j][-5])):
            j += 1
        else:
            i += 1
            
        n += 1

    return ans


def OR(a, b):
    ans = []
    i = 0
    j = 0
    while(i < len(a) and j < len(b)):
        if(a[i] == b[j]):
            ans.append(a[i])
            i += 1
            j += 1
        elif(int(a[i][-5]) > int(b[j][-5])):
            ans.append(b[j])
            j += 1
        else:
            ans.append(a[i])
            i += 1
            

    if(i != j):

        if(i == len(a)):
            ans += b[j:len(b)]

        else:
            ans += a[i:len(a)]

    return ans


def AND_NOT(a, b):
    ans = []
    i = 0
    j = 0
    while(i < len(a) and j < len(b)):
        if(a[i] == b[j]):
            i += 1
            j += 1
        elif(int(a[i][-5]) < int(b[j][-5])):
            ans.append(a[i])
            i += 1
        else:
            j += 1
            
    if(i < len(a)):
        ans += a[i:len(a)]

    return ans


def main():

    listFiles = readFiles()
    dataDict = build(listFiles)
    saveFile("out.txt", dataDict)
    print("AND : ")
    recovery(AND(AND(L('anillo'), L('hobbit')),L('Gandalf')))
    print("OR : ")
    recovery(OR(OR(L('anillo'), L('hobbit')),L('Gandalf')))
    print("AND-NOT :")
    recovery(OR(AND_NOT(L('anillo'), L('hobbit')),L('Gandalf')))
    


if __name__ == "__main__":
    main()

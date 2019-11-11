import re


# Retire les espaces blanc aux extremites d'une chaine de caractere
#   '  les pains ' -> 'les pains'
def removeEndSpace(chaine):
    if chaine[-1:] == ' ':
        return removeEndSpace(chaine[:-1])
    elif chaine[:1] == ' ':
        return removeEndSpace(chaine[1:])
    else:
        return chaine


def analyzeHyphen(chaine):
    regexKey = "^[\s]*[\d]{1,2}[A-B,a-b]{1}[\s]*$"
    regexTempo = "^[\s]*[\d]{1,3}[\s]*$"
    regexLength = "^[\s]*[\d]{1,3}[:][\d]{1,2}[\s]*$"

    if chaine.count('-') == 4 :
        return chaine.split('-')
    elif chaine.count('-') == 5:
        temp = chaine.split('-')
        if re.match(regexLength,temp[-1]) and re.match(regexTempo,temp[-2]) and re.match(regexKey, temp[-3]):


            return temp
    else :
        print("Error split chaine  : {0}".format(chaine))
        return("NULL")



def analyzeHyphenTest():
    regexKey = "^[\s]*[\d]{1,2}[A-B,a-b]{1}[\s]*$"
    regexTempo = "^[\s]*[\d]{1,3}[\s]*$"
    regexLength = "^[\s]*[\d]{1,3}[:][\d]{1,2}[\s]*$"

    str1 = "Gatekeeper - Forgotten - 8A - 120-03:58"
    str2 = "Jean-Luc - Le Sabbat - 10A - 84-07:01"
    print(analyzeHyphen(str1))
    if re.match(regexKey, analyzeHyphen(str1)[2]):
        print("str1 key successful !")
    if re.match(regexTempo, analyzeHyphen(str1)[3]):
        print("str1 tempo succeful !")
    if re.match(regexLength, analyzeHyphen(str1)[4]):
        print("str1 length succeful !")
    print(analyzeHyphen(str2))

analyzeHyphenTest()
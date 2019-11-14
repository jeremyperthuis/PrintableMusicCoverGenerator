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
            return([temp[0]+"-"+temp[1],temp[2],temp[3],temp[4],temp[5]])
        else:
            return("erreur")
    else :
        print("Error split chaine  : {0}".format(chaine))
        return("NULL")

# Save in a txt file the last path
def WriteLastPath(path):
    file = open("savePath.txt",'w', encoding="utf8")
    file.write(path)

def GetLastPath():
    file=open("savePath.txt",'r', encoding="utf8")
    if(file.read() == ""):
        return("\\")
    else:
        return(file.read())
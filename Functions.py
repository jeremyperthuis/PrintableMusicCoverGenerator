# Retire les espaces blanc aux extremites d'une chaine de caractere
#   '  les pains ' -> 'les pains'
def removeEndSpace(chaine):
    if chaine[-1:] == ' ':
        return removeEndSpace(chaine[:-1])
    elif chaine[:1] == ' ':
        return removeEndSpace(chaine[1:])
    else:
        return chaine

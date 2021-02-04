import re
import os
import logging

def removeEndpointSpace(chaine):
    """
    Remove Blank space at the beginning and end of the string
    eg : ' test ' -> 'test'
    :param chaine:
    :return: chaine without blank space
    """
    if chaine[-1:] == ' ':
        return removeEndpointSpace(chaine[:-1])
    elif chaine[:1] == ' ':
        return removeEndpointSpace(chaine[1:])
    else:
        return chaine


def splitRawTitle(chaine):

    regexKey = "^[\s]*[\d]{1,2}[A-B,a-b]{1}[\s]*$"
    regexTempo = "^[\s]*[\d]{1,3}[\s]*$"
    hyphen_nbr = chaine.count('-')
    data=dict()
    title_split = chaine.split('-')
    # Cas sans tempo ni clé "artiste - titre"
    if hyphen_nbr == 1 :
        data["artist"] = removeEndpointSpace(title_split[0])
        data["title"] = removeEndpointSpace(title_split[1])
        data["display_title"] = data["artist"] +" - "+ data["title"]
        data["key"] = ""
        data["tempo"] = ""
        return data

    # Cas normal -> "artiste - titre - key - tempo
    elif hyphen_nbr == 3:
        data["artist"] = removeEndpointSpace(title_split[0])
        data["title"] = removeEndpointSpace(title_split[1])
        data["display_title"] = data["artist"] + " - " + data["title"]

        if re.match(regexKey,title_split[2]):
            data["key"] = removeEndpointSpace(title_split[2])
        else:
            data["key"] = ""

        if re.match(regexTempo, title_split[3]):
            data["tempo"] = removeEndpointSpace(title_split[3])
        else:
            data["tempo"] = ""

        return data

    # Cas "-" dans artiste -> "artiste-artiste - titre - key - tempo
    elif hyphen_nbr == 4:
        if re.match(regexTempo,title_split[-1]) and re.match(regexKey, title_split[-2]):
            data["artist"] = removeEndpointSpace("{0}-{1}".format(title_split[0],title_split[1]))
            data["title"] = removeEndpointSpace(title_split[2])
            data["display_title"] = data["artist"] + " - " + data["title"]
            data["key"] = removeEndpointSpace(title_split[3])
            data["tempo"] = removeEndpointSpace(title_split[4])
            return data
        else:
            return("erreur")
    else :
        print("Error split chaine  : {0}".format(chaine))
        return {"artist":"none","title":"none","display_title":"none","key":"none","tempo":"none"}

# Save in a txt file the last path
def writeLastPath(path):
    file = open(os.path.abspath("themes/savePath.txt"),'w', encoding="utf8")
    file.write(path)

def getLastPath():
    """
        If exist, open file which contain path to last opened directory, creates one instead.
        :return String path if existed, None if not
    """
    file_path = os.path.abspath("themes/savePath.txt")
    try :
        file = open(file_path,'r', encoding="utf8")
        logging.info("read file : savePath.txt")
        return (file.read())
    except IOError:
        file = open(file_path, 'w', encoding="utf8")
        logging.info("Error IO file doesnt exists : savePath.txt created")
        return os.path.abspath('/')



def isMP3(file):
    regex_mp3 = "^.*\.mp3$"
    if re.match(regex_mp3,file):
        return True
    else:
        return False

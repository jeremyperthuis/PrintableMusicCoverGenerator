# TextCoverSongTitle 1.5
![License MIT](https://img.shields.io/cocoapods/l/AFNetworking.svg)

TextCoverSongTitle s'adresse à tout les mecs bloqué à l'ère du CompactDisc.
Il permet de faciliter  l'organisation de ses CD ~~illégalements~~ gravés en générant des pochettes contenant le numéro des pistes avec artistes et titres ainsi que
certaines metadonnées utiles comme le tempo ou la tonalité (utile pour les discs-jockeys).

### Prérequis :
* Windows 7, 8 , 10
* Python 3.5

#### Formatage des titres
Les titres doivent être de la forme "artiste - titre - clé - tempo"
les informations de clé et de tempo sont optionnelles et peuvent être concaténées au titre automatiquement avec un programme tel
que [Mixed in Key](https://mixedinkey.com/).
Pour l'instant seul les fichiers .mp3 sont acceptés 
> Pour les fanboys des formats FLAC et WAV, il y aura des mises à jour prochainement.

#### Comment ça marche ?
les morceaux sources du CD doivent être rangés dans un dossier spécifique, à la sélection du dossier les fichiers sont importés
par ordre alphabétique. (les morceaux doivent êtres gravés par ordre alphabetiques)
> Possibilité de modifier l'ordre dans la prochaine mise à jour !
 
 Le programme permet de modifier les titres lorsque ceux-ci sont trop long.
 Lors de la génération de la pochette, un fichier *tracklist.txt* est crée dans le dossier source.

 

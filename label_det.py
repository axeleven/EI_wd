"""
Etiquetage déterministe de notre échantillon d'entrainement:
On prend un tweet, et on décide comme suit (règles décidées à partir des observations des étiquettes données manuellement):
S'il cite une source, ou retweete un compte "fiable" (appartenant à dico_media_italiens), le tweet est catalogué comme neutre --> score 1
Sinon:
S'il contient un mot du lexique de la rage, du drame ou de la peur, ou qu'il contient plus de majuscules que de minuscules, il est catalogué comme sentiment négatif --> score 0
Sinon:
S'il ne contient pas de ponctuation forte (!, ?, ...), il est catalogué comme neutre
S'il en contient:
S'il a un mot du lexique du rire, il est catalogué comme joyeux --> score 2
Sonon, il est catalogué comme sentiment négatif --> score 0
"""

import re

def type_de_caractere(c):
    if len(c) != 1:
        return "erreur"
    if c.islower():
        return "minuscule"
    elif c.isupper():
        return "majuscule"
    elif c.isalpha():
        return "lettre (non standard)"
    else:
        return "pas une lettre"


dico_rage = {
    "rabbia": None, "merda": None,
    "odio": None, "che schifo": None, "basta": None, "schifo": None, "nervi": None, "incazzare": None,
    "incazzo": None, "vaffanculo": None, "bastardo": None, "merda": None, "incazzato": None, "incazzata": None,
    "furioso": None, "furiosa": None, "che rabbia": None, "stronzo": None, "coglione": None,
    "rottura": None, "vogliamo": None, "vergogna": None, "vergognatevi": None, "vomitare": None,
    "schifo": None, "fastidio": None, "urta": None, "odio": None, "ridicolo": None,
    "buffone": None, "inaccettabile": None, "scandaloso": None, "pena": None, "inutile": None,
    "arrabbiato": None, "incazzato": None, "urlo": None, "grido": None, "rompe": None, "spacco": None
}



dico_drame = {
    "dramma": None, "tragedia": None, "distrutto": None, "incredulo": None, "finita": None,
    "spezza": None, "troppo": None, "aiuto": None, "oddio": None,
    "disastro": None, "crollo": None, "pezzi": None, "sconvolto": None, "orribile": None,
    "piangere": None, "tristezza": None, "addio": None, "dolore": None, "rovinato": None,
    "morto": None, "abbandonati": None,  "strazio": None,
    "triste": None, "agonia": None, "devastante": None, "desolazione": None,
    "male": None, "finita": None, "urlare": None,
    "perdita": None, "terribile": None
}


dico_peur = {
    "paura": None, "tremando": None, "panico": None, "ansia": None, "aiuto": None,
    "oddio": None, "male": None, "ansia": None, "panico": None, 
    "spaventa": None, "agitato": None,  "inquietante": None, 
    "scappo": None, "tremo": None, "incubo": None, "insicuro": None, "inquietante": None,
    "terribile": None, "shock": None, 
    "terrorizzato": None, "agito": None, "blocco": None, "panico": None, 
    "impazzendo": None, "svenendo": None, "ansia": None, "incubo": None, "paurissima": None,
    "terrore": None, "tensione": None
}

dico_fun = {
    "ahah": None, "ahaha": None, "ahahah": None, "ahahaha": None, "lol": None, "lmao": None,
    "muoio": None, "morendo": None, "rido": None, "ridendo": None, "morire": None,
    "ridere": None, "forte": None, "esilarante": None, "comicità": None,
    "scherzo": None, "ironico": None, "divertente": None, "umorismo": None, "sorriso": None,
    "felice": None, "felicità": None, "gioia": None, "contento": None, "contenta": None, "spettacolo": None,
    "fantastico": None, "bellissimo": None, "adoro": None, "top": None, "epico": None, "geniale": None,
    "volando": None, 
    "scena": None, "pazzesco": None, "epic": None,  "grande": None,
    "mito": None, "mitico": None, "bravo": None, "bravissimo": None, "meraviglioso": None,
    "super": None, "straordinario": None, "crepapelle": None, "bello": None, "bellissimo": None
}

dico_media_italiens = {
    "@Agenzia_Ansa": None,
    "@repubblica": None,
    "@Corriere": None,
    "@ilpost": None,
    "@fattoquotidiano": None,
    "@SkyTG24": None,
    "@TgLa7": None,
    "@RaiNews": None,
    "@RaiTre": None,
    "@RaiUno": None,
    "@RaiDue": None,
    "@LaStampa": None,
    "@ilsole24ore": None,
    "@LaVeritaWeb": None,
    "@Adnkronos": None,
    "@gazzetta_it": None,
    "@quotidianonet": None,
    "@ilgiornale": None,
    "@il_messaggero": None,
    "@ilfattoquotidiano": None,
    "@Tgcom24": None,
    "@fanpage": None,
    "@HuffPostItalia": None,
    "@agi_agenzia": None,
    "@internazionale": None,
    "@ilfoglio_it": None,
    "@Avvenire_NEI": None,
    "@ilmanifesto": None,
    "@Libero_official": None,
    "@ilriformista": None,
    "@iltempo": None,
    "@ilsecoloxix": None,
    "@ilpiccolo": None,
    "@gazzettadelsud": None,
    "@gazzettadiparma": None,
    "@gds_it": None,
    "@gazzettino": None,
    "@ilrestodelcarlino": None,
    "@lanazione": None,
    "@ilmattino": None,
    "@ilmattinodipadova": None,
    "@messveneto": None,
    "@lagazzettadelmezzogiorno": None,
    "@gazzettadimantova": None,
    "@gazzettadireggio": None,
    "@nuovaferrara": None,
    "@gazzettadimodena": None,
    "@laprovinciacr": None,
    "@laprovinciapv": None,
    "@laprovinciadilecco": None,
    "@laprovinciadisondrio": None,
    "@laprovinciadivarese": None,
    "@laprovinciadibergamo": None,
    "@laprovinciadicomo": None,
    "@laprovinciadibrescia": None,
    "@laprovinciadimantova": None,
    "@laprovinciadipavia": None,
    "@laprovinciadivarese": None,
    "@laprovinciadilecco": None,
    "@laprovinciadisondrio": None,
    "@laprovinciadicomo": None,
    "@laprovinciadibergamo": None,
    "@laprovinciadibrescia": None,
    "@laprovinciadimantova": None,
    "@laprovinciadipavia": None,
    "@laprovinciadivarese": None,
    "@laprovinciadilecco": None,
    "@laprovinciadisondrio": None,
    "@laprovinciadicomo": None,
    "@laprovinciadibergamo": None,
    "@laprovinciadibrescia": None,
    "@laprovinciadimantova": None,
    "@laprovinciadipavia": None,
    "@laprovinciadivarese": None,
    "@laprovinciadilecco": None,
    "@laprovinciadisondrio": None,
    "@laprovinciadicomo": None,
    "@laprovinciadibergamo": None,
    "@laprovinciadibrescia": None,
    "@laprovinciadimantova": None,
    "@laprovinciadipavia": None,
    "@laprovinciadivarese": None,
    "@laprovinciadilecco": None,
    "@laprovinciadisondrio": None,
    "@laprovinciadicomo": None,
    "@laprovinciadibergamo": None,
    "@laprovinciadibrescia": None,
    "@laprovinciadimantova": None,
    "@laprovinciadipavia": None,
    "@laprovinciadivarese": None,
    "@laprovinciadilecco": None,
    "@laprovinciadisondrio": None,
    "@laprovinciadicomo": None,
    "@laprovinciadibergamo": None,
    "@laprovinciadibrescia": None,
    "@laprovinciadimantova": None,
    "@laprovinciadipavia": None,
    "@laprovinciadivarese": None,
    "@laprovinciadilecco": None,
    "@laprovinciadisondrio": None,
    "@laprovinciadicomo": None,
    "@laprovinciadibergamo": None,
    "@laprovinciadibrescia": None,
    "@laprovinciadimantova": None,
    "@laprovinciadipavia": None,
    "@laprovinciadivarese": None,
    "@laprovinciadilecco": None,
    "@laprovinciadisondrio": None,
    "@laprovinciadicomo": None,
    "@laprovinciadibergamo": None,
    "@laprovinciadibrescia": None,
    "@laprovinciadimantova": None,
    "@laprovinciadipavia": None,
    "@laprovinciadivarese": None,
    "@laprovinciadilecco": None,
    "@laprovinciadisondrio": None,
    "@laprovinciadicomo": None,
    "@laprovinciadibergamo": None,
    "@laprovinciadibrescia": None,
    "@laprovinciadimantova": None,
    "@laprovinciadipavia": None,
    "@laprovinciadivarese": None,
    "@laprovinciadilecco": None,
    "@laprovinciadisondrio": None,
    "@laprovinciadicomo": None,
    "@laprovinciadibergamo": None,
    "@laprovinciadibrescia": None,
    "@laprovinciadimantova": None,
    "@laprovinciadipavia": None,
    "@laprovinciadivarese": None,
    "@laprovinciadilecco": None,
    "@laprovinciadisondrio": None,
    "@laprovinciadicomo": None,
    "@laprovinciadibergamo": None,
    "@laprovinciadibrescia": None,
    "@laprovinciadimantova": None,
    "@laprovinciadipavia": None,
    "@laprovinciadivarese": None,
    "@laprovinciadilecco": None,
    "@laprovinciadisondrio": None,
    "@laprovinciadicomo": None,
    "@laprovinciadibergamo": None,
    "@laprovinciadibrescia": None,
    "@laprovinciadimantova": None,
    "@laprovinciadipavia": None,
    "@laprovinciadivarese": None,
    "@laprovinciadilecco": None,
    "@laprovinciadisondrio": None,
    "@laprovinciadicomo": None,
    "@laprovinciadibergamo": None,
    "@laprovinciadibrescia": None,
    "@laprovinciadimantova": None,
    "@laprovinciadipavia": None,
    "@laprovinciadivarese": None,
    "@laprovinciadilecco": None,
    "@laprovinciadisondrio": None,
    "@laprovinciadicomo": None,
    "@laprovinciadibergamo": None,
    "@laprovinciadibrescia": None,
    "@laprovinciadimantova": None,
    "@laprovinciadipavia": None,
    "@laprovinciadivarese": None,
    "@laprovinciadilecco": None,
    "@laprovinciadisondrio": None,
    "@laprovinciadicomo": None,
    "@laprovinciadibergamo": None,
    "@laprovinciadibrescia": None,
    "@laprovinciadimantova": None,
    "@laprovinciadipavia": None,
    "@laprovinciadivarese": None,
    "@laprovinciadilecco": None,
    "@laprovinciadisondrio": None,
    "@laprovinciadicomo": None,
    "@laprovinciadibergamo": None,
    "@laprovinciadibrescia": None,
    "@laprovinciadimantova": None,
    "@laprovinciadipavia": None,
    "@laprovinciadivarese": None,
    "@laprovinciadilecco": None,
    "@laprovinciadisondrio": None,
    "@laprovinciadicomo": None,
    "@laprovinciadibergamo": None,
    "@laprovinciadibrescia": None,
    "@laprovinciadimantova": None,
    "@laprovinciadipavia": None,
    "@laprovinciadivarese": None,
    "@laprovinciadilecco": None,
    "@laprovinciadisondrio": None,
    "@laprovinciadicomo": None,
    "@laprovinciadibergamo": None,
    "@INGVterremoti": None
}
 



def lab(str):
    #sépare le tweet avec " ", ":", ","
    lst = re.split(r"[ :,]", str)

    #booléens indiquant la satisfaction aux critères retenus
    url = False
    fiable = False
    lexique = False
    ponctu = False
    rire = False


    #détection de retweet de médias fiables
    if lst[0] == "RT":
        if len(lst)>1 and lst[1] in dico_media_italiens:
            fiable = True


    #compte majuscules et minuscuels
    min = 0
    maj = 0


    #on parcourt la liste, en ignorant ce qui est mis entre guillements
    entre_guillemet = False
    for i in range(len(lst)):
        elt = lst[i]
        if len(elt)>0 and elt[0] == "»":
            entre_guillemet = False

        if entre_guillemet == True:
            pass

        if len(elt)>0 and elt[0] == "«":
            entre_guillemet = True

        
        #détecte citations
        if elt[:3] == "http":
            url = True
        
        #détecte lexiques
        if elt in dico_drame or elt in dico_peur or elt in dico_rage:
            lexique = True
        
        #détecte ponctuation forte
        if elt == '!' or elt == '?' or elt=="...":
            ponctu = True
        
        #détecte rire
        if elt in dico_fun:
            rire = True
        
        #parcout un mot, compte sa teneur en majuscules et s'il est rattaché à de la ponctuation forte 
        for c in elt:
            if c == '!' or c == '?':
                ponctu = True
            
            rep = type_de_caractere(c)

            if rep == 'minuscule':
                min+=1
            elif rep== 'majuscule':
                maj+=1
    

    #arbre de décision
    if url:
        return 1
    if fiable:
        return 1
    if lexique:
        return 0
    if maj>min:
        return 0
    if not(ponctu):
        return 1
    if rire:
        return 2
    return 0
    



import pandas as pd

def ajouter_labels(fichier_entree, fichier_sortie, colonne_texte="Content"):
    # lecture de l'échantillon
    df = pd.read_csv(fichier_entree)

    # étiquetage ligne par ligne
    df["label"] = df[colonne_texte].astype(str).apply(lab)

    # sauvegarde du nouveau fichier
    df.to_csv(fichier_sortie, index=False)
    print(f"fichier sauvegardé sous : {fichier_sortie}")


#nous avons eu besoin d'une deuxième fonction d'étiquetage pour équilibrer les labels 0 et 1
def ajouter_labels_limites(fichier_entree, fichier_sortie, colonne_texte="Content", max_0=50000, max_1=50000):
    # lecture de l'échantillon
    df = pd.read_csv(fichier_entree)


    lignes_selectionnees = []
    nb_0, nb_1 = 0, 0

    for _, ligne in df.iterrows():
        texte = str(ligne[colonne_texte])
        label = lab(texte)

        if label == 0 and nb_0 < max_0:
            ligne["label"] = label
            lignes_selectionnees.append(ligne)
            nb_0 += 1

        elif label == 2:
            ligne["label"] = label
            lignes_selectionnees.append(ligne)
 
        elif label == 1 and nb_1 < max_1:
            ligne["label"] = label
            lignes_selectionnees.append(ligne)
            nb_1 += 1

        if nb_0 >= max_0 and nb_1 >= max_1:
            break

    #résultat
    df_resultat = pd.DataFrame(lignes_selectionnees)
    df_resultat.to_csv(fichier_sortie, index=False)
    print(f"fichier sauvegardé dans : {fichier_sortie}")



entree = input("Chemin du fichier échantillon CSV : ").strip()
sortie = input("Nom du fichier de sortie : ").strip()
ajouter_labels_limites(entree, sortie)

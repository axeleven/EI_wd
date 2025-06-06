"""
Etiquetage déterministe de l'échantillon d'entrainement pour truth
Etiquette d'un truth: moyenne des scores de colère de ses tokens (scores renseignés dans dict_tokens) (si un token n'est pas dans le dictionnaire, il est simplement ignoré), ajusté par sa teneur en majuscules
"""

import emoji
import spacy

nlp = spacy.load("en_core_news_sm")

def nettoyer_et_lemmatiser(texte):
    texte = emoji.demojize(texte, delimiters=("", ""))
    doc = nlp(texte.lower())
    tokens = [
        token.lemma_ for token in doc
        if not token.is_stop and not token.is_punct and not token.like_url and not token.like_email
    ]
    return " ".join(tokens)



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
    

dict = {'!': [0.0, 0], 'm': 0.2654545454545455, 'currently': 0.0, 'struggle': 0.0, 'feeling': 0.30999999999999994, 'offend': 0.3, 'drs': 0.0, 'office': 0.0, 'worry': 0.0, 'body': 0.05, 'heck': 0.0, 'wrong': 0.4000000000000001, 'seriously': 0.06666666666666667, 'contemplate': 0.0, 'get': 0.3111111111111111, 'tube': 0.0, 'tie': 0.0, 'normal': 0.0, 'everyday': 0.0, 'thing': 0.1, 'occupy': 0.0, 'mind': 0.0, 'give': 0.0, 'time': 0.0, 'start': 0.0, 'secondary': 0.0, 'school': 0.0, 'age': 0.0, 'night': 0.0, 'cry': 0.0, 'lose': 0.0, 'sleep': 0.0, 'thought': 0.2, 'day': 0.35714285714285715, 'not': 0.2708333333333333, 'usual': 0.0, 'oh': 0.3, 'bother': 0.24571428571428572, 'low': 0.0, 'grade': 0.0, 'physics': 0.0, 'midterm': 0.0, 'grandmother': 0.0, 'come': 0.03333333333333333, 'stay': 0.2333333333333333, 'permanently': 0.0, 'difficult': 0.0, 'person': 0.2833333333333334, 'tell': 0.0, 'false': 0.0, 'story': 0.0, 'people': 0.21428571428571427, 'rest': 0.1, 'you': 0.1, 'little': 0.11, 'appalled': 0.1, 'away': 0.4, 'becuz': 0.6, 'cuz': 0.6, 'dangerous': 0.4, 'badman': 0.6, 'ah': 0.6, 'didn': 0.55, 't': 0.53, 'wish': 0.2, 'president': 0.2, 'hardly': 0.2, 'know': 0.25, 'hate': 0.6222222222222222, 'quiet': 0.2, 'smile': 0.2, 'think': 0.28857142857142853, 'sit': 0.0, 'voice': 0.0, 'sound': 0.0, 've': 0.175, 'food': 0.0, 'mouth': 0.0, 'need': 0.3, 'way': 0.20000000000000004, 'rude': 0.35, 'hear': 0.2, 'treatment': 0.4, 'friend': 0.21428571428571427, 'jail': 0.2, 'inhuman': 0.2, 'realise': 0.2, 'happen': 0.2, 'netherlands': 0.2, 'damage': 0.0, 'wristwatch': 0.0, 'like': 0.1457142857142857, 'include': 0.0, 'violent': 0.0, 'act': 0.0, 'commit': 0.0, 'bad': 0.0, 'go': 0.21500000000000002, 'aggravate': 0.0, 'tomorrow': 0.0, 'argument': 0.3, 'dear': 0.3, 'sarcastic': 0.06666666666666667, 'ivspirit': 0.0, 'href': 0.0, 'http': 0.0, 'translatethis': 0.0, 'intend': 0.23, 'develop': 0.23, 'albeit': 0.23, 'riku': 0.23, 'stubborn': 0.35750000000000004, 'oppose': 0.23, 'open': 0.23, 'book': 0.23, 'plot': 0.23, 'ish': 0.23, 'issue': 0.23, 'determine': 0.0, 'read': 0.0, 'backdrop': 0.0, 'old': 0.30000000000000004, 's': 0.0, 'examine': 0.0, 'adventure': 0.0, 'path': 0.0, 'material': 0.0, 'immediately': 0.0, 'begin': 0.0, 'emerge': 0.0, 'phenomenon': 0.0, 'disgust': 0.8500000000000001, 'bus': 0.8666666666666667, 'conductor': 0.8, 'throw': 0.4, 'woman': 0.8, 'oiut': 0.8, 'minibus': 0.8, 'simply': 0.8, 'pay': 0.8, 'fare': 0.8, 'luggage': 0.8, 'don': 0.5166666666666666, 'gut': 0.7, 'say': 0.2733333333333333, 'gigantic': 0.0, 'spider': 0.0, 'climb': 0.4, 'face': 0.03333333333333333, 'flat': 0.0, 'description': 0.0, 'hurt': 0.4166666666666667, 'refuse': 0.8, 'listen': 0.8, 'spiteful': 0.8, 'hurtful': 0.8, 'sniping': 0.8, 'express': 0.6, 'badly': 0.6, 'ignore': 0.6, 'girl': 0.1, 'enter': 0.2, 'division': 0.2, 'work': 0.4, 'greet': 0.2, 'everybody': 0.2, 'compere': 0.0, 'party': 0.35, 'effort': 0.0, 'rolling': 0.0, 'thwart': 0.0, 'immobile': 0.0, 'love': 0.325, 'cold': 0.0, 'nipping': 0.0, 'nose': 0.0, 'warm': 0.0, 'clothe': 0.0, 'find': 0.125, 'take': 0.1, 'test': 0.1, 'date': 0.9, 'somebody': 0.9, 'pretend': 0.9, 'lie': 0.9, 'treassure': 0.9, 'establish': 0.1, 'rule': 0.1, 'comp': 0.1, 'end': 0.21999999999999997, 'planning': 0.1, 'session': 0.1, 'resolve': 0.1, 'conflict': 0.1, 'anger': 0.05, 'fix': 0.1, 'heat': 0.3, 'discussion': 0.3, 'spouse': 0.3, 'concern': 0.3, 'new': 0.3, 'house': 0.3, 'overall': 0.7, 'dark': 0.7, 'uncomfortable': 0.7, 'choose': 0.7, 'disrupt': 0.7, 'group': 0.75, 'youngster': 0.9, 'dress': 0.9, 'fad': 0.9, 'talk': 0.45, 'foul': 0.9, 'language': 0.9, 'insult': 0.6, 'pedestrian': 0.9, 'road': 0.9, 'impolite': 0.9, 'passenger': 0.9, 'close': 0.03333333333333333, 'nice': 0.0, 'appointment': 0.0, 'drink': 0.0, 'coffee': 0.0, 'togehter': 0.0, 'strop': 0.5, 'bit': 0.5, 'grumpy': 0.5, 'miss': 0.5, 'certain': 0.1, 'occasion': 0.1, 'fight': 0.1, 'boyfriend': 0.1, 'door': 0.1, 'child': 0.24, 'let': 0.0, 'blink': 0.0, 'heartless': 0.0, 'lot': 0.0, 'change': 0.0, 'decision': 0.0, 'crap': 0.0, 'dork': 0.0, 'censorship': 0.0, 'cubicle': 0.0, 'doom': 0.0, 'worthless': 0.12, 'previously': 0.12, 'gear': 0.12, 'ebay': 0.12, 'catch': 0.12, 'have': 0.12, 'fish': 0.12, 'thin': 0.12, 'ground': 0.12, 'dejected': 0.12, 'angry': 0.12, 'visit': 0.9, 'hospital': 0.9, 'disgusted': 0.9, 'experience': 0.9, 'offensive': 0.9, 'smell': 0.9, 'expect': 0.9, 'nearly': 0.9, 'run': 0.9, 'course': 0.8500000000000001, 'shape': 0.1, 'increasingly': 0.1, 'frustrated': 0.1, 'daily': 0.1, 'accumulation': 0.1, 'fat': 0.1, 'elusive': 0.1, 'fail': 0.0, 'entrance': 0.0, 'exam': 0.0, 'medical': 0.0, 'study': 0.0, 'biochemistry': 0.0, 'job': 0.0, 'prospect': 0.0, 'zambia': 0.0, 'wake': 0.1, 'morning': 0.1, 'agitated': 0.1, 'shake': 0.55, 'matter': 0.8, 'hard': 0.8, 'try': 0.8, 'conversation': 0.8, 'keep': 0.8, 'consume': 0.8, 'neglect': 0.3, 'soon': 0.0, 'choir': 0.0, 'deal': 0.05, 'headache': 0.0, 'killer': 0.0, 'evening': 0.0, 'subject': 0.6, 'unfair': 0.3, 'creature': 0.2, 'evaluate': 0.2, 'life': 0.2, 'intimate': 0.0, 'bodily': 0.0, 'relationship': 0.0, 'girlfriend': 0.0, 'avoid': 0.0, 'want': 0.1, 'sudden': 0.8, 'completely': 0.8, 'annoyed': 0.8, 'army': 0.0, 'ill': 0.0, 'local': 0.0, 'movie': 0.0, 'fact': 0.0, 'will': 0.475, 'meaning': 0.0, 'cause': 0.0, 'doubt': 0.0, 'actual': 0.0, 'intention': 0.0, 'actually': 0.0, 'moral': 0.0, 'brainless': 0.0, 'leave': 0.3, 'property': 0.0, 'minute': 0.0, 'later': 0.0, 'main': 0.0, 'street': 0.0, 'unsuspecting': 0.0, 'victim': 0.0, 'unknown': 0.0, 'enemy': 0.0, 'attack': 0.0, 'return': 0.0, 'envious': 0.2, 'win': 0.2, 'able': 0.0, 'recreate': 0.0, 'fog': 0.0, 'await': 0.0, 'home': 0.35, 'irritable': 0.7000000000000001, 'look': 0.2333333333333333, 'forward': 0.7, 'week': 0.7, 'vent': 0.1, 'ugly': 0.1, 'vicious': 0.1, 'nasty': 0.1, 'adult': 0.1, 'meet': 0.1, 'great': 0.1, 'unintentionally': 0.1, 'see': 0.7, 'man': 0.7, 'hit': 0.7, 'year': 0.7, 'consideration': 0.7, 'affect': 0.95, 'petty': 0.95, 'digust': 0.95, 'damn': 0.8, 'accept': 0.4, 'limitation': 0.4, 'hold': 0.4, 'resentful': 0.4, 'ridiculous': 0.5, 'possibly': 0.5, 'colourful': 0.5, 'turn': 0.5, 'phrase': 0.5, 'asleep': 0.5, 'tip': 0.5, 'tongue': 0.5, 'settle': 0.5, 'heave': 0.5, 'sigh': 0.5, 'term': 0.0, 'exboyfriend': 0.0, 'shout': 0.0, 'midnight': 0.0, 'interested': 0.0, 'boy': 0.0, 'remember': 0.0, 'cammie': 0.0, 'couple': 0.0, 'month': 0.0, 'sweet': 0.0, 'innocent': 0.0, 'sob': 0.0, 'unkind': 0.0, 'teacher': 0.0, 'mean': 0.0, 'knowingly': 0.4, 'wound': 0.4, 'seek': 0.4, 'good': 0.30000000000000004, 'feelin': 0.5, 'kind': 0.5, 'funky': 0.5, 'powerlessness': 0.75, 'control': 0.75, 'send': 0.75, 'mad': 0.75, 'tizzy': 0.75, 'haagen': 0.75, 'dazs': 0.75, 'hide': 0.2, 'true': 0.2, 'blurt': 0.2, 'tone': 0.2, 'necessary': 0.4, 'reach': 0.4, 'goal': 0.4, 'make': 0.9, 'antsy': 0.9, 'hill': 0.8, 'frustrate': 0.8, 'd': 0.8, 'pretty': 0.8, 'pace': 0.8, 'entirely': 0.8, 'factor': 0.8, 'hamper': 0.8, 'dent': 0.8, 'write': 0.2, 'appal': 0.2, 'blunt': 0.0, 'relation': 0.0, 'upset': 0.0, 'arrive': 0.0, 'response': 0.0, 'die': 0.0, 'past': 0.0, 'hair': 0.0, 'perfect': 0.0, 'weather': 0.0, 'anxiety': 0.0, 'bring': 0.0, 'tether': 0.0, 'sort': 0.3, 'eat': 0.0, 'rotten': 0.0, 'apple': 0.0}

def score_truth(str, dict_tokens):
    count_excla = 0
    count_maj = 0
    count_lettre = 0

    #parcourt le truth avant la tokenisation pour analyser la ponctuation et les majuscules/minuscules
    for c in str:
        if c == '!':
            count_excla +=1

        if type_de_caractere(c) == "majuscule":
            count_maj +=1 
            count_lettre +=1
        
        if type_de_caractere(c) == "minuscule":
            count_lettre +=1       

    #proportion de majuscules parmi les lettres
    prop_maj = count_maj/count_lettre

    #tokenisation
    tokens = (nettoyer_et_lemmatiser(str)).split()

    #score de colère du truth
    mean = 0

    tokens_comptabilises = 0

    for elt in tokens:
        if elt in dict_tokens:
            mean += dict_tokens[elt]
            tokens_comptabilises +=1
    
    mean += count_excla * (dict_tokens['!'])


    mean = mean/(count_excla + tokens_comptabilises)

    #prise en compte des majuscules: s'il y en a plus de 50%, on ajoute au score son reste pondéré par le pourcentage de majuscules
    if prop_maj>0.5:
        reste = 1 - mean
        mean += prop_maj*reste

    return mean

    




import pandas as pd

def ajouter_labels(fichier_entree, fichier_sortie, colonne_texte="Content"):
    # lecture échantillon
    df = pd.read_csv(fichier_entree)

    # étiquetage
    df["label"] = df[colonne_texte].astype(str).apply(score_truth)

    # sauvegarde
    df.to_csv(fichier_sortie, index=False)
    print(f"fichier sauvegardé sous : {fichier_sortie}")



entree = input("Chemin du fichier échantillon CSV : ").strip()
sortie = input("Nom du fichier de sortie : ").strip()
ajouter_labels(entree, sortie)

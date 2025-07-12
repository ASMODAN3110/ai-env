import nltk
import random
from nltk.corpus import wordnet, stopwords
from nltk import pos_tag, word_tokenize
from nltk.stem import WordNetLemmatizer

# Initialisation des ressources NLTK nécessaires
def initialize_nltk():
    """Vérifie si les ressources NLTK sont installées, sinon les télécharge."""
    resources = [
        ('wordnet', 'wordnet'),
        ('stopwords', 'stopwords'),
        ('punkt', 'punkt'),
        ('punkt_tab', 'punkt_tab'),
        ('averaged_perceptron_tagger', 'averaged_perceptron_tagger'),
        ('averaged_perceptron_tagger_eng', 'averaged_perceptron_tagger_eng')
    ]
    for resource, package in resources:
        try:
            path = (
                f'tokenizers/{resource}' if resource.startswith('punkt') else
                f'taggers/{resource}' if resource.startswith('averaged_perceptron_tagger') else
                f'corpora/{resource}'
            )
            nltk.data.find(path)
        except LookupError:
            print(f"Téléchargement de {package}...")
            nltk.download(package)

# Mappe les étiquettes POS de NLTK à WordNet
def get_wordnet_pos(treebank_tag):
    """
    Convertit les étiquettes POS de NLTK en étiquettes WordNet.

    Args:
        treebank_tag (str): Étiquette POS de NLTK (ex. 'NN', 'VB').

    Returns:
        str or None: Étiquette WordNet correspondante (ex. 'n', 'v') ou None.
    """
    return {
        'J': wordnet.ADJ,  # Adjectif
        'V': wordnet.VERB,  # Verbe
        'N': wordnet.NOUN,  # Nom
        'R': wordnet.ADV   # Adverbe
    }.get(treebank_tag[0], None)

# Trouve des synonymes en utilisant le premier synset
def find_synonyms(word, pos=None):
    """
    Trouve des synonymes pour un mot en utilisant le premier synset correspondant.

    Args:
        word (str): Le mot pour lequel chercher des synonymes.
        pos (str, optional): Type de mot WordNet (ex. 'n', 'v').

    Returns:
        list: Liste de synonymes uniques, sans le mot original.
    """
    lemmatizer = WordNetLemmatizer()
    lemma = lemmatizer.lemmatize(word.lower(), pos=pos) if pos else lemmatizer.lemmatize(word.lower())
    synonyms = set()
    synsets = wordnet.synsets(lemma, pos=pos)
    if not synsets:
        return []

    # Prend le premier synset correspondant au POS
    selected_synset = None
    for synset in synsets:
        if pos is None or synset.pos() == pos:
            selected_synset = synset
            break

    if selected_synset:
        print(f"Synset sélectionné pour '{word}' ({pos}): {selected_synset.name()}")  # Debug
        for lemma in selected_synset.lemmas():
            synonym = lemma.name().replace('_', ' ')
            if synonym.lower() != word.lower():
                synonyms.add(synonym)
        print(f"Synonymes pour '{word}' ({pos}): {synonyms}")  # Debug

    return list(synonyms)

# Remplace des mots par des synonymes
def replace_words_with_synonyms(sentence, max_replacements=1):
    """
    Remplace certains mots dans une phrase par leurs synonymes.

    Args:
        sentence (str): La phrase à modifier.
        max_replacements (int): Nombre maximum de mots à remplacer.

    Returns:
        str: La phrase avec certains mots remplacés.
    """
    words = word_tokenize(sentence)
    if not words:
        return sentence

    tagged_words = pos_tag(words)
    stop_words = set(stopwords.words('english'))

    candidates = []
    for index, (word, tag) in enumerate(tagged_words):
        if word.lower() in stop_words or not word.isalpha():
            continue
        wordnet_pos = get_wordnet_pos(tag)
        if not wordnet_pos:
            continue
        synonyms = find_synonyms(word, pos=wordnet_pos)
        if synonyms:
            candidates.append((index, word, synonyms, tag))

    if not candidates:
        return sentence

    num_replacements = min(max_replacements, len(candidates))
    replacements = random.sample(candidates, num_replacements)

    new_words = words.copy()
    for index, original, synonyms, tag in replacements:
        synonym = random.choice(synonyms)
        if original.istitle():
            synonym = synonym.title()
        new_words[index] = synonym
        print(f"Remplacé '{original}' par '{synonym}'")  # Debug

    return ' '.join(new_words)

if __name__ == "__main__":
    initialize_nltk()
    print("Synonymes de 'sad':", find_synonyms("sad", wordnet.ADJ))
    print("Synonymes de 'dog':", find_synonyms("dog", wordnet.NOUN))
    print("Synonymes de 'run':", find_synonyms("run", wordnet.VERB))
    sentence = "The sad dog ran quickly."
    print("\nPhrase originale:", sentence)
    for i in range(3):
        new_sentence = replace_words_with_synonyms(sentence, max_replacements=1)  # Set to 1 for clarity
        print(f"Essai {i + 1}: {new_sentence}")

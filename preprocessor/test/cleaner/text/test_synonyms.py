import unittest
from unittest.mock import patch
from utilities.synonyms import initialize_nltk, get_wordnet_pos, find_synonyms, replace_words_with_synonyms

class TestSynonymReplacer(unittest.TestCase):
    """Classe pour tester les fonctions de remplacement de synonymes."""

    @classmethod
    def setUpClass(cls):
        """Initialise les ressources NLTK avant tous les tests."""
        initialize_nltk()

    def test_initialize_nltk(self):
        """Teste si initialize_nltk charge correctement les ressources NLTK."""
        with patch('nltk.download') as mock_download:
            # Simule que WordNet n'est pas installé
            mock_download.side_effect = lambda x: None
            initialize_nltk()
            self.assertTrue(mock_download.called, "nltk.download devrait être appelé si les ressources manquent")

    def test_get_wordnet_pos(self):
        """Teste la conversion des étiquettes POS de NLTK en étiquettes WordNet."""
        # Teste les cas pour chaque type de mot
        self.assertEqual(get_wordnet_pos('JJ'), 'a', "L'adjectif devrait retourner 'a'")
        self.assertEqual(get_wordnet_pos('VB'), 'v', "Le verbe devrait retourner 'v'")
        self.assertEqual(get_wordnet_pos('NN'), 'n', "Le nom devrait retourner 'n'")
        self.assertEqual(get_wordnet_pos('RB'), 'r', "L'adverbe devrait retourner 'r'")
        self.assertIsNone(get_wordnet_pos('DT'), "Un déterminant devrait retourner None")

    def test_find_synonyms(self):
        """Teste la recherche de synonymes pour un mot donné."""
        # Teste un mot avec des synonymes
        synonyms = find_synonyms("happy")
        self.assertIn("glad", synonyms, "'glad' devrait être un synonyme de 'happy'")
        self.assertNotIn("happy", synonyms, "Le mot original ne devrait pas être dans les synonymes")
        self.assertNotIn("Happy", synonyms, "Le mot original (en majuscule) ne devrait pas être dans les synonymes")

        # Teste un mot sans synonymes
        synonyms = find_synonyms("xyz")
        self.assertEqual(synonyms, [], "Un mot inexistant devrait retourner une liste vide")

        # Teste avec un type de mot spécifique
        synonyms = find_synonyms("run", pos='v')
        self.assertIn("sprint", synonyms, "'sprint' devrait être un synonyme de 'run' (verbe)")
        self.assertNotIn("test", synonyms, "Les synonymes doivent correspondre au type de mot")

    def test_replace_words_with_synonyms(self):
        """Teste le remplacement de mots par des synonymes dans une phrase."""
        # Teste une phrase normale
        sentence = "The big dog runs fast."
        new_sentence = replace_words_with_synonyms(sentence, max_replacements=1)
        self.assertNotEqual(new_sentence, sentence, "La phrase devrait être modifiée")
        self.assertEqual(len(new_sentence.split()), 5, "La phrase devrait conserver le même nombre de mots")

        # Teste une phrase sans mots remplaçables (que des stop words)
        sentence = "The is and or"
        new_sentence = replace_words_with_synonyms(sentence, max_replacements=1)
        self.assertEqual(new_sentence, sentence, "Une phrase sans mots remplaçables ne devrait pas changer")

        # Teste une phrase vide
        new_sentence = replace_words_with_synonyms("", max_replacements=1)
        self.assertEqual(new_sentence, "", "Une phrase vide devrait retourner une phrase vide")

        # Teste avec un nombre de remplacements supérieur aux mots disponibles
        sentence = "Happy dog"
        new_sentence = replace_words_with_synonyms(sentence, max_replacements=5)
        self.assertTrue(len(new_sentence.split()) == 2, "Le nombre de mots ne devrait pas changer")

if __name__ == '__main__':
    unittest.main()

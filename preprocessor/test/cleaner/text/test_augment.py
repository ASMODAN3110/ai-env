import unittest
import pandas as pd
from utilities.synonyms import replace_words_with_synonyms
from cleaner_text.augment import augment_dataframe  # adjust this import path to your actual module

class TestDataAugmentation(unittest.TestCase):

    def setUp(self):
        # Minimal DataFrame to test augmentation
        self.df = pd.DataFrame({
            "text": [
                "The quick brown fox jumps over the lazy dog",
                "Artificial intelligence is transforming the world"
            ],
            "label": ["neutral", "positive"]
        })

    def test_replace_words_with_synonyms(self):
        text = "The quick brown fox"
        new_text = replace_words_with_synonyms(text, n_replacements=2)
        self.assertIsInstance(new_text, str)
        self.assertNotEqual(text, new_text, "Text should be changed if synonyms exist")

    def test_augmentation_rate(self):
        aug_df = augment_dataframe(self.df, text_column="text", augmentation_rate=2.0)
        self.assertEqual(len(aug_df), len(self.df) * 2, "Augmented dataframe should double in size")

    def test_augmentation_partial(self):
        aug_df = augment_dataframe(self.df, text_column="text", augmentation_rate=1.5)
        expected = int(len(self.df) * 1.5)
        self.assertEqual(len(aug_df), expected, "Augmented dataframe should match expected size")

    def test_no_change_when_rate_is_one(self): #TODO
        aug_df = augment_dataframe(self.df, text_column="text", augmentation_rate=1.0)
        self.assertEqual(len(aug_df), len(self.df), "With rate 1.0, output size must equal input size")

    def test_raises_on_invalid_rate(self):
        with self.assertRaises(ValueError):
            augment_dataframe(self.df, text_column="text", augmentation_rate=0.5)

    def test_augmented_texts_are_different(self):
        aug_df = augment_dataframe(self.df, text_column="text", augmentation_rate=2.0)
        original_texts = set(self.df["text"])
        augmented_texts = set(aug_df["text"])
        self.assertGreater(len(augmented_texts - original_texts), 0, "Some texts must be augmented")


if __name__ == "__main__":
    unittest.main()

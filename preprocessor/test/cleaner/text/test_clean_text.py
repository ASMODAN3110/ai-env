import os
import unittest
import tempfile

from cleaner_text.loader import load_text_data
from cleaner_text.cleaner import clean_text_data

class TestTextCleaning(unittest.TestCase):

    def setUp(self):
        self.temp_files = []

    def tearDown(self):
        for f in self.temp_files:
            if os.path.exists(f):
                os.remove(f)

    def create_temp_file(self, content, suffix):
        fd, path = tempfile.mkstemp(suffix=suffix)
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(content)
        self.temp_files.append(path)
        return path

    def test_clean_csv_data(self):
        raw = (
            "text,label\n"
            "  Hello   😊  ,positive\n"
            "   <b>bad</b> &amp; ugly   ,negative\n"
            "   ,missing\n"
            "Hello   😊  ,positive\n"  # duplicate
        )
        path = self.create_temp_file(raw, ".csv")
        df_loaded = load_text_data(path)
        df_cleaned = clean_text_data(df_loaded)

        # Check number of rows (null + duplicate removed)
        self.assertEqual(len(df_cleaned), 2)

        # Check column presence
        self.assertIn("text", df_cleaned.columns)

        # Check for cleaned content
        cleaned_texts = df_cleaned["text"].tolist()
        for txt in cleaned_texts:
            self.assertNotIn("😊", txt)
            self.assertNotIn("<", txt)
            self.assertNotIn("&", txt)
            self.assertFalse(any(c in txt for c in ['$', '@', '#', '©']))  # strange chars
            self.assertFalse("  " in txt)
            self.assertTrue(txt == txt.lower())

    def test_clean_jsonl_data(self):
        content = (
            '{"text": "   I ❤️ AI  ", "label": "positive"}\n'
            '{"text": "<script>alert(1)</script>", "label": "toxic"}\n'
            '{"text": "", "label": "neutral"}\n'
        )
        path = self.create_temp_file(content, ".jsonl")
        df_loaded = load_text_data(path)
        df_cleaned = clean_text_data(df_loaded)

        self.assertEqual(len(df_cleaned), 2)  # last row is empty and removed

        for txt in df_cleaned["text"]:
            self.assertNotIn("❤️", txt)
            self.assertNotIn("<script>", txt)
            self.assertNotEqual(txt.strip(), "")
            self.assertTrue(txt == txt.lower())


if __name__ == "__main__":
    unittest.main()

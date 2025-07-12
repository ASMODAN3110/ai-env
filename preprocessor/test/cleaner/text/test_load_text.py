import os
import json
import pickle
import unittest
import tempfile
import pandas as pd

from cleaner_text.loader import load_text_data  # <-- adjust import based on your file location


class TestLoadTextData(unittest.TestCase):

    def setUp(self):
        self.temp_files = []

    def tearDown(self):
        for file in self.temp_files:
            try:
                os.remove(file)
            except Exception as e:
                print(e)
                pass

    def create_temp_file(self, content, suffix, mode='w', binary=False):
        fd, path = tempfile.mkstemp(suffix=suffix)
        with os.fdopen(fd, mode + ('b' if binary else '')) as f:
            if binary:
                f.write(content)
            else:
                f.write(content)
        self.temp_files.append(path)
        return path

    def test_csv(self):
        content = "text,label\nHello,positive\nBad,negative\n"
        path = self.create_temp_file(content, ".csv")
        df = load_text_data(path)
        self.assertEqual(len(df), 2)
        self.assertIn("text", df.columns)

    def test_tsv(self):
        content = "text\tlabel\nYes\t1\nNo\t0\n"
        path = self.create_temp_file(content, ".tsv")
        df = load_text_data(path)
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[0]["label"], 1)

    def test_jsonl(self):
        content = '{"text": "Hello", "label": "positive"}\n{"text": "Bad", "label": "negative"}\n'
        path = self.create_temp_file(content, ".jsonl")
        df = load_text_data(path)
        self.assertEqual(df.shape[0], 2)
        self.assertIn("label", df.columns)

    def test_json_array(self):
        content = json.dumps([
            {"text": "Hello", "label": "positive"},
            {"text": "Bad", "label": "negative"}
        ])
        path = self.create_temp_file(content, ".json")
        df = load_text_data(path)
        self.assertEqual(df.iloc[1]["text"], "Bad")

    def test_json_dict(self):
        content = json.dumps({
            "col1": ["a", "b"],
            "col2": [1, 2]
        })
        path = self.create_temp_file(content, ".json")
        df = load_text_data(path)
        self.assertIn("col1", df.columns)
        self.assertEqual(df.shape, (2, 2))

    def test_txt(self):
        content = "line one\nline two\nline three\n"
        path = self.create_temp_file(content, ".txt")
        df = load_text_data(path)
        self.assertEqual(len(df), 3)
        self.assertIn("text", df.columns)

    def test_parquet(self):
        df_original = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
        with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False) as tmp:
            tmp.close()  # close to allow pandas to write to it
            self.temp_files.append(tmp.name)
            df_original.to_parquet(tmp.name)
            df = load_text_data(tmp.name)
            self.assertTrue(df.equals(df_original))

    def test_pickle(self):
        df_original = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
        pickled = pickle.dumps(df_original)
        path = self.create_temp_file(pickled, ".pkl", mode='w', binary=True)
        df = load_text_data(path)
        self.assertTrue(df.equals(df_original))

    def test_invalid_extension(self):
        path = self.create_temp_file("test data", ".xyz")
        with self.assertRaises(RuntimeError):
            load_text_data(path)

    def test_malformed_json(self):
        path = self.create_temp_file("{invalid json]", ".json")
        with self.assertRaises(RuntimeError):
            load_text_data(path)


if __name__ == '__main__':
    unittest.main()

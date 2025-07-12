import pandas as pd
from utilities.synonyms import replace_words_with_synonyms

def augment_dataframe(df, text_column='text', augmentation_rate=2.0):
    """
    Augment a DataFrame by synonym replacement to increase dataset size by augmentation_rate.

    Params:
        df (pd.DataFrame): Original DataFrame
        text_column (str): Column name with text data
        augmentation_rate (float): Target multiplier of dataset size (e.g., 2.0 means double size)

    Returns:
        pd.DataFrame: Augmented DataFrame containing original + synthetic samples
    """
    if augmentation_rate < 1.0:
        raise ValueError("augmentation_rate must be >= 1.0")

    original_count = len(df)
    target_count = int(original_count * augmentation_rate)

    augmented_rows = []
    n_new_samples = target_count - original_count
    samples_per_row = max(1, n_new_samples // original_count)

    for _, row in df.iterrows():
        text = row[text_column]
        for _ in range(samples_per_row):
            # Decide number of replacements: 1 or 2 or more based on sentence length
            n_replace = max(1, len(text.split()) // 10)
            new_text = replace_words_with_synonyms(text, n_replace)
            if new_text != text:
                new_row = row.copy()
                new_row[text_column] = new_text
                augmented_rows.append(new_row)
            if len(augmented_rows) >= n_new_samples:
                break
        if len(augmented_rows) >= n_new_samples:
            break

    augmented_df = pd.concat([df, pd.DataFrame(augmented_rows)], ignore_index=True)
    return augmented_df

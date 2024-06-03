import torch
from torch.utils.data import DataLoader, Dataset
from transformers import BertTokenizer
from sklearn.model_selection import train_test_split
import pandas as pd




class LanguageDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )
        return {
            'text': text,
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }
def load_dataset(filepath):
    # Load the dataset into a pandas DataFrame
    df = pd.read_csv(filepath)
    return df

class LanguageModelDataset(Dataset):
    def __init__(self):
        self.df = load_dataset('./data/data_lang.csv')
        # Ensure that the dataset was loaded correctly
        if self.df is None or 'language' not in self.df.columns or 'text' not in self.df.columns:
            raise ValueError("The dataset could not be loaded or is missing 'text' and 'language' columns.")
        # Encode language labels to integers
        self.language_to_id = {language: idx for idx, language in enumerate(self.df.language.unique())}
        self.id_to_language = {idx: language for language, idx in self.language_to_id.items()}
        self.df['language_id'] = self.df['language'].map(self.language_to_id)
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
        self.MAX_LEN = 128
        self.BATCH_SIZE = 16
        self.EPOCHS = 6
        self.N_CLASSES = self.df.language.nunique()

        self.train_texts, self.val_texts, self.train_labels, self.val_labels = train_test_split(
            self.df.text.values,
            self.df.language_id.values,
            test_size=0.1,
            random_state=42
        )

        self.train_dataset = LanguageDataset(
            texts=self.train_texts,
            labels=self.train_labels,
            tokenizer=self.tokenizer,
            max_len=self.MAX_LEN
        )
        self.val_dataset = LanguageDataset(
            texts=self.val_texts,
            labels=self.val_labels,
            tokenizer=self.tokenizer,
            max_len=self.MAX_LEN
        )

        self.train_data_loader = DataLoader(
            self.train_dataset,
            batch_size=self.BATCH_SIZE,
            shuffle=True
        )
        self.val_data_loader = DataLoader(
            self.val_dataset,
            batch_size=self.BATCH_SIZE,
            shuffle=False
        )













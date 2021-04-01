from typing import List

from transformers import DistilBertTokenizer, DistilBertPreTrainedModel, DistilBertModel, DistilBertConfig
import torch
import torch.nn as nn
import numpy as np


with open("models/themes_list.txt") as f:
    THEMES_LIST = f.read().split(",")


class DistilBertForThemesClassification(DistilBertPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.num_labels = config.num_labels

        self.distilbert = DistilBertModel(config)
        self.dropout = nn.Dropout(config.dropout)
        self.classifier = nn.Linear(config.hidden_size, len(THEMES_LIST))

        self.init_weights()

    def forward(self,
        input_ids=None,
        attention_mask=None):
    
        outputs = self.distilbert(
            input_ids,
            attention_mask=attention_mask)

        sequence_output = outputs[0][:, 0, :]  # Only first token

        sequence_output = self.dropout(sequence_output)
        return self.classifier(sequence_output)


class ThemeRecommander:
    def __init__(self, model_path: str, tokenizer_path: str):
        self.tokenizer = DistilBertTokenizer.from_pretrained(tokenizer_path)
        self.model = DistilBertForThemesClassification.from_pretrained(model_path)
        self.config = DistilBertConfig.from_pretrained(tokenizer_path)
        self.themes_list = np.array(THEMES_LIST)

    def get_themes(self, sentence: str, ntop=20) -> List:
        sentence_encoded = self.tokenizer(sentence, return_tensors='pt', padding='max_length',
                             max_length=self.config.max_position_embeddings,
                             truncation=True)
        preds = torch.sigmoid(self.model(**sentence_encoded)).reshape(-1)
        return self.themes_list[preds.argsort(descending=True)][:ntop].tolist()


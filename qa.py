# Imports
import numpy as np
import torch
from transformers import LongformerTokenizer, LongformerForMultipleChoice

class QuestionAnsweringModel:
    def __init__(self):
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        self.tokenizer = LongformerTokenizer.from_pretrained('allenai/longformer-base-4096')
        self.model = LongformerForMultipleChoice.from_pretrained('valhalla/longformer-base-4096-finetuned-squadv1')
        # print(self.model)
        self.model.to(self.device)

    def _encode_sample(self, text, choices):
        encodings = self.tokenizer([text] * len(choices), choices, return_tensors = 'pt', padding = True)
        encodings = {k : v.to(self.device) for k, v in encodings.items()}
        return encodings

    def get_answer(self, text, choices):
        # print(choices)
        encodings = self._encode_sample(text, choices)
        with torch.no_grad():
            outputs = self.model(**{k : v.unsqueeze(0) for k, v in encodings.items()})
            logits = outputs.logits
            ans = torch.argmax(logits)
            logits = outputs.logits.detach().cpu().numpy()
            ans = np.argmax(logits)
        return ans
from pymilvus import model
from ai_utils import getConfig
#import torch
# 获取类型
#device = "cuda:0" if torch.cuda.is_available() else "cpu"
#print(device)
sentence_transformer_ef = model.dense.SentenceTransformerEmbeddingFunction(
    model_name='./models/mf-all-MiniLM-L6-v2',
    device=getConfig('torch.device')
)

def encode_queries(questions):
   return sentence_transformer_ef.encode_queries(questions)

def encode_documents(documents):
   return sentence_transformer_ef.encode_documents(documents)
    

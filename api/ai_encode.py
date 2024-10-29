from pymilvus import model
import subprocess
try:
    subprocess.check_output(["nvidia-smi"])
    device = "cuda:0"
except (subprocess.CalledProcessError, FileNotFoundError):
    device = "cpu"

print('device', device)

sentence_transformer_ef = model.dense.SentenceTransformerEmbeddingFunction(
    model_name='./models/mf-all-MiniLM-L6-v2',
    device=device
)

def encode_queries(questions):
   return sentence_transformer_ef.encode_queries(questions)

def encode_documents(documents):
   return sentence_transformer_ef.encode_documents(documents)
    

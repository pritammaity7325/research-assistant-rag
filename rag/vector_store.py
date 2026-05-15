import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from config.settings import EMBEDDING_MODEL

embedder = SentenceTransformer(EMBEDDING_MODEL)

class VectorStore:
    def __init__(self):
        self.index = None
        self.texts = []

    def build(self, chunks):
        embeddings = embedder.encode(chunks)
        self.texts = chunks
        dim = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings))

    def query(self, question, top_k=5):
        q_embedding = embedder.encode([question])
        distances, indices = self.index.search(np.array(q_embedding), top_k)

        return [self.texts[i] for i in indices[0]]

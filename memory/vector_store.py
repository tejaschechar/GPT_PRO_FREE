import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# 🔥 Force CPU usage (important for stability)
model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    device="cpu"
)

INDEX_PATH = "data/faiss_index/index.faiss"
META_PATH = "data/faiss_index/meta.pkl"


class VectorStore:
    def __init__(self):
        self.dimension = model.get_sentence_embedding_dimension()

        # cosine similarity using inner product
        self.index = faiss.IndexFlatIP(self.dimension)

        self.texts = []

        if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
            self.load()

    def _embed(self, text: str):
        vec = model.encode(
            text,
            normalize_embeddings=True,
            show_progress_bar=False
        )
        return np.array([vec]).astype("float32")

    def add(self, text: str):
        embedding = self._embed(text)
        self.index.add(embedding)
        self.texts.append(text)

    def add_batch(self, texts):
        embeddings = model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False
        )
        embeddings = np.array(embeddings).astype("float32")

        self.index.add(embeddings)
        self.texts.extend(texts)

    def search(self, query: str, k=3):
        if self.index.ntotal == 0:
            return []

        query_vec = self._embed(query)

        scores, indices = self.index.search(query_vec, k)

        results = []
        for idx in indices[0]:
            if 0 <= idx < len(self.texts):
                results.append(self.texts[idx])

        return results

    def save(self):
        os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)

        faiss.write_index(self.index, INDEX_PATH)

        with open(META_PATH, "wb") as f:
            pickle.dump(self.texts, f)

    def load(self):
        self.index = faiss.read_index(INDEX_PATH)

        with open(META_PATH, "rb") as f:
            self.texts = pickle.load(f)
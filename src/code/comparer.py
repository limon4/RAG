from sentence_transformers import SentenceTransformer
import torch

# Load model
model = SentenceTransformer('Santp98/SBERT-pairs-bert-base-spanish-wwm-cased')

# Define two example sentences
sentence1 = ("se considera centro de trabajo la unidad productiva con organización específica, que sea dada de alta, "
             "como tal, ante la autoridad laboral.")
sentence2 = ("Un centro de trabajo es un lugar donde se desarrollan actividades laborales y productivas, normalmente "
             "administrado por una empresa.")

# Encode sentences and compute similarity score
embeddings1 = model.encode([sentence1], convert_to_tensor=True)
embeddings2 = model.encode([sentence2], convert_to_tensor=True)
cosine_similarities = torch.nn.functional.cosine_similarity(embeddings1, embeddings2)

# Print similarity score
print(f"Similarity score: {cosine_similarities.item()}")
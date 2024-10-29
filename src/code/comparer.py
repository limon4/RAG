from sentence_transformers import SentenceTransformer
import torch

# Load model
model = SentenceTransformer('Santp98/SBERT-pairs-bert-base-spanish-wwm-cased')

# Define two example sentences
sentence1 = ("Esta ley será de aplicación a los trabajadores que voluntariamente presten sus servicios retribuidos por "
             "cuenta ajena y dentro del ámbito de organización y dirección de otra persona, física o jurídica")
sentence2 = "El Estatuto de los Trabajadores se aplica a todas las personas que están relacionadas con la actividad productiva, sea como empleados, trabajadores independientes o dependientes directos."

# Encode sentences and compute similarity score
embeddings1 = model.encode([sentence1], convert_to_tensor=True)
embeddings2 = model.encode([sentence2], convert_to_tensor=True)
cosine_similarities = torch.nn.functional.cosine_similarity(embeddings1, embeddings2)

# Print similarity score
print(f"Similarity score: {cosine_similarities.item()}")
# RAG implementation using Llama models and Hugging Face Embeddings

## Testing few models

### ¿A quién se le aplica el Estatuto de los Trabajadores (en adelante ET)?

| LLM model | Embedding model | RAG answer | Score (cosine similarity) |
| --------- | --------------- | ---------- | ------------------------- |
| mistral | RoBERTalex | El Estatuto de los Trabajadores se aplica a todas las personas que están relacionadas con la actividad productiva, sea como empleados, trabajadores independientes o dependientes directos. | 0.62 |

### ¿Qué se considera un empresario en la legislación laboral?
| LLM model | Embedding model | RAG answer | Score (cosine similarity) |
| --------- | --------------- | ---------- | ------------------------- |
| mistral | RoBERTalex | Un empresario, según la legislación laboral, es una persona que tiene o gestiona una actividad económica o empresa propia. Es decir, el dueño de una empresa u organización comercial que pone en juego su capital y se responsabiliza por sus decisiones y riesgos. | 0.65 |

### ¿Qué relaciones laborales se excluyen de la aplicación del Estatuto de los Trabajadores?
| LLM model | Embedding model | RAG answer | Score (cosine similarity) |
| --------- | --------------- | ---------- | ------------------------- |
| mistral | RoBERTalex |

### Si tengo una empresa española, ¿Se aplican los derechos económicos de la legislación española laboral a los trabajadores españoles contratados en España?
| LLM model | Embedding model | RAG answer | Score (cosine similarity) |
| --------- | --------------- | ---------- | ------------------------- |
| mistral | RoBERTalex |

### ¿Qué es un centro de trabajo?
| LLM model | Embedding model | RAG answer | Score (cosine similarity) |
| --------- | --------------- | ---------- | ------------------------- |
| mistral | RoBERTalex |

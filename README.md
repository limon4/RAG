# RAG implementation using Llama models and Hugging Face Embeddings

## Testing few models

### ¿A quién se le aplica el Estatuto de los Trabajadores (en adelante ET)?

| LLM model | Embedding model | RAG answer | ST model | Score (cosine similarity) |
| --------- | --------------- | ---------- | -------- | ------------------------- |
| mistral | RoBERTalex | El Estatuto de los Trabajadores se aplica a todas las personas que están relacionadas con la actividad productiva, sea como empleados, trabajadores independientes o dependientes directos. | SBERT-pairs-bert-base-spanish-wwm-cased | 0.62 |

### ¿Qué se considera un empresario en la legislación laboral?
| LLM model | Embedding model | RAG answer | ST model | Score (cosine similarity) |
| --------- | --------------- | ---------- | -------- | ------------------------- |
| mistral | RoBERTalex | Un empresario, según la legislación laboral, es una persona que tiene o gestiona una actividad económica o empresa propia. Es decir, el dueño de una empresa u organización comercial que pone en juego su capital y se responsabiliza por sus decisiones y riesgos. | SBERT-pairs-bert-base-spanish-wwm-cased | 0.65 |

### ¿Qué relaciones laborales se excluyen de la aplicación del Estatuto de los Trabajadores?
| LLM model | Embedding model | RAG answer | ST model | Score (cosine similarity) |
| --------- | --------------- | ---------- | -------- | ------------------------- |
| mistral | RoBERTalex | 1. Familiares que residen en el hogar y colaboran en las tareas domésticas sin relación laboral formal. 2. Miembros del personal de la Administración Pública Nacional (APN) y los trabajadores de Empresa Pública, cuyos régimenes se rigen por disposiciones específicas. 3. Empleados domésticos que trabajan en la casa propia de sus patrones y no son contratados por una agencia temporal. 4. Alguien que trabaje como artista independiente y no cumpla con las características legales para considerarse como empleado. 5. El personal militar, naval o aeronáutico de carrera regular del Ejército, Armada o Fuerza Aérea Española. 6. El personal que ejerce una profesión liberal, con independencia de la forma en que desempeñe su actividad laboral: autónomo, empleado o colaborador. 7. El personal de las Fuerzas y Cuerpos de Seguridad del Estado (Policía Nacional, Guardia Civil, etc.). 8. Los trabajadores de entidades religiosas que no sean entidades de derecho público. 9. El personal de la Administración Local y Autonómica. Nota: Esta lista es un ejemplo generico y puede variar segun el contexto geográfico especifico en el que estemos. | SBERT-pairs-bert-base-spanish-wwm-cased | 0.63 |

### Si tengo una empresa española, ¿Se aplican los derechos económicos de la legislación española laboral a los trabajadores españoles contratados en España?
| LLM model | Embedding model | RAG answer | ST model | Score (cosine similarity) |
| --------- | --------------- | ---------- | -------- | ------------------------- |
| mistral | RoBERTalex | Sí, los derechos económicos de la legislación española laboral se aplican a los trabajadores españoles contratados en España. | SBERT-pairs-bert-base-spanish-wwm-cased | 0.81 |

### ¿Qué es un centro de trabajo?
| LLM model | Embedding model | RAG answer | ST model | Score (cosine similarity) |
| --------- | --------------- | ---------- | -------- | ------------------------- |
| mistral | RoBERTalex | Un centro de trabajo es una instalación física diseñada para alojar a personas que realizan tareas laborales, ofreciendo servicios y recursos necesarios para llevar a cabo dichas actividades. | SBERT-pairs-bert-base-spanish-wwm-cased | 0.70 |

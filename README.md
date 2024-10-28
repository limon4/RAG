# RAG implementation using Llama models and Hugging Face Embeddings

## Testing few models

### ¿A quién se le aplica el Estatuto de los Trabajadores (en adelante ET)?

| LLM model | Embedding model | RAG answer | ST model | Score (cosine similarity) |
| --------- | --------------- | ---------- | -------- | ------------------------- |
| mistral | FastEmbedEmbeddings | El Estatuto de los Trabajadores se aplica a los trabajadores. | SBERT-pairs-bert-base-spanish-wwm-cased | 0.62 |
| mistral | RoBERTalex | El Estatuto de los Trabajadores se aplica a todas las personas que están relacionadas con la actividad productiva, sea como empleados, trabajadores independientes o dependientes directos. | SBERT-pairs-bert-base-spanish-wwm-cased | 0.62 |

### ¿Qué se considera un empresario en la legislación laboral?
| LLM model | Embedding model | RAG answer | ST model | Score (cosine similarity) |
| --------- | --------------- | ---------- | -------- | ------------------------- |
| mistral | FastEmbedEmbeddings | Un empresario en la legislación laboral es aquella persona o entidad que ejerce dirección y mando sobre los trabajadores, y puede iniciar procedimientos en el ámbito laboral, como la suspensión de contratos o reducción temporal de jornada. | SBERT-pairs-bert-base-spanish-wwm-cased | 0.65 |
| mistral | RoBERTalex | Un empresario, según la legislación laboral, es una persona que tiene o gestiona una actividad económica o empresa propia. Es decir, el dueño de una empresa u organización comercial que pone en juego su capital y se responsabiliza por sus decisiones y riesgos. | SBERT-pairs-bert-base-spanish-wwm-cased | 0.65 |

### ¿Qué relaciones laborales se excluyen de la aplicación del Estatuto de los Trabajadores?
| LLM model | Embedding model | RAG answer | ST model | Score (cosine similarity) |
| --------- | --------------- | ---------- | -------- | ------------------------- |
| mistral | FastEmbedEmbeddings | Las relaciones laborales de carácter especial excluidas del Estatuto de los Trabajadores son: a) La del personal de alta dirección no incluido en el artículo 1.3.c). b) La del servicio del hogar familiar. c) La de los penados en las instituciones penitenciarias. d) La de los deportistas profesionales. e) La de las personas artistas que desarrollan su actividad en las artes escénicas, audiovisuales y musicales, así como las personas que realizan actividades técnicas o auxiliares necesarias para el desarrollo de dicha actividad. f) La de las personas que intervengan en operaciones mercantiles por cuenta de uno o. | SBERT-pairs-bert-base-spanish-wwm-cased | 0.63 |
| mistral | RoBERTalex | 1. Familiares que residen en el hogar y colaboran en las tareas domésticas sin relación laboral formal. 2. Miembros del personal de la Administración Pública Nacional (APN) y los trabajadores de Empresa Pública, cuyos régimenes se rigen por disposiciones específicas. 3. Empleados domésticos que trabajan en la casa propia de sus patrones y no son contratados por una agencia temporal. 4. Alguien que trabaje como artista independiente y no cumpla con las características legales para considerarse como empleado. 5. El personal militar, naval o aeronáutico de carrera regular del Ejército, Armada o Fuerza Aérea Española. 6. El personal que ejerce una profesión liberal, con independencia de la forma en que desempeñe su actividad laboral: autónomo, empleado o colaborador. 7. El personal de las Fuerzas y Cuerpos de Seguridad del Estado (Policía Nacional, Guardia Civil, etc.). 8. Los trabajadores de entidades religiosas que no sean entidades de derecho público. 9. El personal de la Administración Local y Autonómica. Nota: Esta lista es un ejemplo generico y puede variar segun el contexto geográfico especifico en el que estemos. | SBERT-pairs-bert-base-spanish-wwm-cased | 0.63 |

### Si tengo una empresa española, ¿Se aplican los derechos económicos de la legislación española laboral a los trabajadores españoles contratados en España?
| LLM model | Embedding model | RAG answer | ST model | Score (cosine similarity) |
| --------- | --------------- | ---------- | -------- | ------------------------- |
| mistral | FastEmbedEmbeddings | Los trabajadores españoles contratados en España tienen derecho a los beneficios establecidos por la legislación laboral española. La relación laboral puede extenderse durante cierto tiempo si se ha acordado que el trabajador haya recibido una especialización profesional con cargo al empresario para poner en marcha proyectos determinados o realizar un trabajo específico, y este acuerdo no debe durar más de dos años. Si un trabajador abandona el trabajo antes del plazo establecido, el empresario tiene derecho a una indemnización de daños y perjuicios. En caso de cesión ilegal, el trabajador tendrá derecho a convertirse en fijo en la empresa cedente o cesionaria. Además, cualquiera de las partes puede exigir que el contrato se formalice por escrito. | SBERT-pairs-bert-base-spanish-wwm-cased | 0.81 |
| mistral | RoBERTalex | Sí, los derechos económicos de la legislación española laboral se aplican a los trabajadores españoles contratados en España. | SBERT-pairs-bert-base-spanish-wwm-cased | 0.81 |

### ¿Qué es un centro de trabajo?
| LLM model | Embedding model | RAG answer | ST model | Score (cosine similarity) |
| --------- | --------------- | ---------- | -------- | ------------------------- |
| mistral | FastEmbedEmbeddings | Un centro de trabajo es una unidad productiva con organización específica, que se da de alta ante la autoridad laboral. Este concepto incluye territorios españoles, centros afectados por ciertos procedimientos y buques en su puerto de base. En el marco de las relaciones laborales de carácter especial, los centros de trabajo también se refieren al servicio del hogar familiar, a la dirección alta no incluida en otros artículos y a ciertas actividades en las artes escénicas, audiovisuales y musicales. | SBERT-pairs-bert-base-spanish-wwm-cased | 0.70 |
| mistral | RoBERTalex | Un centro de trabajo es una instalación física diseñada para alojar a personas que realizan tareas laborales, ofreciendo servicios y recursos necesarios para llevar a cabo dichas actividades. | SBERT-pairs-bert-base-spanish-wwm-cased | 0.70 |

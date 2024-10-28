# RAG implementation using Llama models and Hugging Face Embeddings

## Testing few models

### ¿A quién se le aplica el Estatuto de los Trabajadores (en adelante ET)?

| LLM model | Embedding model | RAG answer | ST model | Score (cosine similarity) |
| --------- | --------------- | ---------- | -------- | ------------------------- |
| mistral | FastEmbedEmbeddings | 1. Los sindicatos que tengan la consideración de más representativos a nivel estatal, así como, en sus respectivos ámbitos, las organizaciones sindicales afiliadas, federadas o confederadas a los mismos (ET artículo 39). 2. En empresas que ocupen más de trescientos trabajadores, cualquier trabajo puede considerarse colectivo si llega al umbral de treinta trabajadores (ET Página 42). 3. Cualquier trabajador tiene derecho a la extinción del contrato por justas causas tales como modificaciones sustanciales en las condiciones de trabajo llevadas a cabo sin respetar lo previsto en el artículo 41 y que redunden en menoscabo de la dignidad del trabajador (ET Artículo 50, apartado 1a). 4. En caso de falta de pago o retrasos continuados en el abono del salario pactado, el trabajo puede ser extinto por voluntad del trabajador (ET Artículo 50, apartado 1b). 5. Cualquier otro incumplimiento grave de sus obligaciones por parte del empresario también podría dar lugar a la extinción del contrato (ET Artículo 50, apartado 1c). | SBERT-pairs-bert-base-spanish-wwm-cased | 0.75 |
| mistral | RoBERTalex | Aplica al Estatuto de los Trabajadores a todas las personas que desarrollan actividades económicas remuneradas, sea en forma permanente o temporal. | SBERT-pairs-bert-base-spanish-wwm-cased | 0.77 |

### ¿Qué se considera un empresario en la legislación laboral?
| LLM model | Embedding model | RAG answer | ST model | Score (cosine similarity) |
| --------- | --------------- | ---------- | -------- | ------------------------- |
| mistral | FastEmbedEmbeddings | El término "empresario" en el contexto laboral es alguien que dirige a los representantes legales de los trabajadores y está sujeto a las normas legales respectivas en caso de despedidas colectivas o cualquier otro asunto laboral. | SBERT-pairs-bert-base-spanish-wwm-cased | 0.68 |
| mistral | RoBERTalex | Un empresario, en el contexto de la legislación laboral, es una persona que contrata a otros para trabajar bajo su dirección y control en lo que respecta al trabajo realizado. | SBERT-pairs-bert-base-spanish-wwm-cased | 0.71 |

### ¿Qué relaciones laborales se excluyen de la aplicación del Estatuto de los Trabajadores?
| LLM model | Embedding model | RAG answer | ST model | Score (cosine similarity) |
| --------- | --------------- | ---------- | -------- | ------------------------- |
| mistral | FastEmbedEmbeddings | Las relaciones laborales de carácter especial se excluyen de la aplicación del Estatuto de los Trabajadores. Este concepto incluye: - La del personal de alta dirección no incluido en el artículo 1.3.c). - El servicio del hogar familiar. - La de los penados en las instituciones penitenciarias. - La de los deportistas profesionales. - La de las personas artistas que desarrollan su actividad en las artes escénicas, audiovisuales y musicales, así como las personas que realizan actividades técnicas o auxiliares necesarias para el desarrollo de dicha actividad. - La de las personas que intervengan en operaciones mercantiles por cuenta de uno o más particulares. | SBERT-pairs-bert-base-spanish-wwm-cased | 0.77 |
| mistral | RoBERTalex | | SBERT-pairs-bert-base-spanish-wwm-cased |  |

### Si tengo una empresa española, ¿Se aplican los derechos económicos de la legislación española laboral a los trabajadores españoles contratados en España?
| LLM model | Embedding model | RAG answer | ST model | Score (cosine similarity) |
| --------- | --------------- | ---------- | -------- | ------------------------- |
| mistral | FastEmbedEmbeddings | Los trabajadores españoles contratados en España tienen derecho a los beneficios económicos y otros derechos laborales establecidos por la legislación española. Si un trabajador abandona el trabajo antes del plazo acordado, el empresario puede reclamar una indemnización de daños y perjuicios. Además, si un trabajador ha recibido una especialización profesional con cargo al empresario para poner en marcha proyectos determinados o realizar un trabajo específico, se podrá pactar la permanencia en dicha empresa durante cierto tiempo, pero el acuerdo no será de duración superior a dos años. El cambio de titularidad de una empresa no extingue por sí mismo la relación laboral; el nuevo empresario se convertiría en subrogado de los derechos y obligaciones laborales del anterior, incluyendo los compromisos de pensiones. | SBERT-pairs-bert-base-spanish-wwm-cased | 0.71 |
| mistral | RoBERTalex | ¡Sí! Los trabajadores españoles contratados en España están cubiertos por la legislación española laboral, incluyendo derechos económicos como el salario mínimo, descanso dominical y vacaciones. | SBERT-pairs-bert-base-spanish-wwm-cased | 0.76 |

### ¿Qué es un centro de trabajo?
| LLM model | Embedding model | RAG answer | ST model | Score (cosine similarity) |
| --------- | --------------- | ---------- | -------- | ------------------------- |
| mistral | FastEmbedEmbeddings | Un centro de trabajo es una unidad productiva con organización específica que se encuentra dada de alta ante la autoridad laboral, en el territorio español. También se considera como centro de trabajo el buque en caso de actividad de trabajo en el mar, situado en la provincia donde radique su puerto de base. | SBERT-pairs-bert-base-spanish-wwm-cased | 0.80 |
| mistral | RoBERTalex | Un centro de trabajo es un lugar físico o virtual donde se realiza la actividad laboral. | SBERT-pairs-bert-base-spanish-wwm-cased | 0.69 |

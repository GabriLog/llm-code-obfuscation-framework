# 1. La ofuscación tradicional es el único método fiable
    Error rate: 0%
    Functional match 83.3%
    Node ratio 6.17x
    AST score 0.93
    Tarda entre 1.1 y 1.6 segundos
Ninguno de los LLMs iguala los resultados del ofuscador tradicional.


# 2. La ofuscación de los LLMs falla en la mayoría de casos
- **qwen2.5-coder:7b**:
    functional match 58.3%
    error rate 8.3%
    AST score 0.99
- **llama3.1:8b**:
    functional match 16.7% 
    error rate 41.7%
    AST score 0.56
- **llama3.2:3b**:
    functional match 16.7%
    error rate 66.7%
    AST score 0.41
- **mistral:7b**
    functional match 8.3%
    error rate 83.3%
    AST score 0.32
3/4 modelos generan errores de código en más de la mitad experimentos.
Qwen es la única excepción.

# 3. La desofuscación de los LLMs es el eslabón más débil 
- **qwen2.5-coder:7b**: 
    functional match 16.7%
    error rate 33.3%
    AST score 0.91
- **llama3.1:8b**: 
    functional match 33.3%
    error rate 33.3%
    AST score 0.81
- **llama3.2:3b**:
    functional match 0.0%
    error rate 66.7%
    AST score 0.40
- **mistral:7b**: 
    functional match 8.3% 
    error rate 83.3%
    AST score 0.35
Qwen, el mejor en ofuscación, baja de 58.3% a 16.7% en funcionalidad al desofuscar. 
Llama3.2 no logra ni un solo caso correcto.

# 4. Few-shot no mejora siempre los resultados 
En ofuscación LLM: 
    zero-shot obtiene functional match 33.3% con error rate 45.8%
    few-shot obtiene functional match 16.7% con error rate 54.2% 
En desofuscación: 
    zero-shot obtiene functional match 4.2% con error rate 79.2% 
    few-shot obtiene functional match 25% con error rate 29.2%
El few-shot en la ofuscación empeora los resultados, confunde al modelo?
Sin embargo, en la desofuscación vemos una clara mejoría.

# 5. La especialización en código importa más que el tamaño en la ofuscación
qwen2.5-coder:7b (especializado en código) obtiene functional match 58.3% en ofuscación. 
llama3.1:8b (de propósito general) se queda en 16.7%. 
Con menos parámetros, qwen triplica el rendimiento funcional de llama3.1. 
En la ofuscación el factor determinante es la especialización, no el tamaño.

# 6. El coste computacional hace inviable cualquier uso real
- **qwen2.5-coder:7b**:
    obf_llm: 657s 
    deob_llm: 987s 
- **llama3.1:8b**: 
    obf_llm: 886s 
    deob_llm: 991s
- **llama3.2:3b**:
    obf_llm: 333s 
    deob_llm: 546s 
- **mistral:7b**: 
    obf_llm: 1029s
    deob_llm: 1113s
    La ofuscación tradicional tarda entre 1.1 y 1.6s.
La ofuscación LLM es al menos 200x más lenta que la tradicional. 
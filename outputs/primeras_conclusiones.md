# 1. La ofuscación tradicional es funcionalmente perfecta pero estructuralmente predecible
En los 12 experimentos realizados produce siempre la salida correcta. El node ratio medio ronda 4.5x–6x nodos respecto al original (de 58 nodos a ~475 en factorial, de 234 a ~1200 en analize_numbers), con un ast score medio de ~0.95. Es completamente fiable pero genera un patrón de inflado muy reconocible.

# 2. La ofuscación LLM es inconsistente y mayoritariamente fallida
qwen es el único modelo que funciona de forma repetida, con ast score medio de 0.99 y node ratio de 2.26. El resto se desploma: llama3.2 obtiene ast score medio de 0.49, llama3.1 de 0.46 y mistral de 0.47, con node ratios entre 1.2 y 2.15. En la mayoría de casos generan código con SyntaxError o ReferenceError directamente no ejecutable.

# 3. El AST score es engañoso sin verificar la salida real
Mistral zero-shot small obtiene ast score de 0.973 pero produce ReferenceError: String_fromCharCode is not defined. llama3.1 zero-shot small obtiene 0.985 pero lanza TypeError. Un ast score cercano a 1 no garantiza en absoluto que el código ejecute correctamente.

# 4. La desofuscación LLM es el eslabón más débil
Solo 3 de 16 experimentos producen la salida correcta. Las latencias van de 294 segundos en el mejor caso hasta 1411 segundos. qwen few-shot small es el mejor caso con ast score de 1.0 y salida correcta en 739 segundos. llama3.2 y mistral acumulan errores de sintaxis en prácticamente todos sus intentos de desofuscación.

# 5. Few-shot no aporta mejora consistente
En llama3.2, zero-shot large produce ast score de 0.9996 con salida correcta, mientras few-shot large cae a 0 con SyntaxError. En mistral, zero-shot small obtiene 0.973 y few-shot small cae a 0. Solo qwen mantiene rendimiento similar entre estrategias, con ast scores de 1.0 y 0.9477 respectivamente.

# 6. La especialización en código supera al tamaño del modelo
qwen2.5-coder con 7B parámetros alcanza ast score medio de 0.99 en ofuscación y node ratio de 2.26. llama3.1 con 8B parámetros, es decir más parámetros, se queda en ast score medio de 0.46 y falla en 3 de 4 experimentos. La diferencia de rendimiento entre ambos es mayor que la diferencia de tamaño, lo que apunta a que la especialización en código es el factor determinante.

# 7. El coste computacional hace inviable el uso real
La ofuscación tradicional tarda entre 1 y 4 segundos en todos los casos. qwen obf_llm tarda de media 697 segundos, llama3.1 obf_llm 795 segundos y mistral obf_llm 965 segundos. La desofuscación es aún peor, con llama3.1 few-shot large llegando a 1411 segundos. Estamos hablando de un factor de entre 200x y 1400x más lento para peores resultados.

# 8. Reconstruir semántica es más difícil que transformarla
En ofuscación, qwen logra ast score de 1.0 en 3 de 4 casos. En desofuscación, ese mismo modelo obtiene ast scores de 0.9668 y 0.9642 pero con salida incorrecta o vacía. llama3.2 en desofuscación acumula 3 syntax errors de 4 intentos frente a 1 en ofuscación. El obfuscator tradicional genera patrones con lookup tables y control flow flattening que los modelos no logran revertir.
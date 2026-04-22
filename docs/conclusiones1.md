# 1. La ofuscación tradicional es más estable funcionalmente

Mantiene altas tasas de funcionalidad.
Aunque incrementa mucho el tamaño del AST (node inflation fuerte), no rompe el código.

Conclusión: es un método consistente y seguro, pero predecible.


# 2. La ofuscación LLM es más inestable pero estructuralmente más “inteligente”

A veces AST score muy alto (0.98–1.0) con baja modificación estructural.
Otras veces genera errores de sintaxis o ejecución críticos.
Se observa un patrón:
👉 cuando “funciona”, suele modificar menos nodos (node ratio bajo)
👉 cuando falla, directamente rompe el código (parse errors)

Conclusión: la ofuscación LLM es no determinista y frágil, aunque potencialmente más eficiente estructuralmente.


# 3. La desofuscación LLM es el punto más débil del pipeline

Muestra muchas veces functional_match = false
Alta latencia (muy alto time_seconds)
Frecuentes errores o salidas incompletas
Incluso cuando el AST score es alto, no garantiza recuperación funcional

Conclusión: la desofuscación LLM es costosa y poco fiable para reconstrucción real del código


# 4. El AST score NO es una métrica suficiente por sí sola

AST alto + funcional FAIL
AST alto + código roto o vacío
Esto indica que:
👉 El AST mide similitud estructural, no corrección semántica

Conclusión: AST score es engañoso si no se combina con funcional_match


# 5. El node ratio refleja dos estrategias opuestas

obf_tradicional → node ratio alto (expansión masiva del código)
obf_llm → node ratio bajo o moderado (reestructuración más compacta o errática)

Conclusión:
Tradicional = “ensuciar y expandir”
LLM = “reestructurar o intentar optimizar (pero inestable)”


# 6. El coste computacional del LLM es extremadamente superior

obf_tradicional: ~1–3 segundos
obf_llm / deob_llm: cientos o miles de segundos
Esto es crítico si se piensa en uso real o escalabilidad

Conclusión: orden de magnitud 100x–1000x más lento


# 7. Few-shot vs zero-shot: no hay ventaja consistente clara

few-shot mejora estabilidad en obf_llm
en otros empeora (más errores o menos coherencia)
Tendencia general:
👉 impacto menor que el tipo de tarea (obf vs deob)

Conclusión: la estrategia importa menos que la tarea y el modelo


# 8. La desofuscación es sistemáticamente más difícil que la ofuscación

obf_llm: a veces funciona
deob_llm: falla más frecuentemente incluso cuando AST es alto

Conclusión: reconstruir semántica es más difícil que transformarla
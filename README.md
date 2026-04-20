# llm-code-obfuscation-framework

- core: código que da funcionalidad a la aplicación
- datasets: contiene los scripts con los que trabaja
- logs: registro básico de las ejecuciones realizadas
- outputs: resultados de evaluación, métricas y gráficas
- prompts: contiene los prompts que se pueden utilizar
- runs: ejecución y config experimentos, tradicional, llm
- prompts_config.json: asiganciones de prompt a modelo

## Entorno

- Python 3.10+
- Node.js 18+
- Ollama

## Requisitos HW

Recomendable tener al menos 16 GB de RAM para ejecutar modelos de hasta 8B parámetros

## Ollama

ollama --version

Instalar desde: https://ollama.com

Instalar LLMs:
ollama pull llama3.2:3b  
ollama pull qwen2.5-coder:7b  
ollama pull mistral:7b  
ollama pull llama3.1:8b  

ollama list

## Dependencias

pip install -r requirements.txt  
npm install  

## Ejecución PowerShell

1) py app.py        =>  experimentar con los llms deseados
2) py app.py -ev    =>  evaluación de los datos obtenidos

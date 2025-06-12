#  Deployment Notes – Producción de la API de Procesamiento de Documentos

Este documento describe cómo sería el reemplazo del componente simulado de modelo de lenguaje (LLM) por una solución real en un entorno de producción. El objetivo es mejorar la capacidad de análisis semántico de los documentos mediante herramientas de IA avanzadas.


##  Componente a reemplazar

Actualmente, el proyecto utiliza un archivo `llm.py` que simula dos funciones:

- `summarize_text(text: str)` → devuelve un resumen ficticio.
- `extract_entities(text: str)` → devuelve una lista simulada de entidades.

En producción, este módulo debe ser reemplazado por un modelo real de lenguaje, que puede estar en la nube o ejecutarse de forma local.


##  Opciones de reemplazo en producción

### Opción 1: OpenAI GPT-4 (via API)

**Resumen:** Ideal para entornos cloud que requieran máxima precisión y calidad en el procesamiento de lenguaje natural.

**Ventajas:**
- Alta calidad en resúmenes y detección de entidades.
- Fácil integración con SDK oficial.
- Ideal para productos con acceso a internet y presupuesto para uso por token.

**Consideraciones:**
- Uso responsable del API: manejar errores, límites de cuota, y costes.
- Las claves deben almacenarse en variables de entorno (no hardcoded).


###  Opción 2: Ollama (modelos locales como Mistral o LLaMA)

**Resumen:** Solución completamente local, ideal para despliegues on-premise o cuando se requiere privacidad total de los datos.

**Ventajas:**
- Gratuito y privado.
- Fácil de probar y escalar.
- Compatible con modelos como `llama2`, `mistral`, `gemma`.

**Consideraciones:**
- Ollama debe estar corriendo como servicio.
- Posiblemente necesitarás ajustar la infraestructura para GPUs si se busca rendimiento.


###  Opción 3: Hugging Face Transformers (local o cloud)

**Resumen:** Para proyectos que requieran personalización de modelos o integración en pipelines ML.

**Ventajas:**
- Gran variedad de modelos disponibles.
- Uso local o con inferencia en la nube.
- APIs de NER disponibles como `dslim/bert-base-NER`.

**Consideraciones:**
- Requiere buena RAM y/o GPU para modelos grandes.
- Puedes cachear modelos para rendimiento óptimo.


##  Conclusión

Este sistema ha sido desarrollado de forma modular para facilitar su evolución. El uso de un simulador permitió validar la arquitectura general, mientras que en producción, es recomendable reemplazar el backend LLM por soluciones reales como OpenAI, Ollama o modelos de HuggingFace según las necesidades específicas de privacidad, rendimiento y coste.
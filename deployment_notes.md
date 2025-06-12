#  Deployment Notes – Producción de la API de Procesamiento de Documentos

Este documento resume cómo se puede reemplazar el componente simulado del modelo de lenguaje (llm.py) por una solución real en un entorno de producción. La idea es mejorar el análisis semántico de los documentos, usando herramientas más potentes para generar resúmenes y extraer entidades.


##  Componente a reemplazar

Actualmente, el archivo `llm.py` incluye dos funciones básicas que simulan el comportamiento de un modelo de lenguaje:

- `summarize_text(text: str)` : genera un resumen de ejemplo.
- `extract_entities(text: str)` : devuelve una lista ficticia de entidades.

Estas funciones están pensadas para fines de prueba, pero en producción deberían reemplazarse por un modelo real, ya sea local o basado en API.


##  Opciones de reemplazo en producción

### Opción 1: OpenAI GPT-4 (via API)

**Resumen:** Ideal si el proyecto se va a desplegar en la nube y se busca alta precisión en los resultados.

**Ventajas:**
- Excelente calidad en los resúmenes y en la detección de entidades.
- Integración rápida usando el SDK oficial o peticiones HTTP.

**Consideraciones:**
-Hay costos por token procesado, así que se debe controlar el uso.
-Las claves API deben guardarse como variables de entorno, nunca en el código directamente.


###  Opción 2: Ollama (modelos locales como Mistral o LLaMA)

**Resumen:** Muy útil si se necesita correr todo localmente (on-premise) o si los datos no pueden salir de la red.

**Ventajas:**
- Gratuito, no requiere conexión a Internet.
- Compatible con varios modelos ligeros y eficientes.

**Consideraciones:**
- Se necesita tener el servicio de Ollama corriendo.
- Para mejorar tiempos de respuesta, puede requerir una máquina con GPU.


###  Opción 3: Hugging Face Transformers (local o cloud)

**Resumen:** Cuando se quiere más flexibilidad, personalización, o se planea integrar la solución a un pipeline de ML más amplio.

**Ventajas:**
- Amplia variedad de modelos disponibles.
- Puedes usarlos localmente o vía transformers + pipeline.
- Modelos preentrenados de NER como `bert-base-NER` listos para usar.

**Consideraciones:**
- Algunos modelos son pesados, por lo que se recomienda contar con suficiente RAM o GPU.
- El tiempo de carga inicial puede ser mayor, aunque luego mejora con caché.


##  Conclusión

El proyecto fue diseñado para ser fácilmente adaptable a diferentes entornos. El uso de funciones simuladas permitió enfocarse en la arquitectura general y dejar lista la estructura para incorporar un modelo de lenguaje real cuando sea necesario.
Cualquiera de las opciones mencionadas puede integrarse sin cambiar gran parte del código, ya que las funciones clave (summarize_text y extract_entities) están aisladas. La elección final dependerá de las necesidades del entorno de despliegue: disponibilidad de internet, presupuesto, privacidad y capacidad de cómputo.
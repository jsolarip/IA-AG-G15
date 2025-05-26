# Diseño del Perfil Óptimo de Compañero de Equipo F1 mediante Algoritmos Genéticos

## Descripción del Proyecto

Este proyecto utiliza un Algoritmo Genético (AG) para diseñar y optimizar un "perfil de piloto ideal" para ser el compañero de equipo de Max Verstappen en Red Bull Racing (Fórmula 1). El sistema explora diversas combinaciones de atributos de un piloto ficticio y evalúa su "idealidad" según un conjunto de criterios y reglas predefinidas que simulan las prioridades del equipo.

El AG no selecciona un piloto de una lista preexistente, sino que evoluciona un perfil (un conjunto de características) que maximiza una función de aptitud personalizada.

**Materia:** Inteligencia Artificial
**Institución:** Universidad Tecnológica Nacional - Facultad Regional Buenos Aires (UTN FRBA)
**Año:** 2025

## Características del Perfil de Piloto

El perfil del piloto ideal se define mediante 8 atributos clave, cada uno con 4 valores posibles (codificados con 2 bits):

1.  **A1: Nivel de Experiencia en F1:** Novato, Joven Promesa, Establecido, Veterano.
2.  **A2: Estilo de Conducción Principal:** Agresivo Controlado, Consistente y Calculador, Técnico y Metódico, Adaptable Camaleónico.
3.  **A3: Velocidad Pura (Clasificación):** Regular, Buena, Muy Buena, Excepcional.
4.  **A4: Consistencia en Carrera:** Inconsistente, Algo Consistente, Muy Consistente, Extremadamente Consistente.
5.  **A5: Capacidad de Desarrollo y Feedback Técnico:** Limitada, Adecuada, Fuerte, Excepcional.
6.  **A6: Mentalidad de Equipo y Disposición al Rol:** Primariamente Individualista, Equilibrado, Jugador de Equipo Nato, Totalmente Alineado con el Equipo.
7.  **A7: Encaje con la Marca Red Bull (Carisma/Medios):** Bajo Encaje, Encaje Aceptable, Buen Encaje, Encaje Perfecto.
8.  **A8: Exigencia Salarial Estimada:** Salario Muy Bajo, Salario Bajo, Salario Medio, Salario Alto.

El cromosoma de cada individuo en el AG es una cadena de 16 bits (8 atributos x 2 bits/atributo).

## Estructura del Proyecto

El proyecto consta principalmente de dos archivos Python:

* `config_piloto.py`:
    * Define las constantes del problema (mapeo de bits a valores de atributos).
    * Contiene la función `decodificar_cromosoma(cromosoma_bits)` para traducir un cromosoma binario a un perfil de piloto legible.
    * Incluye la función `evaluar_aptitud_piloto(cromosoma_bits)` que calcula la aptitud de un perfil basado en un conjunto de reglas de bonificación y penalización.
    * Proporciona una función `imprimir_perfil_piloto(cromosoma_bits)` para mostrar un perfil de forma clara.
* `piloto_ideal_ag.py`:
    * Utiliza la librería DEAP para implementar el Algoritmo Genético.
    * Configura los tipos de `Fitness` e `Individual` de DEAP.
    * Registra en la `Toolbox` las funciones para la generación de individuos, población, evaluación (usando `evaluar_aptitud_piloto` de `config_piloto.py`), cruce, mutación y selección.
    * Define los parámetros del AG (tamaño de población, número de generaciones, probabilidades de cruce y mutación).
    * Ejecuta el algoritmo evolutivo.
    * Muestra el mejor perfil de piloto encontrado y su aptitud.
    * Genera un gráfico (usando Matplotlib) de la evolución de la aptitud promedio y máxima a lo largo de las generaciones.

## Requisitos Previos

* Python 3.x
* Las librerías listadas en `requirements.txt`.

## Cómo Ejecutar el Algoritmo Genético

1.  Asegúrate de que tu entorno virtual esté activado y las librerias instaladas.
2.  Navega en tu terminal a la carpeta raíz del proyecto (donde se encuentran `piloto_ideal_ag.py` y `config_piloto.py`).
3.  Ejecuta el script principal:
    ```bash
    python piloto_ideal_ag.py
    ```

## Interpretación de la Salida

Al ejecutar el script:
1.  Se mostrarán en la consola los parámetros con los que se inicia la evolución.
2.  Si `verbose=True` está activado en la configuración del algoritmo de DEAP (como está actualmente), verás estadísticas por cada generación (número de generación, número de evaluaciones, aptitud promedio, desviación estándar, aptitud mínima y máxima).
3.  Al finalizar todas las generaciones, se imprimirá:
    * El "MEJOR PERFIL DE PILOTO ENCONTRADO", detallando los valores de cada uno de los 8 atributos.
    * La aptitud (puntuación) de este mejor perfil.
4.  Se intentará mostrar una ventana con un gráfico de Matplotlib que ilustra la evolución de la aptitud promedio y máxima a lo largo de las generaciones.
    * **Nota sobre el gráfico:** Si estás en un entorno sin GUI (como algunas terminales SSH o MINGW64 con configuraciones por defecto), el gráfico podría no mostrarse directamente y podrías ver una `UserWarning` relacionada con `FigureCanvasAgg`. En tal caso, el código también guarda el gráfico como un archivo de imagen llamado `evolucion_aptitud.png` en la misma carpeta, el cual podrás abrir manualmente.

## Parámetros del Algoritmo y Personalización

Los principales parámetros del AG se encuentran en la función `ejecutar_ag()` dentro de `piloto_ideal_ag.py`:
* `TAM_POBLACION`: Número de individuos por generación.
* `PROBABILIDAD_CRUCE` (CXPB): Probabilidad de que dos individuos se crucen.
* `PROBABILIDAD_MUTACION_IND` (MUTPB): Probabilidad de que un individuo mute.
* `NUM_GENERACIONES` (NGEN): Total de generaciones a ejecutar.

Las reglas para calcular la aptitud, incluyendo bonificaciones y penalizaciones, están definidas en la función `evaluar_aptitud_piloto()` dentro del archivo `config_piloto.py`. Puedes modificar estas reglas para explorar diferentes criterios de "idealidad" para el perfil del piloto.


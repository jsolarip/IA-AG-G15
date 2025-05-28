import random
from deap import base, creator, tools, algorithms # 
import numpy # Para estadísticas
import matplotlib.pyplot as plt # Para gráficos
# --- Importamos desde nuestro archivo de configuración del problema ---
from config_piloto import LONGITUD_CROMOSOMA, evaluar_aptitud_piloto, imprimir_perfil_piloto, evaluar_aptitud_piloto_nueva

# --- 1. Definición de Tipos  ---
# El objetivo es MAXIMIZAR la aptitud, así que los pesos son positivos (1.0)
creator.create("FitnessMax", base.Fitness, weights=(1.0,))

# Cada individuo (cromosoma) será una lista de bits (0s y 1s),
# y tendrá asociada la función de aptitud que acabamos de crear.
creator.create("Individual", list, fitness=creator.FitnessMax)

# --- 2. Inicialización y Registro en la Toolbox ---
toolbox = base.Toolbox()

# Generador de Atributos (cada bit del cromosoma):
# 'attr_bool' generará un 0 o un 1 al azar.
toolbox.register("attr_bool", random.randint, 0, 1)

# Inicializador de Individuos (cromosomas):
# 'individual' creará un individuo completo (lista de 16 bits)
# usando 'attr_bool' 16 veces (LONGITUD_CROMOSOMA).
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, LONGITUD_CROMOSOMA)

# Inicializador de Población:
# 'population' creará una lista de individuos.
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# --- 3. Registro de los Operadores Genéticos ---

# A. Función de Evaluación (Fitness Function):
#    Le decimos a DEAP que la función que debe usar para evaluar la aptitud
#    de cada individuo se llama 'evaluar_aptitud_piloto' (la que creamos en config_piloto.py).
#    DEAP llamará a esta función pasándole un individuo (un cromosoma de 16 bits).

#toolbox.register("evaluate", evaluar_aptitud_piloto)
toolbox.register("evaluate", evaluar_aptitud_piloto_nueva) # esta es la nueva, la original esta comentada arriba


# B. Operador de Cruce (Crossover):
#    Registramos la operación de cruce. 'tools.cxTwoPoint' es un cruce de dos puntos estándar.
#    Cuando DEAP necesite cruzar dos individuos padres, usará esta función.
#    Hay otros tipos de cruce como cxOnePoint (usado en el ejemplo de Halloween), cxUniform, etc.
#    cxTwoPoint suele funcionar bien para cromosomas binarios.
toolbox.register("mate", tools.cxTwoPoint)

# C. Operador de Mutación:
#    Registramos la operación de mutación. 'tools.mutFlipBit' es común para cromosomas binarios.
#    Esta función toma un individuo y voltea cada uno de sus bits (de 0 a 1 o de 1 a 0)
#    con una probabilidad independiente 'indpb'.
#    'indpb=0.05' significa que cada bit tiene un 5% de probabilidad de ser volteado.
#    Este valor (0.05) es un hiperparámetro que podrías ajustar más adelante.
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

# D. Operador de Selección:
#    Registramos el método de selección. 'tools.selTournament' implementa la selección por torneo.
#    'tournsize=3' significa que para seleccionar un individuo
#    para la siguiente generación (o para cruce), DEAP tomará 3 individuos al azar de la
#    población actual y elegirá al mejor de esos 3 (el que tenga mayor aptitud).
#    Es un método de selección común y efectivo.
toolbox.register("select", tools.selTournament, tournsize=3) 

# --- 4. Configuración de Estadísticas y Salón de la Fama (Hall of Fame) ---

# A. Salón de la Fama (Hall of Fame):
#    'tools.HallOfFame(1)' crea un objeto que almacenará al mejor individuo encontrado
#    a lo largo de todas las generaciones. El '1' significa que solo guardará al mejor.
#    Si quisieras guardar los 5 mejores, usarías tools.HallOfFame(5).
hof = tools.HallOfFame(7)

# B. Estadísticas:
#    'tools.Statistics' nos permite llevar un registro de ciertas métricas de la
#    población en cada generación (como el promedio, mínimo, máximo de la aptitud).
#    El argumento 'lambda ind: ind.fitness.values' le dice que las estadísticas
#    se deben calcular sobre los valores de aptitud de los individuos.
stats = tools.Statistics(lambda ind: ind.fitness.values)

# Registramos las estadísticas específicas que queremos calcular:
# - "avg": Calculará el promedio de las aptitudes.
# - "std": Calculará la desviación estándar de las aptitudes.
# - "min": Calculará la aptitud mínima.
# - "max": Calculará la aptitud máxima.
# 'numpy.mean', 'numpy.std', etc., son funciones de la librería NumPy que realizan estos cálculos.
stats.register("avg", numpy.mean) 
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)

# --- 5. Definición de Parámetros del Algoritmo y Ejecución ---
def ejecutar_ag():
    # Parámetros del algoritmo genético
    TAM_POBLACION = 100  # Tamaño de la población 
    PROBABILIDAD_CRUCE = 0.7 # Probabilidad de que dos individuos se crucen (CXPB)
    PROBABILIDAD_MUTACION = 0.3 # Probabilidad de que un individuo mute (MUTPB)
    NUM_GENERACIONES = 100 # Número de generaciones a ejecutar (NGEN)

    print(f"Iniciando evolución con {NUM_GENERACIONES} generaciones y población de {TAM_POBLACION} individuos...")
    print(f"Probabilidad de Cruce: {PROBABILIDAD_CRUCE}, Probabilidad de Mutación: {PROBABILIDAD_MUTACION}")

    # Creación de la población inicial
    # Llama a la función "population" que registramos en la toolbox,
    # pasándole n=TAM_POBLACION para crear la cantidad deseada de individuos.
    pop = toolbox.population(n=TAM_POBLACION)

    # Ejecución del algoritmo evolutivo
    # algorithms.eaSimple es uno de los algoritmos predefinidos en DEAP.
    # También podríamos usar algorithms.eaMuPlusLambda 
    # mu = número de individuos a seleccionar para la siguiente generación.
    # lambda_ = número de hijos a generar en cada generación.
    
    # El objeto 'logbook' registrará las estadísticas de cada generación.
    pop, logbook = algorithms.eaMuPlusLambda(
        pop,                     # La población inicial
        toolbox,                 # Nuestra caja de herramientas con los operadores registrados
        mu=TAM_POBLACION,        # Número de individuos a seleccionar para la siguiente generación
        lambda_=TAM_POBLACION,   # Número de hijos a generar
        cxpb=PROBABILIDAD_CRUCE, # Probabilidad de cruce
        mutpb=PROBABILIDAD_MUTACION, # Probabilidad de mutación
        ngen=NUM_GENERACIONES,   # Número de generaciones
        stats=stats,             # Objeto para registrar estadísticas
        halloffame=hof,          # Objeto para guardar al mejor(es) individuo(s)
        verbose=True             # Imprime información del progreso en cada generación
    )

    return pop, logbook, hof

# --- Bloque Principal de Ejecución ---
if __name__ == "__main__":
    # Ejecutamos el algoritmo genético
    poblacion_final, libro_estadisticas, salon_fama = ejecutar_ag()
    """
    # Imprimimos el mejor individuo encontrado
    mejor_individuo = salon_fama[0] # El HallOfFame guarda al mejor en la posición 0
    
    print("\n--- MEJOR PERFIL DE PILOTO ENCONTRADO ---")
    imprimir_perfil_piloto(mejor_individuo) # Usamos nuestra función de config_piloto.py
    print(f"Aptitud del mejor perfil: {mejor_individuo.fitness.values[0]:.2f}")
    """
    # Para imprimir en caso de usar más de 1 elemento en el Hall of Fame
    for piloto_hof in salon_fama:
        print("\n --- SUGERENCIA PILOTO CANDIDATO ---")
        imprimir_perfil_piloto(piloto_hof) # Usamos nuestra función de config_piloto.py
        print(f"Aptitud del perfil sugerido: {piloto_hof.fitness.values[0]:.2f}")

    # Graficar la evolución de la aptitud
    gen = libro_estadisticas.select("gen")
    avg_fitness = libro_estadisticas.select("avg")
    max_fitness = libro_estadisticas.select("max")

    plt.figure(figsize=(10, 6))
    plt.plot(gen, avg_fitness, label="Aptitud Promedio")
    plt.plot(gen, max_fitness, label="Aptitud Máxima")
    plt.xlabel("Generación")
    plt.ylabel("Aptitud")
    plt.legend(loc="lower right")
    plt.title("Evolución de la Aptitud a lo largo de las Generaciones")
    plt.grid(True)
    plt.show()

    print("\nEvolución completada.")
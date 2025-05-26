# --- Definición de Atributos y sus Valores ---
# Estos diccionarios nos ayudarán a decodificar los bits del cromosoma
# en valores legibles y a usarlos en la función de aptitud.

ATRIBUTOS_CONFIG = {
    "A1_Experiencia": {
        "00": "Novato", # (0-1 año completo)
        "01": "Joven Promesa", # (2-4 años)
        "10": "Establecido", # (5-8 años)
        "11": "Veterano" # (>8 años)
    },
    "A2_EstiloConduccion": {
        "00": "Agresivo Controlado",
        "01": "Consistente y Calculador",
        "10": "Técnico y Metódico",
        "11": "Adaptable Camaleónico"
    },
    "A3_VelocidadPura": {
        "00": "Regular",
        "01": "Buena",
        "10": "Muy Buena",
        "11": "Excepcional"
    },
    "A4_ConsistenciaCarrera": {
        "00": "Inconsistente",
        "01": "Algo Consistente",
        "10": "Muy Consistente",
        "11": "Extremadamente Consistente"
    },
    "A5_FeedbackTecnico": {
        "00": "Limitada",
        "01": "Adecuada",
        "10": "Fuerte",
        "11": "Excepcional"
    },
    "A6_MentalidadEquipo": {
        "00": "Primariamente Individualista",
        "01": "Equilibrado",
        "10": "Jugador de Equipo Nato",
        "11": "Totalmente Alineado con el Equipo"
    },
    "A7_EncajeMarca": {
        "00": "Bajo Encaje",
        "01": "Encaje Aceptable",
        "10": "Buen Encaje",
        "11": "Encaje Perfecto"
    },
    "A8_ExigenciaSalarial": {
        "00": "Salario Muy Bajo",
        "01": "Salario Bajo",
        "10": "Salario Medio",
        "11": "Salario Alto"
    }
}

# Definimos el orden y el tamaño en bits de cada atributo en el cromosoma
# (nombre_atributo, bits_inicio_en_cromosoma_contando_desde_0, cantidad_de_bits)
# Esto es si concatenamos A1+A2+A3...
# A1: bits 0-1
# A2: bits 2-3
# A3: bits 4-5
# ...
# A8: bits 14-15
ORDEN_ATRIBUTOS = [
    ("A1_Experiencia", 0, 2),
    ("A2_EstiloConduccion", 2, 2),
    ("A3_VelocidadPura", 4, 2),
    ("A4_ConsistenciaCarrera", 6, 2),
    ("A5_FeedbackTecnico", 8, 2),
    ("A6_MentalidadEquipo", 10, 2),
    ("A7_EncajeMarca", 12, 2),
    ("A8_ExigenciaSalarial", 14, 2)
]

LONGITUD_CROMOSOMA = 16

# --- Función para Decodificar un Cromosoma ---
def decodificar_cromosoma(cromosoma_bits):
    """
    Convierte un cromosoma (lista de 16 bits) en un diccionario
    con los atributos del perfil del piloto y sus valores legibles.
    """
    if len(cromosoma_bits) != LONGITUD_CROMOSOMA:
        raise ValueError(f"El cromosoma debe tener {LONGITUD_CROMOSOMA} bits.")

    perfil_decodificado = {}
    for nombre_attr, inicio_bit, num_bits in ORDEN_ATRIBUTOS:
        # Extraer los bits para este atributo
        bits_atributo = "".join(map(str, cromosoma_bits[inicio_bit : inicio_bit + num_bits]))
        # Obtener el valor legible del diccionario ATRIBUTOS_CONFIG
        perfil_decodificado[nombre_attr] = ATRIBUTOS_CONFIG[nombre_attr][bits_atributo]

    return perfil_decodificado

# --- Función de Aptitud ---
def evaluar_aptitud_piloto(cromosoma_bits):
    """
    Calcula la aptitud de un perfil de piloto representado por un cromosoma,
    """
    perfil = decodificar_cromosoma(cromosoma_bits)
    
    puntaje_base = 0 # Puntaje base inicial, puede ser ajustado según sea necesario
    bonificaciones = 0
    penalizaciones = 0

    # --- A. Características Deseables (Bonificaciones) ---

    # BD1: Rendimiento sólido en pista 
    if (perfil["A3_VelocidadPura"] in ["Muy Buena", "Excepcional"] and 
        perfil["A4_ConsistenciaCarrera"] in ["Muy Consistente", "Extremadamente Consistente"]):
        bonificaciones += 10

    # BD2: Mentalidad constructiva para el equipo 
    if (perfil["A6_MentalidadEquipo"] in ["Jugador de Equipo Nato", "Totalmente Alineado con el Equipo"] and
        perfil["A5_FeedbackTecnico"] in ["Fuerte", "Excepcional"]):
        bonificaciones += 8

    # BD3: Perfil Red Bull (juventud/marca con costo razonable) 
    if ((perfil["A1_Experiencia"] in ["Novato", "Joven Promesa"] or 
         perfil["A7_EncajeMarca"] in ["Buen Encaje", "Encaje Perfecto"]) and
        (perfil["A8_ExigenciaSalarial"] in ["Salario Muy Bajo", "Salario Bajo"])): # El doc dice "Salario Muy Bajo" O "Salario Bajo"
        bonificaciones += 7

    # BD4: Compañero mecánico 
    if (perfil["A5_FeedbackTecnico"] == "Fuerte" and # El doc dice "Fuerte" específicamente
        perfil["A6_MentalidadEquipo"] == "Jugador de Equipo Nato"): # El doc dice "Jugador de Equipo Nato" específicamente
        bonificaciones += 9

    # BD5: Futuro rentable (Promesa con carisma y sueldo razonable) 
    if (perfil["A1_Experiencia"] == "Joven Promesa" and # El doc dice "Joven Promesa" específicamente
        (perfil["A7_EncajeMarca"] in ["Buen Encaje", "Encaje Perfecto"]) and
        perfil["A8_ExigenciaSalarial"] == "Salario Bajo"): # El doc dice "Salario Bajo" específicamente
        bonificaciones += 7
        
    # BD6: Adaptabilidad y consistencia 
    if (perfil["A2_EstiloConduccion"] == "Adaptable Camaleónico" and # El doc dice "Adaptable Camaleónico" específicamente
        perfil["A4_ConsistenciaCarrera"] == "Muy Consistente"): # El doc dice "Muy Consistente" específicamente
        bonificaciones += 6

    # --- B. Reglas de Incompatibilidad (Penalizaciones) ---

    # INC1: Veterano excesivamente barato 
    if (perfil["A1_Experiencia"] == "Veterano" and 
        perfil["A8_ExigenciaSalarial"] in ["Salario Muy Bajo", "Salario Bajo"]):
        penalizaciones += 6 

    # INC2: Estrella totalmente sumisa 
    if (perfil["A3_VelocidadPura"] == "Excepcional" and 
        perfil["A6_MentalidadEquipo"] == "Totalmente Alineado con el Equipo"):
        penalizaciones += 5

    # INC3: Novato con conocimiento técnico de élite 
    if (perfil["A1_Experiencia"] == "Novato" and 
        perfil["A5_FeedbackTecnico"] == "Excepcional"):
        penalizaciones += 4
        
    # INC4: Agresividad y sumisión total 
    if (perfil["A6_MentalidadEquipo"] in ["Jugador de Equipo Nato", "Totalmente Alineado con el Equipo"] and 
        perfil["A2_EstiloConduccion"] == "Agresivo Controlado"):
        penalizaciones += 3
        
    # INC5: El "super talento irrealmente barato" 
    condiciones_elite_cumplidas_inc5 = 0
    if perfil["A3_VelocidadPura"] == "Excepcional": condiciones_elite_cumplidas_inc5 += 1
    if perfil["A4_ConsistenciaCarrera"] == "Extremadamente Consistente": condiciones_elite_cumplidas_inc5 += 1
    if perfil["A5_FeedbackTecnico"] == "Excepcional": condiciones_elite_cumplidas_inc5 += 1
    if perfil["A7_EncajeMarca"] == "Encaje Perfecto": condiciones_elite_cumplidas_inc5 += 1
    
    if condiciones_elite_cumplidas_inc5 >= 3 and perfil["A8_ExigenciaSalarial"] in ["Salario Muy Bajo", "Salario Bajo"]:
        penalizaciones += 10
        
    # INC6: Adaptable sin buen feedback 
    if (perfil["A2_EstiloConduccion"] == "Adaptable Camaleónico" and 
        perfil["A5_FeedbackTecnico"] == "Limitada"):
        penalizaciones += 4

    # INC7: Salario alto con baja imagen 
    if (perfil["A8_ExigenciaSalarial"] == "Salario Alto" and 
        perfil["A7_EncajeMarca"] == "Bajo Encaje"):
        penalizaciones += 5

    # INC8: Mucha experiencia, poca consistencia 
    if (perfil["A1_Experiencia"] in ["Establecido", "Veterano"] and 
        perfil["A4_ConsistenciaCarrera"] == "Inconsistente"):
        penalizaciones += 4

    # INC9: Calculador pero excepcional en clasificación pura 
    if (perfil["A2_EstiloConduccion"] == "Consistente y Calculador" and 
        perfil["A3_VelocidadPura"] == "Excepcional"):
        penalizaciones += 3
        
    # Cálculo Final de Aptitud 
    aptitud_final = puntaje_base + bonificaciones - penalizaciones
    
    # DEAP espera que la función de aptitud devuelva una tupla
    return (max(0, aptitud_final),) # Asegura que la aptitud no sea negativa, lo cual es buena práctica



# --- Función para imprimir un individuo de forma legible (opcional pero útil) ---
def imprimir_perfil_piloto(cromosoma_bits):
    """
    Imprime de forma legible el perfil de piloto correspondiente a un cromosoma.
    """
    perfil = decodificar_cromosoma(cromosoma_bits)
    print("--- Perfil de Piloto Ideal ---")
    for atributo, valor in perfil.items():
        print(f"{atributo.replace('_', ' ')}: {valor}")
    print(f"Aptitud Bruta (ejemplo): {evaluar_aptitud_piloto(cromosoma_bits)[0]}") # Solo para mostrar, la aptitud se asigna en el AG
    print("-----------------------------")

""" # --- PARA PROBAR ESTE ARCHIVO (puedes borrar o comentar después) ---
import random # Necesitarás importar random aquí si no está ya al inicio del archivo

print("--- INICIO DE PRUEBA DE config_piloto.py ---")

# Generamos un cromosoma aleatorio de 16 bits para la prueba
cromosoma_test = [random.randint(0,1) for _ in range(LONGITUD_CROMOSOMA)]
print(f"Cromosoma de prueba generado: {cromosoma_test}")

print("\nProbando la decodificación, evaluación e impresión con imprimir_perfil_piloto...")
try:
    # La función imprimir_perfil_piloto internamente llamará a
    # decodificar_cromosoma y a evaluar_aptitud_piloto (según la definimos)
    imprimir_perfil_piloto(cromosoma_test)
except ValueError as ve: # Captura el error de longitud si ocurre
    print(f"Error al procesar el cromosoma: {ve}")
except KeyError as ke: # Captura errores si una clave de bits no se encuentra en ATRIBUTOS_CONFIG
    print(f"Error de clave al decodificar el perfil (revisa ATRIBUTOS_CONFIG y los bits generados): {ke}")
except Exception as e: # Captura cualquier otro error
    print(f"Ocurrió un error inesperado: {e}")
    
print("--- FIN DE PRUEBA DE config_piloto.py ---") """
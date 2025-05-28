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
    
    puntaje_base = 0
    bonificaciones_individuales = 0
    bonificaciones_sinergia = 0
    penalizaciones = 0 # Un solo acumulador para todas las penalizaciones

    # --- A. Bonificaciones por Atributos Individuales Positivos (BIs) ---
    if perfil["A1_Experiencia"] == "Joven Promesa": bonificaciones_individuales += 2
    elif perfil["A1_Experiencia"] == "Establecido": bonificaciones_individuales += 2
    elif perfil["A1_Experiencia"] == "Veterano": bonificaciones_individuales += 1

    if perfil["A2_EstiloConduccion"] == "Agresivo Controlado": bonificaciones_individuales += 4 # antes era 2
    elif perfil["A2_EstiloConduccion"] == "Adaptable Camaleónico": bonificaciones_individuales += 2

    if perfil["A3_VelocidadPura"] == "Excepcional": bonificaciones_individuales += 4
    elif perfil["A3_VelocidadPura"] == "Muy Buena": bonificaciones_individuales += 2

    if perfil["A4_ConsistenciaCarrera"] == "Extremadamente Consistente": bonificaciones_individuales += 4
    elif perfil["A4_ConsistenciaCarrera"] == "Muy Consistente": bonificaciones_individuales += 2

    if perfil["A5_FeedbackTecnico"] == "Excepcional": bonificaciones_individuales += 4
    elif perfil["A5_FeedbackTecnico"] == "Fuerte": bonificaciones_individuales += 2

    if perfil["A6_MentalidadEquipo"] == "Jugador de Equipo Nato": bonificaciones_individuales += 2
    elif perfil["A6_MentalidadEquipo"] == "Totalmente Alineado con el Equipo": bonificaciones_individuales += 3
    elif perfil["A6_MentalidadEquipo"] == "Equilibrado": bonificaciones_individuales += 1

    if perfil["A7_EncajeMarca"] == "Encaje Perfecto": bonificaciones_individuales += 3
    elif perfil["A7_EncajeMarca"] == "Buen Encaje": bonificaciones_individuales += 2

    if perfil["A8_ExigenciaSalarial"] == "Salario Muy Bajo": bonificaciones_individuales += 2 # antes 3
    elif perfil["A8_ExigenciaSalarial"] == "Salario Bajo": bonificaciones_individuales += 1 # antes 2

    # --- B. Bonificaciones por Sinergias (BDs) ---
    # BD1
    if (perfil["A3_VelocidadPura"] in ["Muy Buena", "Excepcional"] and 
        perfil["A4_ConsistenciaCarrera"] in ["Muy Consistente", "Extremadamente Consistente"]):
        bonificaciones_sinergia += 10
    # BD2
    if (perfil["A6_MentalidadEquipo"] in ["Jugador de Equipo Nato", "Totalmente Alineado con el Equipo"] and
        perfil["A5_FeedbackTecnico"] in ["Fuerte", "Excepcional"]):
        bonificaciones_sinergia += 8
    # BD3
    if ((perfil["A1_Experiencia"] in ["Novato"] or                            #, "Joven Promesa"] or // comento esto para separar la bd3 de la 5 
         perfil["A7_EncajeMarca"] in ["Buen Encaje", "Encaje Perfecto"]) and
        (perfil["A8_ExigenciaSalarial"] in ["Salario Muy Bajo", "Salario Bajo"])):
        bonificaciones_sinergia += 6 # antes 7
    # BD4
    if (perfil["A5_FeedbackTecnico"] == "Fuerte" and
        perfil["A6_MentalidadEquipo"] == "Jugador de Equipo Nato"):
        bonificaciones_sinergia += 9
    # BD5
    if (perfil["A1_Experiencia"] == "Joven Promesa" and
        (perfil["A7_EncajeMarca"] in ["Buen Encaje", "Encaje Perfecto"]) and
        perfil["A8_ExigenciaSalarial"] == "Salario Bajo"):
        bonificaciones_sinergia += 7
    # BD6
    if (perfil["A2_EstiloConduccion"] == "Adaptable Camaleónico" and
        perfil["A4_ConsistenciaCarrera"] == "Muy Consistente"):
        bonificaciones_sinergia += 6
    # BD7 
    if (perfil["A1_Experiencia"] in ["Establecido", "Veterano"] and
        perfil["A5_FeedbackTecnico"] == "Excepcional" and
        perfil["A4_ConsistenciaCarrera"] in ["Muy Consistente", "Extremadamente Consistente"]):
        bonificaciones_sinergia += 10
    # BD8 
    if (perfil["A1_Experiencia"] == "Veterano" and
        perfil["A7_EncajeMarca"] in ["Buen Encaje"] and # saque encaje perfecto xq raro que un veterano se asocie con la imagen redbull
        perfil["A6_MentalidadEquipo"] in ["Jugador de Equipo Nato", "Totalmente Alineado con el Equipo"]):
        bonificaciones_sinergia += 8
    # BD9 
    if ((perfil["A3_VelocidadPura"] == "Excepcional" or perfil["A5_FeedbackTecnico"] == "Excepcional") and
        perfil["A8_ExigenciaSalarial"] == "Salario Medio"):
        bonificaciones_sinergia += 4
        
    # --- C. Reglas de Incompatibilidad (Penalizaciones - INCs) ---
    # INC1
    if (perfil["A1_Experiencia"] == "Veterano" and 
        perfil["A8_ExigenciaSalarial"] in ["Salario Muy Bajo", "Salario Bajo"]):
        penalizaciones += 9 # antes era 6
    # INC2
    if (perfil["A3_VelocidadPura"] == "Excepcional" and 
        perfil["A6_MentalidadEquipo"] == "Totalmente Alineado con el Equipo"):
        penalizaciones += 5
    # INC3
    if (perfil["A1_Experiencia"] == "Novato" and 
        perfil["A5_FeedbackTecnico"] == "Excepcional"):
        penalizaciones += 4
    # INC4
    if (perfil["A6_MentalidadEquipo"] in ["Jugador de Equipo Nato", "Totalmente Alineado con el Equipo"] and 
        perfil["A2_EstiloConduccion"] == "Agresivo Controlado"):
        penalizaciones += 3
    # INC5
    condiciones_elite_inc5 = 0
    if perfil["A3_VelocidadPura"] == "Excepcional": condiciones_elite_inc5 += 1
    if perfil["A4_ConsistenciaCarrera"] == "Extremadamente Consistente": condiciones_elite_inc5 += 1
    if perfil["A5_FeedbackTecnico"] == "Excepcional": condiciones_elite_inc5 += 1
    if perfil["A7_EncajeMarca"] == "Encaje Perfecto": condiciones_elite_inc5 += 1
    if condiciones_elite_inc5 >= 2 and perfil["A8_ExigenciaSalarial"] in ["Salario Muy Bajo", "Salario Bajo"]:
        penalizaciones += 13 # antes 9
    # INC6
    if (perfil["A2_EstiloConduccion"] == "Adaptable Camaleónico" and 
        perfil["A5_FeedbackTecnico"] == "Limitada"):
        penalizaciones += 4
    # INC7
    if (perfil["A8_ExigenciaSalarial"] == "Salario Alto" and 
        perfil["A7_EncajeMarca"] == "Bajo Encaje"):
        penalizaciones += 5
    # INC8
    if (perfil["A1_Experiencia"] in ["Establecido", "Veterano"] and 
        perfil["A4_ConsistenciaCarrera"] == "Inconsistente"):
        penalizaciones += 4
    # INC9
    if (perfil["A2_EstiloConduccion"] == "Consistente y Calculador" and 
        perfil["A3_VelocidadPura"] == "Excepcional"):
        penalizaciones += 3
    # INC10
    if (perfil["A1_Experiencia"] in ["Novato", "Joven Promesa"] and
        perfil["A5_FeedbackTecnico"] in ["Fuerte", "Excepcional"]):
        penalizaciones += 2
    # INC11
    if (perfil["A3_VelocidadPura"] == "Excepcional" and
        perfil["A4_ConsistenciaCarrera"] == "Extremadamente Consistente"):
        penalizaciones += 3
    # INC12
    if (perfil["A1_Experiencia"] == "Joven Promesa" and
        perfil["A2_EstiloConduccion"] == "Adaptable Camaleónico" and
        perfil["A7_EncajeMarca"] in ["Buen Encaje", "Encaje Perfecto"] and
        (perfil["A3_VelocidadPura"] in ["Muy Buena", "Excepcional"] or 
         perfil["A4_ConsistenciaCarrera"] in ["Muy Consistente", "Extremadamente Consistente"])):
        penalizaciones += 6 # antes era 3
    # INC13
    if (perfil["A6_MentalidadEquipo"] in ["Jugador de Equipo Nato", "Totalmente Alineado con el Equipo"] and
        perfil["A3_VelocidadPura"] in ["Muy Buena", "Excepcional"]):
        penalizaciones += 4
    # INC14
    if (perfil["A1_Experiencia"] in ["Novato", "Joven Promesa"] and
        perfil["A3_VelocidadPura"] in ["Muy Buena", "Excepcional"] and
        perfil["A4_ConsistenciaCarrera"] in ["Muy Consistente", "Extremadamente Consistente"] and
        perfil["A8_ExigenciaSalarial"] in ["Salario Muy Bajo", "Salario Bajo"]):
        penalizaciones += 8 # antes era 5
    # INC15
    if (perfil["A1_Experiencia"] == "Veterano" and
        perfil["A3_VelocidadPura"] == "Excepcional" and
        perfil["A8_ExigenciaSalarial"] == "Salario Alto" and
        perfil["A6_MentalidadEquipo"] in ["Equilibrado", "Primariamente Individualista"]):
        penalizaciones += 9
    # INC16
    if (perfil["A1_Experiencia"] in ["Establecido", "Veterano"] and
        perfil["A3_VelocidadPura"] in ["Muy Buena", "Excepcional"] and
        perfil["A4_ConsistenciaCarrera"] in ["Muy Consistente", "Extremadamente Consistente"]):
        penalizaciones += 6
    # INC17
    if (perfil["A1_Experiencia"] in ["Establecido", "Veterano"] and
        perfil["A5_FeedbackTecnico"] in ["Fuerte", "Excepcional"] and
        perfil["A8_ExigenciaSalarial"] in ["Salario Medio", "Salario Alto"]):
        penalizaciones += 7
    # INC18
    if (perfil["A1_Experiencia"] == "Veterano" and
        perfil["A2_EstiloConduccion"] == "Agresivo Controlado"):
        penalizaciones += 5
    # INC19 (Ajustada)
    if (perfil["A2_EstiloConduccion"] == "Agresivo Controlado" and
        perfil["A3_VelocidadPura"] in ["Muy Buena", "Excepcional"] and 
        perfil["A4_ConsistenciaCarrera"] != "Extremadamente Consistente"):
        penalizaciones += 4
    #INC20
    if (perfil["A4_ConsistenciaCarrera"] in ["Extremadamente Consistente","Muy Consistente"] and
        perfil["A8_ExigenciaSalarial"] in ["Salario Muy Bajo", "Salario Bajo"]):
        penalizaciones += 9
    #INC21
    if (perfil["A1_Experiencia"] == "Veterano" and
        perfil["A7_EncajeMarca"] == "Encaje Perfecto"):
        penalizaciones += 5

    # TODO (al menos considerar): salvar de restricciones de salarios muy bajos a los novatos, o premiarlos x eso
        
    aptitud_final = (puntaje_base + 
                     bonificaciones_individuales + 
                     bonificaciones_sinergia - 
                     penalizaciones)
    
    return (max(0, aptitud_final),)



# --- Función para imprimir un individuo de forma legible (opcional pero útil) ---
def imprimir_perfil_piloto(cromosoma_bits):
    """
    Imprime de forma legible el perfil de piloto correspondiente a un cromosoma.
    """
    perfil = decodificar_cromosoma(cromosoma_bits)
    print("--- Perfil de Piloto Ideal ---")
    for atributo, valor in perfil.items():
        print(f"{atributo.replace('_', ' ')}: {valor}")
    
    #print(f"Aptitud Bruta (ejemplo): {evaluar_aptitud_piloto(cromosoma_bits)[0]}") # Solo para mostrar, la aptitud se asigna en el AG

    print(f"Aptitud Bruta NUEVA: {evaluar_aptitud_piloto_nueva(cromosoma_bits)[0]}") # Solo para mostrar, la aptitud se asigna en el AG
    
    print("-----------------------------")

# --- PARA PROBAR ESTE ARCHIVO (puedes borrar o comentar después) ---
""" import random 

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
    
print("--- FIN DE PRUEBA DE config_piloto.py ---")  """

def evaluar_aptitud_piloto_nueva(cromosoma_bits):
    perfil = decodificar_cromosoma(cromosoma_bits)

    puntaje_base = 0
    bonificaciones_individuales = 0
    bonificaciones_sinergia = 0
    penalizaciones = 0

    # --- Bonificaciones Individuales ---
    #BI1
    if perfil["A1_Experiencia"] == "Joven Promesa": bonificaciones_individuales += 2
    elif perfil["A1_Experiencia"] == "Establecido": bonificaciones_individuales += 2
    elif perfil["A1_Experiencia"] == "Veterano": bonificaciones_individuales += 1
    #BI2
    if perfil["A2_EstiloConduccion"] == "Agresivo Controlado": bonificaciones_individuales += 2
    elif perfil["A2_EstiloConduccion"] == "Adaptable Camaleónico": bonificaciones_individuales += 2
    #BI3
    if perfil["A3_VelocidadPura"] == "Excepcional": bonificaciones_individuales += 4
    elif perfil["A3_VelocidadPura"] == "Muy Buena": bonificaciones_individuales += 2
    #BI4
    if perfil["A4_ConsistenciaCarrera"] == "Extremadamente Consistente": bonificaciones_individuales += 4
    elif perfil["A4_ConsistenciaCarrera"] == "Muy Consistente": bonificaciones_individuales += 2
    #BI5
    if perfil["A5_FeedbackTecnico"] == "Excepcional": bonificaciones_individuales += 4
    elif perfil["A5_FeedbackTecnico"] == "Fuerte": bonificaciones_individuales += 2
    #BI6
    if perfil["A6_MentalidadEquipo"] == "Jugador de Equipo Nato": bonificaciones_individuales += 2
    elif perfil["A6_MentalidadEquipo"] == "Totalmente Alineado con el Equipo": bonificaciones_individuales += 3
    elif perfil["A6_MentalidadEquipo"] == "Equilibrado": bonificaciones_individuales += 1
    #BI7
    if perfil["A7_EncajeMarca"] == "Encaje Perfecto": bonificaciones_individuales += 3
    elif perfil["A7_EncajeMarca"] == "Buen Encaje": bonificaciones_individuales += 2
    #BI8
    if perfil["A8_ExigenciaSalarial"] == "Salario Muy Bajo": bonificaciones_individuales += 2
    elif perfil["A8_ExigenciaSalarial"] == "Salario Bajo": bonificaciones_individuales += 1

    # --- Bonificaciones por Sinergia ---
    #BD1
    BD1_aplicado = False
    if (perfil["A3_VelocidadPura"] in ["Muy Buena", "Excepcional"] and 
        perfil["A4_ConsistenciaCarrera"] in ["Muy Consistente", "Extremadamente Consistente"]):
        bonificaciones_sinergia += 10
        BD1_aplicado = True
    #BD2
    if (perfil["A5_FeedbackTecnico"] in ["Fuerte", "Excepcional"] and
        perfil["A6_MentalidadEquipo"] in ["Jugador de Equipo Nato", "Totalmente Alineado con el Equipo"]):
        bonificaciones_sinergia += 10
    #BD3
    if (perfil["A1_Experiencia"] in ["Novato", "Joven Promesa"] and
        perfil["A7_EncajeMarca"] in ["Buen Encaje", "Encaje Perfecto"] and
        perfil["A8_ExigenciaSalarial"] in ["Salario Muy Bajo", "Salario Bajo"]):
        bonificaciones_sinergia += 6
    #BD4
    if (perfil["A2_EstiloConduccion"] == "Adaptable Camaleónico" and
        perfil["A4_ConsistenciaCarrera"] == "Muy Consistente"):
        bonificaciones_sinergia += 6
    #BD5
    if (perfil["A1_Experiencia"] in ["Establecido", "Veterano"] and
        perfil["A5_FeedbackTecnico"] == "Excepcional" and
        perfil["A4_ConsistenciaCarrera"] in ["Muy Consistente", "Extremadamente Consistente"] and
        perfil["A6_MentalidadEquipo"] in ["Jugador de Equipo Nato", "Totalmente Alineado con el Equipo"]):
        bonificaciones_sinergia += 8
    #BD6
    if (perfil["A1_Experiencia"] == "Veterano" and
        perfil["A7_EncajeMarca"] == "Buen Encaje" and
        perfil["A6_MentalidadEquipo"] in ["Jugador de Equipo Nato", "Totalmente Alineado con el Equipo"]):
        bonificaciones_sinergia += 8
    #BD7
    if ((perfil["A3_VelocidadPura"] == "Excepcional" or perfil["A5_FeedbackTecnico"] == "Excepcional") and
        perfil["A8_ExigenciaSalarial"] == "Salario Medio"):
        bonificaciones_sinergia += 4
    #BD8
    if (perfil["A1_Experiencia"] == "Establecido" and
        perfil["A5_FeedbackTecnico"] == "Fuerte" and
        perfil["A6_MentalidadEquipo"] == "Jugador de Equipo Nato" and
        perfil["A8_ExigenciaSalarial"] == "Salario Medio"):
        bonificaciones_sinergia += 6
    #BD9
    if (perfil["A1_Experiencia"] == "Novato" and
        perfil["A5_FeedbackTecnico"] == "Adecuada" and
        perfil["A6_MentalidadEquipo"] == "Equilibrado" and
        perfil["A8_ExigenciaSalarial"] == "Salario Muy Bajo"):
        bonificaciones_sinergia += 5

    # --- Penalizaciones agrupadas escalonadas ---
    #INC_AVANZADA1
    penalizador_elite = 0
    if perfil["A3_VelocidadPura"] == "Excepcional": penalizador_elite += 1
    if perfil["A4_ConsistenciaCarrera"] == "Extremadamente Consistente": penalizador_elite += 1
    if perfil["A5_FeedbackTecnico"] == "Excepcional": penalizador_elite += 1
    if perfil["A7_EncajeMarca"] == "Encaje Perfecto": penalizador_elite += 1
    if perfil["A8_ExigenciaSalarial"] in ["Salario Muy Bajo", "Salario Bajo"] and penalizador_elite >= 2:
        penalizaciones += 10 + (penalizador_elite - 2) * 2
    #INC_AVANZADA2 - Penalización por "perfil incoherente"
    penalizador_incoherente = 0
    if perfil["A1_Experiencia"] in ["Establecido", "Veterano"]: penalizador_incoherente += 1
    if perfil["A5_FeedbackTecnico"] in ["Fuerte", "Excepcional"]: penalizador_incoherente += 1
    if perfil["A8_ExigenciaSalarial"] in ["Salario Muy Bajo", "Salario Bajo"]: penalizador_incoherente += 1
    if penalizador_incoherente >= 2:
        penalizaciones += 9 + (penalizador_incoherente - 2) * 2
    #INC_AVANZADA3 - Penalización por “perfil Dios”
    if BD1_aplicado and perfil["A3_VelocidadPura"] == "Excepcional" and perfil["A4_ConsistenciaCarrera"] == "Extremadamente Consistente":
        penalizaciones += 6

    aptitud_final = max(0, puntaje_base + bonificaciones_individuales + bonificaciones_sinergia - penalizaciones)
    return aptitud_final

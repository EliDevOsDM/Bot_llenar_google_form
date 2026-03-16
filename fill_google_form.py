"""
Script para llenar un formulario de Google Forms con datos aleatorios.
Formulario: Uso de Inteligencia Artificial en estudiantes universitarios
"""

import requests
import random
import time
# URL del formulario (endpoint de envío)
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfQjciqKuqg1jpbZDVI7osA01SEQd-uY5beBuQTGDT3Ax63eQ/formResponse"

# IDs de las entradas del formulario (extraídos del HTML)
ENTRY_IDS = {
    "edad": "984911518",
    "carrera": "748704243",
    "genero": "616105835",
    "horas_estudio": "947600831",
    "usa_ia": "2078444358",
    "frecuencia_ia": "1015796024",
    "veces_semana_ia": "1839243160",
    "herramientas_ia": "222086622",
    "meses_ia": "1989670008",
    "satisfaccion": "1371108494",
}

# Datos para generar respuestas aleatorias
CARRERAS = [
    "Ingeniería de Sistemas", "Medicina", "Derecho", "Administración",
    "Psicología", "Contaduría", "Economía", "Comunicación Social",
    "Ingeniería Civil", "Arquitectura", "Enfermería", "Educación",
    "Marketing", "Ingeniería Industrial", "Biología", "Química",
]

GENEROS = ["Masculino", "Femenino", "Prefiero no decirlo"]

USA_IA = ["Si", "No"]

FRECUENCIAS = [
    "Todos los días",
    "Varias veces por semana",
    "Algunas veces al mes",
    "Nunca",
]

HERRAMIENTAS = ["ChatGPT", "Gemini", "Copilot", "DeepSeek"]


def generar_datos_aleatorios():
    """Genera un conjunto de datos aleatorios para el formulario."""
    usa_ia = random.choice(USA_IA)

    # Si no usa IA, ajustar datos para consistencia
    if usa_ia == "No":
        frecuencia = "Nunca"
        veces_semana = 0
        herramienta = random.choice(HERRAMIENTAS)  # Puede haber usado antes
        meses = random.randint(0, 6)
        satisfaccion = str(random.randint(1, 3))
    else:
        frecuencia = random.choice(FRECUENCIAS)
        if frecuencia == "Todos los días":
            veces_semana = random.randint(7, 20)
        elif frecuencia == "Varias veces por semana":
            veces_semana = random.randint(3, 6)
        elif frecuencia == "Algunas veces al mes":
            veces_semana = random.randint(1, 4)
        else:
            veces_semana = 0
        herramienta = random.choice(HERRAMIENTAS)
        meses = random.randint(1, 24)
        satisfaccion = str(random.randint(1, 5))

    return {
        "entry.984911518": str(random.randint(18, 35)),  # Edad
        "entry.748704243": random.choice(CARRERAS),  # Carrera
        "entry.616105835": random.choice(GENEROS),  # Género
        "entry.947600831": str(round(random.uniform(1, 8), 1)),  # Horas estudio (puede ser decimal)
        "entry.2078444358": usa_ia,  # ¿Utilizas IA?
        "entry.1015796024": frecuencia,  # Frecuencia
        "entry.1839243160": str(veces_semana),  # Veces por semana
        "entry.222086622": herramienta,  # Herramientas
        "entry.1989670008": str(meses),  # Meses usando IA
        "entry.1371108494": satisfaccion,  # Satisfacción 1-5
        "fvv": "1",
        "partialResponse": '[null,null,"-5996844371421353134"]',
        "pageHistory": "0",
        "fbzx": "-5996844371421353134",
    }


def enviar_formulario(datos):
    """Envía los datos al formulario de Google."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://docs.google.com/forms/d/e/1FAIpQLSfQjciqKuqg1jpbZDVI7osA01SEQd-uY5beBuQTGDT3Ax63eQ/viewform",
        "Origin": "https://docs.google.com",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    try:
        response = requests.post(
            FORM_URL,
            data=datos,
            headers=headers,
            allow_redirects=False,
            timeout=10,
        )
        # Google Forms devuelve 302 al enviar correctamente
        return response.status_code in (200, 302)
    except requests.RequestException as e:
        print(f"  Error: {e}")
        return False


def main():
    NUM_ENVIOS = 12000
    print(f"Enviando {NUM_ENVIOS} respuestas al formulario...")
    print("-" * 50)

    exitosos = 0
    fallidos = 0

    for i in range(1, NUM_ENVIOS + 1):
        datos = generar_datos_aleatorios()
        print(f"[{i}/{NUM_ENVIOS}] Enviando: Edad={datos['entry.984911518']}, "
              f"Carrera={datos['entry.748704243']}, IA={datos['entry.2078444358']}...", end=" ")

        if enviar_formulario(datos):
            print("OK")
            exitosos += 1
        else:
            print("Fallo")
            fallidos += 1

        # Pequeña pausa para no saturar (1-3 segundos entre envíos)
        if i < NUM_ENVIOS:
            time.sleep(random.uniform(1, 3))

    print("-" * 50)
    print(f"Completado: {exitosos} exitosos, {fallidos} fallidos")


if __name__ == "__main__":
    main()

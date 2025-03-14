import re
from unidecode import unidecode
from datetime import datetime

def convertir_a_slug(titulo):
    """Convierte un título en un slug URL-friendly."""
    titulo = unidecode(titulo).lower()
    titulo = re.sub(r"[^a-z0-9\s-]", "", titulo)
    return re.sub(r"\s+", "-", titulo.strip())

def limpiar_texto(texto):
    """Elimina saltos de línea y múltiples espacios."""
    return re.sub(r"\s+", " ", texto.replace("\n", " ")).strip()

def capitalizer(texto):
    """Convierte la primera letra de cada palabra en mayúscula."""
    return " ".join([palabra.capitalize() for palabra in texto.split()])

def convertir_hora(hora_24):
    """Convierte una hora en formato 24 horas a 12 horas (ejemplo: 16:20 → 04:20 PM)."""
    try:
        hora_obj = datetime.strptime(hora_24, "%H:%M")
        return hora_obj.strftime("%I:%M %p").lstrip("0").lower()
    except ValueError:
        return hora_24
    
if __name__ == "__main__":
    print("main")
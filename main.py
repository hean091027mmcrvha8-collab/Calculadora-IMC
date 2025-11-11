from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

# --------------------------
# 1. INICIALIZACIÓN DE FASTAPI
# --------------------------

app = FastAPI()

# --------------------------
# 2. CONFIGURACIÓN DE CORS
# --------------------------
# Permite que tu app de Expo (frontend) se comunique con este servidor.

origins = [
    # Usaremos '*' temporalmente para desarrollo.
    "*", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------
# 3. DEFINICIÓN DE MODELOS (Pydantic)
# --------------------------

# Define el formato de los datos que se recibirán del frontend
class DatosIMC(BaseModel):
    imc: float
    clasificacion: str
    edad: int
    sexo: str
    peso: float
    estatura: int

# Define el formato de una sugerencia individual
class Sugerencia(BaseModel):
    titulo: str
    texto: str

# Define el formato completo de la respuesta del endpoint
class RespuestaSugerencias(BaseModel):
    mensaje: str
    sugerencias: List[Sugerencia]


# --------------------------
# 4. LÓGICA DE SUGERENCIAS (Datos Estáticos y Personalizados)
# --------------------------

# Sugerencias para Sobrepeso, Obesidad y Obesidad extrema
SUGERENCIAS_SOBREPESO_OBESIDAD = [
    {
        "titulo": "Alimentación Balanceada",
        "texto": "Incluye abundantes frutas, verduras, carnes magras o alternativas vegetarianas, y cereales integrales como avena, pan integral y pasta. Prioriza alimentos frescos y de temporada."
    },
    {
        "titulo": "Limitar Alimentos Procesados",
        "texto": "Evita o limita el consumo de alimentos y bebidas con alto contenido de azúcar, grasas saturadas y sal, como refrescos, jugos industrializados, pan dulce y alimentos fritos."
    },
    {
        "titulo": "Actividad Aeróbica Moderada",
        "texto": "Realiza al menos 30 minutos de actividad aeróbica de intensidad moderada la mayoría de los días de la semana (5 veces), como caminar a paso rápido, nadar o andar en bicicleta."
    },
    {
        "titulo": "Aumento Gradual de Intensidad",
        "texto": "A medida que tu resistencia y estado físico mejoran, aumenta progresivamente la duración (hasta 60 minutos) y la intensidad de tu actividad física para optimizar la quema calórica."
    },
]

# Sugerencias para Bajo Peso
SUGERENCIAS_BAJO_PESO = [
    {
        "titulo": "Nutrición Calórica y Proteína",
        "texto": "Prioriza alimentos ricos en nutrientes y calorías saludables: frutos secos, aguacate, aceites de calidad, leguminosas y lácteos enteros para promover la ganancia de peso saludable."
    },
    {
        "titulo": "Comidas Frecuentes",
        "texto": "Consume 5 a 6 comidas pequeñas al día, incluyendo refrigerios ricos en proteína (como yogur o huevos), para facilitar el consumo de calorías necesarias sin sentirse demasiado lleno."
    },
    {
        "titulo": "Entrenamiento de Fuerza",
        "texto": "Enfoca tu ejercicio en el entrenamiento con pesas o fuerza (al menos 3 veces por semana) para aumentar la masa muscular y evitar el aumento excesivo de grasa corporal."
    },
]

# Sugerencias para Peso Normal (Mantenimiento)
SUGERENCIAS_PESO_NORMAL = [
    {
        "titulo": "Balance Nutricional y Porciones",
        "texto": "Mantén tu dieta equilibrada. Asegúrate de incluir proteínas, grasas saludables y carbohidratos complejos en porciones adecuadas en cada comida."
    },
    {
        "titulo": "Ejercicio Variado",
        "texto": "Combina ejercicio cardiovascular (correr, nadar) y entrenamiento de fuerza 3-5 veces por semana para mantener la salud cardiovascular y el tono muscular."
    },
    {
        "titulo": "Hidratación y Descanso",
        "texto": "Garantiza al menos 7-8 horas de sueño de calidad y bebe suficiente agua natural (2-3 litros) durante el día para mantener tu metabolismo óptimo."
    },
]


# --------------------------
# 5. ENDPOINT (Ruta)
# --------------------------

@app.post("/api/sugerencias")
def obtener_sugerencias(datos: DatosIMC) -> RespuestaSugerencias:
    """
    Recibe los datos del IMC y devuelve un set de sugerencias basado en la clasificación.
    """
    
    clasificacion = datos.clasificacion
    fuente = "Gobierno de México en Estrategia Nacional para la Prevención y el Control del Sobrepeso, la Obesidad y la Diabetes"

    if clasificacion == "Bajo peso":
        sugerencias_finales = SUGERENCIAS_BAJO_PESO
        mensaje_final = f"Sugerencias generadas para {clasificacion}, basadas en recomendaciones de salud."
    elif clasificacion == "Peso normal":
        sugerencias_finales = SUGERENCIAS_PESO_NORMAL
        mensaje_final = f"¡Felicidades! Recomendaciones para mantener el {clasificacion} y un estilo de vida saludable."
    elif clasificacion in ["Sobrepeso", "Obesidad", "Obesidad extrema"]:
        sugerencias_finales = SUGERENCIAS_SOBREPESO_OBESIDAD
        mensaje_final = f"Sugerencias para el grupo de {clasificacion}, según el {fuente}."
    else:
        # En caso de una clasificación desconocida
        sugerencias_finales = [
            {"titulo": "Clasificación Desconocida", "texto": "Por favor, verifica los datos enviados o calcula un IMC válido."}
        ]
        mensaje_final = f"Clasificación '{clasificacion}' no reconocida. No se pudieron obtener sugerencias."


    return RespuestaSugerencias(
        mensaje=mensaje_final,
        sugerencias=sugerencias_finales
    )

# RUTA DE PRUEBA (Opcional, pero útil)
@app.get("/")
def read_root():
    return {"message": "Servidor de Sugerencias IMC Funcionando (FastAPI)"}
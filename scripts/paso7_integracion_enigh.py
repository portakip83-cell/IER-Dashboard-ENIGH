# ============================================
# PASO 7 – Integración ENIGH
# Construcción del dataset maestro
# ============================================

import os
import pandas as pd
import numpy as np

print("Librerías cargadas correctamente")

# --------------------------------------------
# 1. Definir rutas
# --------------------------------------------

BASE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "ENIGH", "2024")
)

OUTPUT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "outputs")
)

os.makedirs(OUTPUT_PATH, exist_ok=True)

print("Ruta ENIGH:", BASE_PATH)
print("Ruta outputs:", OUTPUT_PATH)

# --------------------------------------------
# 2. Cargar bases de datos
# --------------------------------------------

hogares = pd.read_csv(os.path.join(BASE_PATH, "hogares.csv"))
viviendas = pd.read_csv(os.path.join(BASE_PATH, "viviendas.csv"))
poblacion = pd.read_csv(os.path.join(BASE_PATH, "poblacion.csv"))

print("Bases cargadas correctamente")

print("Hogares:", hogares.shape)
print("Viviendas:", viviendas.shape)
print("Población:", poblacion.shape)

# --------------------------------------------
# 3. Construir estructura familiar
# --------------------------------------------

pob = poblacion[
    [
        "folioviv",
        "foliohog",
        "numren",
        "parentesco",
        "sexo",
        "edad"
    ]
].copy()

# Jefe(a) de hogar
jefes = pob[pob["parentesco"] == 101].copy()

jefes = jefes.rename(
    columns={
        "sexo": "sexo_jefe",
        "edad": "edad_jefe"
    }
)

# Variables de composición del hogar
estructura = pob.groupby(
    ["folioviv", "foliohog"]
).apply(
    lambda x: pd.Series({
        "pareja": int((x["parentesco"] == 201).any()),
        "hijos": int((x["parentesco"] == 301).any()),
        "otros_adultos": int(
            ((x["parentesco"] >= 400) & (x["edad"] >= 18)).any()
        )
    })
).reset_index()

# Unir con jefe(a)
estructura = estructura.merge(
    jefes[["folioviv", "foliohog", "sexo_jefe", "edad_jefe"]],
    on=["folioviv", "foliohog"],
    how="left"
)

# --------------------------------------------
# 4. Clasificación de estructura familiar
# --------------------------------------------

def clasificar_estructura(row):
    if row["sexo_jefe"] == 2:  # Mujer
        if row["pareja"] == 0 and row["hijos"] == 0:
            return "FA"   # Femenino unipersonal
        elif row["pareja"] == 1 and row["hijos"] == 0:
            return "FP"   # Femenino con pareja
        elif row["hijos"] == 1:
            return "FC"   # Femenino con hijos
        else:
            return "FAD"  # Femenino ampliado
    else:  # Hombre
        if row["pareja"] == 0 and row["hijos"] == 0:
            return "MA"   # Masculino unipersonal
        elif row["pareja"] == 1:
            return "MP"   # Masculino con pareja
        else:
            return "MAD"  # Masculino ampliado

estructura["estructura_familiar"] = estructura.apply(
    clasificar_estructura,
    axis=1
)

print("Distribución estructura familiar:")
print(estructura["estructura_familiar"].value_counts())

# Guardar estructura familiar
estructura_path = os.path.join(
    OUTPUT_PATH, "estructura_familiar_2024.csv"
)
estructura.to_csv(estructura_path, index=False)
print("Archivo creado:", estructura_path)

# --------------------------------------------
# 5. Integración con hogares y viviendas
# --------------------------------------------

df = estructura.merge(
    hogares,
    on=["folioviv", "foliohog"],
    how="left"
)

print("Después de unir con hogares:", df.shape)

df = df.merge(
    viviendas,
    on="folioviv",
    how="left"
)

print("Después de unir con viviendas:", df.shape)

# --------------------------------------------
# 6. Control de duplicados
# --------------------------------------------

duplicados = df.duplicated(
    subset=["folioviv", "foliohog"]
).sum()

print("Duplicados detectados:", duplicados)

# --------------------------------------------
# 7. Dataset maestro final
# --------------------------------------------

df["anio"] = 2024  # clave para panel temporal

dataset_path = os.path.join(
    OUTPUT_PATH, "dataset_maestro_enigh_2024.csv"
)

df.to_csv(dataset_path, index=False)

print("===================================")
print("Dataset maestro creado correctamente")
print("Archivo:", dataset_path)
print("Observaciones finales:", df.shape)
print("===================================")

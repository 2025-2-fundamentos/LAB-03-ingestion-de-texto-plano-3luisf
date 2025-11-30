"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel
def pregunta_01():
    import re
    import pandas as pd

    ruta = "files/input/clusters_report.txt"

    with open(ruta, "r", encoding="utf-8") as f:
        lines = f.readlines()

    filas = []
    buffer = ""
    recolectando = False

    for line in lines:
        # Detectamos el inicio de una fila: empieza con número
        if re.match(r"^\s*\d+\s+", line):
            if buffer:
                filas.append(buffer.strip())
            buffer = line.strip()
            recolectando = True
        else:
            if recolectando:
                buffer += " " + line.strip()

            # Si la línea actual termina con punto → fin del registro
            if line.strip().endswith('.'):
                recolectando = False

    if buffer:
        filas.append(buffer.strip())

    # REGEX para extraer las cuatro columnas
    pattern = r"^(\d+)\s+(\d+)\s+([\d,]+ ?%)\s+(.+)$"

    data = []
    for fila in filas:
        m = re.match(pattern, fila)
        if m:
            data.append(m.groups())

    df = pd.DataFrame(data, columns=[
        "cluster",
        "cantidad_de_palabras_clave",
        "porcentaje_de_palabras_clave",
        "principales_palabras_clave",
    ])

    # Normalizar nombres
    df.columns = [c.lower() for c in df.columns]

    # Normalizar los espacios y comas
    df['principales_palabras_clave'] = (
        df['principales_palabras_clave']
        .str.replace(r'\s+', ' ', regex=True)
        .str.replace(r'\s*,\s*', ', ', regex=True)
        .str.rstrip('.')
    )

    # Tipos
    df["cluster"] = df["cluster"].astype(int)
    df["cantidad_de_palabras_clave"] = df["cantidad_de_palabras_clave"].astype(int)
    df["porcentaje_de_palabras_clave"] = (
        df["porcentaje_de_palabras_clave"]
        .str.replace("%", "")
        .str.replace(",", ".")
        .astype(float)
    )

    return df

print(pregunta_01())
print(pregunta_01().principales_palabras_clave.to_list()[1])
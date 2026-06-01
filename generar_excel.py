import os
import pandas as pd
from datetime import datetime, timedelta

BASE_PATH = r"C:\Users\u1305913\OneDrive - Komatsu Ltd\TUTOR DE CAPACITACIÓN\CERTIFICADOS LEGALES 2026"

data = []

for trabajador in os.listdir(BASE_PATH):

    ruta_trab = os.path.join(BASE_PATH, trabajador)

    if not os.path.isdir(ruta_trab):
        continue

    for carpeta in os.listdir(ruta_trab):

        ruta_carp = os.path.join(ruta_trab, carpeta)

        if not os.path.isdir(ruta_carp):
            continue

        archivos_pdf = []

        for archivo in os.listdir(ruta_carp):

            if archivo.lower() == "vencidos":
                continue

            ruta_archivo = os.path.join(ruta_carp, archivo)

            if os.path.isfile(ruta_archivo) and archivo.lower().endswith(".pdf"):
                archivos_pdf.append((archivo, ruta_archivo))

        # ==============================
        # CFK → MUCHOS PDF SIN FECHA
        # ==============================
        if "CFK" in carpeta.upper():

            for archivo, ruta in archivos_pdf:
                data.append({
                    "TRABAJADOR": trabajador,
                    "CURSO": archivo.replace(".pdf",""),
                    "TIPO": "FORMACION",
                    "ARCHIVO": ruta,
                    "VENCIMIENTO": None
                })

        # ==============================
        # OPERACIÓN EQUIPOS → MUCHOS PDF + FECHA
        # ==============================
        if "OPERACIÓN EQUIPOS" in carpeta.upper():

            for archivo, ruta in archivos_pdf:

                fecha_venc = datetime.now() + timedelta(days=730)

                data.append({
                    "TRABAJADOR": trabajador,
                    "CURSO": archivo.replace(".pdf",""),
                    "TIPO": "OPERACIÓN_EQUIPOS",
                    "ARCHIVO": ruta,
                    "VENCIMIENTO": fecha_venc
                })

        # ==============================
        # CERTIFICADOS → 1 ARCHIVO + 1 AÑO
        # ==============================
        else:

            if len(archivos_pdf) > 0:

                archivo, ruta = archivos_pdf[0]

                fecha_venc = datetime.now() + timedelta(days=365)

                data.append({
                    "TRABAJADOR": trabajador,
                    "CURSO": carpeta,
                    "TIPO": "CERTIFICACION",
                    "ARCHIVO": ruta,
                    "VENCIMIENTO": fecha_venc
                })

# ==============================
# EXPORTAR
# ==============================
df = pd.DataFrame(data)
df.to_excel("CONTROL_TOTAL.xlsx", index=False)

print("✅ Excel generado correctamente")
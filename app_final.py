import streamlit as st
import pandas as pd
import os
import webbrowser
from datetime import datetime

st.set_page_config(layout="wide")
st.markdown("""
<style>
.stApp {
    background-color: #1B1E6D;  /* azul corporativo */
}

/* Texto más visible */
h1, h2, h3, h4, h5, h6, p, span {
    color: white !important;
}

/* Opcional: tarjetas más claras */
.block-container {
    background-color: transparent;
}
</style>
""", unsafe_allow_html=True)
col_logo, col_title = st.columns([1,5])

with col_logo:
    st.image("komatsu.png", width=120)

with col_title:
    st.title("📊 ACREDITACIONES KOMATSU RT")

ARCHIVO = "CONTROL_TOTAL.xlsx"
ARCHIVO_MATRIZ = "Certificados.xlsx"

BASE_PATH = r"C:\Users\u1305913\OneDrive - Komatsu Ltd\TUTOR DE CAPACITACIÓN\CERTIFICADOS LEGALES 2026"

# ==============================
# CARGAR MATRIZ
# ==============================
df_matriz = pd.read_excel(ARCHIVO_MATRIZ, sheet_name="MATRIZ")
df_matriz.columns = df_matriz.columns.str.strip().str.upper()
df_matriz["NOMBRE COMPLETO"] = df_matriz["NOMBRE COMPLETO"].str.strip().str.upper()

# ==============================
# CARGAR DATOS CONTROL
# ==============================
df = pd.read_excel(ARCHIVO)
df.columns = df.columns.str.upper()

# ==============================
# FUNCIONES
# ==============================
def estado(fecha):
    if pd.isna(fecha):
        return "—"
    fecha = pd.to_datetime(fecha)
    hoy = datetime.now()

    if fecha < hoy:
        return "🔴 VENCIDO"
    elif (fecha - hoy).days <= 30:
        return "🟡 POR VENCER"
    return "🟢 VIGENTE"

def dato(df, col):
    if col in df.columns and not df.empty:
        val = df[col].iloc[0]
        return val if pd.notna(val) else "Sin dato"
    return "Sin dato"

def obtener_foto(nombre):
    ruta = os.path.join(BASE_PATH, nombre)
    if os.path.exists(ruta):
        for f in os.listdir(ruta):
            if f.lower().endswith(".jpg"):
                return os.path.join(ruta, f)
    return None

# ==============================
# SELECTOR
# ==============================
trabajador = st.selectbox(
    "Seleccionar trabajador",
    sorted(df_matriz["NOMBRE COMPLETO"].unique())
)

trabajador_clean = trabajador.strip().upper()

df_persona = df_matriz[df_matriz["NOMBRE COMPLETO"] == trabajador_clean]
df_trab = df[df["TRABAJADOR"].str.upper() == trabajador_clean]

# ==============================
# 📊 RESUMEN
# ==============================
df_cert = df_trab[df_trab["TIPO"] == "CERTIFICACION"]
df_op = df_trab[df_trab["TIPO"].str.upper().str.contains("OPERACIÓN_EQUIPOS")]
df_form = df_trab[df_trab["TIPO"] == "FORMACION"]

c1, c2, c3, c4 = st.columns(4)

c1.metric("📄 Certificados", len(df_cert))
c2.metric("🚜 Operación", len(df_op))
c3.metric("🎓 Formación", len(df_form))
c4.metric("📊 Total", len(df_trab))

st.markdown("---")

# ==============================
# PERFIL
# ==============================
st.subheader("👤 Perfil del Trabajador")
st.markdown("---")

col1, col2 = st.columns([1.2, 6])
foto = obtener_foto(trabajador)

with col1:
    if foto:
        st.image(foto, width=200)

with col2:
    st.write(f"## {trabajador}")
    st.write(f"📇Rut: {dato(df_persona,'RUT')}")
    st.write(f"💼Cargo: {dato(df_persona,'CARGO')}")
    st.write(f"🏢Empresa: {dato(df_persona,'EMPRESA')}")
    st.write(f"🪪Licencia: {dato(df_persona,'LICENCIA')}")
    st.write(f"📧Correo: {dato(df_persona,'E-MAIL')}")

# ==============================
# 1. CERTIFICADOS
# ==============================
st.subheader("📄 Certificados Legales")
st.markdown("---")


# ✅ TITULOS
col1, col2, col3, col4 = st.columns([4,2,2,2])
col1.markdown("**CURSO**")
col2.markdown("**VENCIMIENTO**")
col3.markdown("**ESTADO**")
col4.markdown("**ACCIÓN**")


for i, row in df_trab[df_trab["TIPO"] == "CERTIFICACION"].iterrows():

    col1, col2, col3, col4 = st.columns([4,2,2,2])

    col1.write(row["CURSO"])
    col2.write(str(row["VENCIMIENTO"])[:10])
    col3.write(estado(row["VENCIMIENTO"]))

    if col4.button("📄 Diploma", key=f"c{i}"):
        webbrowser.open_new(row["ARCHIVO"])

# ==============================
# 2. OPERACION EQUIPO (TODOS)
# ==============================
st.subheader("🚜 Operación de Equipos")
st.markdown("---")

# ✅ TITULOS
col1, col2, col3, col4 = st.columns([4,2,2,2])
col1.markdown("**CURSO**")
col2.markdown("**VENCIMIENTO**")
col3.markdown("**ESTADO**")
col4.markdown("**ACCIÓN**")


df_op = df_trab[
    df_trab["TIPO"]
    .astype(str)
    .str.upper()
    .str.replace("Ó", "O")
    .str.contains("OPERACION", na=False)
]

for i, row in df_op.iterrows():

    col1, col2, col3, col4 = st.columns([4,2,2,2])

    fecha = pd.to_datetime(row["VENCIMIENTO"])

    col1.write(row["CURSO"])
    col2.write(fecha.strftime("%d-%m-%Y"))
    col3.write(estado(fecha))

    if col4.button("📄 Diploma", key=f"op{i}"):
        webbrowser.open_new(row["ARCHIVO"])

# ==============================
# 3. FORMACION
# ==============================
st.subheader("🎓 Formación CFK")
st.markdown("---")


# ✅ TITULOS
col1, col2, col3 = st.columns([5,2,2])
col1.markdown("**CURSO**")
col2.markdown("**ESTADO**")
col3.markdown("**ACCIÓN**")


for i, row in df_trab[df_trab["TIPO"] == "FORMACION"].iterrows():

    col1, col2, col3 = st.columns([5,2,2])

    col1.write(row["CURSO"])
    col2.write("🎓FORMACIÓN COMPLETADA")

    if col3.button("📄 Diploma", key=f"f{i}"):
        webbrowser.open_new(row["ARCHIVO"])
st.markdown("---")
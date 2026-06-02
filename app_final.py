import streamlit as st
import pandas as pd
import os
import webbrowser
import base64
from datetime import datetime

st.set_page_config(layout="wide")
# ==============================
# 🔥 LOGO BASE64
# ==============================
def cargar_logo(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = cargar_logo("komatsu.png")

# ==============================
# 🎨 ESTILOS
# ==============================
st.markdown(f"""
<style>

.stApp{{
    background:
    radial-gradient(circle at center,
    #0d2d63 0%,
    #071b3b 35%,
    #030b1c 100%);
}}

.card-pro{{
    background:
    linear-gradient(135deg,
        rgba(8,25,55,0.95),
        rgba(4,15,35,0.95)
    );
    border:2px solid #2490ff;
    border-radius:24px;
    padding:40px;
    margin-bottom:25px;

    box-shadow:
    0 0 25px rgba(36,144,255,.45),
    inset 0 0 40px rgba(36,144,255,.08);
}}

.card-title{{
    color:white;
    font-size:24px;
    font-weight:700;
    margin-bottom:25px;
}}

.nombre{{
    color:white;
    font-size:34px;
    font-weight:700;
    margin-bottom:15px;
}}

.info{{
    color:#d7e8ff;
    font-size:18px;
    margin-bottom:12px;
}}

.card-pro img{{
    border-radius:18px;
    border:2px solid #2490ff;
    box-shadow:0 0 20px rgba(36,144,255,.45);
}}

</style>

<img src="data:image/png;base64,{logo_base64}" style="position:fixed; top:80px; right:60px; width:200px; opacity:0.15;">

""", unsafe_allow_html=True)
st.markdown("""
<style>

.card{
    position: relative;
}

.card::before{
    content:"";
    position:absolute;
    top:0;
    left:0;
    width:100%;
    height:5px;

    background: linear-gradient(
        90deg,
        #00BFFF,
        #1E90FF,
        #00BFFF
    );

    border-radius:25px 25px 0 0;
}

.card:hover {
    transform: scale(1.01);

    box-shadow:
        0 0 25px #4DB2FF,
        0 0 50px rgba(77,178,255,0.8),
        0 0 80px rgba(77,178,255,0.5);
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

[data-testid="stMetric"]{
    background: rgba(8,25,55,0.95);
    border: 2px solid #2490FF;
    border-radius: 18px;
    padding: 20px;
    text-align:center;

    box-shadow:
        0 0 15px rgba(36,144,255,.4);
}

/* BOTONES */
.stButton > button{
    background:#0F3A7A;
    color:white;
    border:2px solid #2490FF;
    border-radius:12px;

    box-shadow:
        0 0 10px rgba(36,144,255,.5),
        0 0 20px rgba(36,144,255,.3);
}

</style>
""", unsafe_allow_html=True)

col_logo, col_title = st.columns([1,5])

with col_logo:
    st.image("komatsu.png", width=240)

with col_title:
    st.title("ACREDITACIONES RADOMIRO TOMIC")

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

def mostrar_pdf(pdf_file):
    with open(pdf_file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")

    pdf_display = f"""
    <iframe
        src="data:application/pdf;base64,{base64_pdf}"
        width="100%"
        height="800"
        type="application/pdf">
    </iframe>
    """

    st.markdown(pdf_display, unsafe_allow_html=True)
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
with st.container(border=True):

	df_cert = df_trab[df_trab["TIPO"] == "CERTIFICACION"]
	df_op = df_trab[df_trab["TIPO"].str.upper().str.contains("OPERACIÓN_EQUIPOS")]
	df_form = df_trab[df_trab["TIPO"] == "FORMACION"]

	c1, c2, c3, c4 = st.columns(4)

	c1.metric("📄 Certificados", len(df_cert))
	c2.metric("🚜 Operación", len(df_op))
	c3.metric("🎓 Formación", len(df_form))
	c4.metric("📊 Total", len(df_trab))

# ==============================
# PERFIL
# ==============================
with st.container(border=True):

	st.subheader("👤 Perfil del Trabajador")

with st.container(border=True):

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
with st.container(border=True):

    st.subheader("📄 Certificados Legales")

with st.container(border=True):

    col1, col2, col3, col4 = st.columns([4,2,2,2])
    col1.markdown("**CURSO**")
    col2.markdown("**VENCIMIENTO**")
    col3.markdown("**ESTADO**")
    col4.markdown("**ACCIÓN**")

with st.container(border=True):

    for i, row in df_trab[df_trab["TIPO"] == "CERTIFICACION"].iterrows():

        col1, col2, col3, col4 = st.columns([4, 2, 2, 2])

        col1.write(row["CURSO"])
        col2.write(str(row["VENCIMIENTO"])[:10])
        col3.write(estado(row["VENCIMIENTO"]))

        if col4.button("📄 Ver PDF", key=f"c{i}"):

             if os.path.exists(row["ARCHIVO"]):
                 mostrar_pdf(row["ARCHIVO"])
             else:
                 st.error("PDF no encontrado")

# ==============================
# 2. OPERACION EQUIPO (TODOS)
# ==============================
with st.container(border=True):

	st.subheader("🚜 Operación de Equipos")

with st.container(border=True):

    col1, col2, col3, col4 = st.columns([4,2,2,2])
    col1.markdown("**CURSO**")
    col2.markdown("**VENCIMIENTO**")
    col3.markdown("**ESTADO**")
    col4.markdown("**ACCIÓN**")

with st.container(border=True):

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

        if col4.button("📄 Ver PDF", key=f"c{i}"):

            if os.path.exists(row["ARCHIVO"]):
                mostrar_pdf(row["ARCHIVO"])
            else:
                st.error("PDF no encontrado")

# ==============================
# 3. FORMACION
# ==============================
with st.container(border=True):

    st.subheader("🎓 Formación CFK")

with st.container(border=True):

    col1, col2, col3 = st.columns([5,2,2])
    col1.markdown("**CURSO**")
    col2.markdown("**ESTADO**")
    col3.markdown("**ACCIÓN**")

with st.container(border=True):

    for i, row in df_trab[df_trab["TIPO"] == "FORMACION"].iterrows():

        col1, col2, col3 = st.columns([5, 2, 2])

        col1.write(row["CURSO"])
        col2.write("🎓 FORMACIÓN COMPLETADA")

        if col3.button("📄 Ver PDF", key=f"c{i}"):

            if os.path.exists(row["ARCHIVO"]):
                mostrar_pdf(row["ARCHIVO"])
            else:
                st.error("PDF no encontrado")

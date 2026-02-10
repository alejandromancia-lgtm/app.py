import streamlit as st
import os
from fpdf import FPDF
from datetime import datetime
import base64
import urllib.parse

# 1. CONFIGURACIÓN (Mantené tus datos aquí)
MI_EMPRESA = "AGM SRL"

st.set_page_config(page_title="MboyoValé", page_icon="🇵🇾")

# 2. ENCABEZADO CON LOGO
col1, col2 = st.columns([1, 3])
with col1:
    # Usamos "logo.png" que es más fácil de escribir
    if os.path.exists("logo.png"):
        st.image("logo.png", width=100)
    else:
        st.write("📌") # Un emoji temporal si no hay logo

with col2:
    st.title("MboyoValé")
    st.write(f"Gestión Profesional para **{MI_EMPRESA}**")

# ... (seguí con el resto de tu código de presupuestos)

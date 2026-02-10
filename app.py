import streamlit as st
from fpdf import FPDF
from datetime import datetime

# 1. CONFIGURACIÓN DE TU EMPRESA
MI_EMPRESA = "AGM SOLUCIONES"
MI_RUC = "80012345-6"
MI_CONTACTO = "+595 981 123 456"
MI_DIRECCION = "Asunción, Paraguay"

st.set_page_config(page_title="MboyoValé", page_icon="🇵🇾")

# Título y Logo
st.title("🇵🇾 MboyoValé")
st.write(f"Emisor: **{MI_EMPRESA}**")

# 2. ENTRADA DE DATOS
with st.expander("Datos del Cliente", expanded=True):
    cliente = st.text_input("Nombre / Razón Social del Cliente")
    ruc_cliente = st.text_input("RUC del Cliente (Opcional)")

with st.expander("Detalle del Servicio", expanded=True):
    servicio = st.text_input("Descripción del Servicio/Producto")
    col1, col2 = st.columns(2)
    with col1:
        cantidad = st.number_input("Cantidad", min_value=1, value=1)
    with col2:
        precio_unit = st.number_input("Precio Unitario (Gs.)", min_value=0, step=50000)

# 3. CÁLCULOS
subtotal = cantidad * precio_unit
iva_10 = int(subtotal / 11)

# 4. BOTÓN PARA GENERAR
if st.button("Generar Presupuesto Formal"):
    if cliente and servicio and precio_unit > 0:
        pdf = FPDF()
        pdf.add_page()
        
        # ENCABEZADO EMPRESA
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 8, MI_EMPRESA, 0, 1, "R")
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 5, f"RUC: {MI_RUC}", 0, 1, "R")
        pdf.cell(0, 5, f"Contacto: {MI_CONTACTO}", 0, 1, "R")
        pdf.cell(0, 5, MI_DIRECCION, 0, 1, "R")
        pdf.ln(10)
        
        # TÍTULO
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "PRESUPUESTO", "B", 1, "L")
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 10, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", 0, 1, "L")
        pdf.ln(5)

        # TABLA
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(90, 10, " Concepto", 1, 0, "L", True)
        pdf.cell(20, 10, "Cant

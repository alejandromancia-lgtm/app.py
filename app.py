import streamlit as st
from fpdf import FPDF
from datetime import datetime

# 1. CONFIGURACIÓN DE TU EMPRESA (Podés editar esto)
MI_EMPRESA = "AGM SOLUCIONES"
MI_RUC = "80012345-6"
MI_CONTACTO = "+595 981 123 456"

st.set_page_config(page_title="MboyoValé", page_icon="🇵🇾")

# Título y Bienvenida
st.title("🇵🇾 MboyoValé")
st.write(f"Gestión Profesional para **{MI_EMPRESA}**")

# 2. ENTRADA DE DATOS
with st.container():
    cliente = st.text_input("Nombre del Cliente")
    servicio = st.text_input("Descripción del Servicio")
    col1, col2 = st.columns(2)
    with col1:
        cantidad = st.number_input("Cantidad", min_value=1, value=1)
    with col2:
        precio_unit = st.number_input("Precio Unitario (Gs.)", min_value=0, step=10000)

# 3. CÁLCULOS AUTOMÁTICOS
subtotal = cantidad * precio_unit
iva_10 = int(subtotal / 11)

# 4. BOTÓN DE GENERACIÓN
if st.button("🚀 Generar Presupuesto PDF"):
    if cliente and servicio and precio_unit > 0:
        pdf = FPDF()
        pdf.add_page()
        
        # Encabezado Empresa
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, MI_EMPRESA, 0, 1, "R")
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 5, f"RUC: {MI_RUC}", 0, 1, "R")
        pdf.cell(0, 5, f"Tel: {MI_CONTACTO}", 0, 1, "R")
        pdf.ln(10)
        
        # Título del Documento
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "PRESUPUESTO", "B", 1, "L")
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 10, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", 0, 1, "L")
        pdf.ln(5)

        # Datos del Cliente
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 7, f"PARA: {cliente}", 0, 1)
        pdf.ln(5)
        
        # Tabla de Detalles
        pdf.set_fill_color(230, 230, 230)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(90, 10, " Concepto", 1, 0, "L", True)
        pdf.cell(20, 10, "Cant.", 1, 0, "C", True)
        pdf.cell(40, 10, "P. Unit", 1, 0, "C", True)
        pdf.cell(40, 10, "Total", 1, 1, "C", True)
        
        pdf.set_font("Arial", "", 10)
        pdf.cell(90, 10, f" {servicio[:40]}", 1)
        pdf.cell(20, 10, str(cantidad), 1, 0, "C")
        pdf.cell(40, 10, f"{precio_unit:,}", 1, 0, "R")
        pdf.cell(40, 10, f"{subtotal:,}", 1, 1, "R")
        
        # Liquidación de IVA y Total
        pdf.ln(5)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(150, 8, "IVA 10% (Incluido):", 0, 0, "R")
        pdf.cell(40, 8, f"{iva_10:,}", 0, 1, "R")
        
        pdf.set_fill_color(0, 51, 102)
        pdf.set_text_color(255)
        pdf.cell(150, 10, "TOTAL A PAGAR (Gs.):", 0, 0, "R", True)
        pdf.cell(40,

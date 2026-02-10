import streamlit as st
from fpdf import FPDF
from datetime import datetime

# 1. DATOS DE TU EMPRESA (Editables)
EMPRESA_NOMBRE = "AGM SOLUCIONES"
EMPRESA_RUC = "80012345-6"
EMPRESA_TEL = "+595 981 123 456"

st.set_page_config(page_title="MboyoValé", page_icon="🇵🇾")

# Interfaz Simple
st.title("🇵🇾 MboyoValé")
st.write(f"Panel de Presupuestos - **{EMPRESA_NOMBRE}**")

# 2. ENTRADA DE DATOS
cliente = st.text_input("Nombre del Cliente")
servicio = st.text_input("Descripción del Servicio/Producto")

col1, col2 = st.columns(2)
with col1:
    cantidad = st.number_input("Cantidad", min_value=1, value=1)
with col2:
    precio_unit = st.number_input("Precio Unitario (Gs.)", min_value=0, step=10000)

# 3. CÁLCULOS (IVA 10% Incluido)
total_general = cantidad * precio_unit
iva_diez = int(total_general / 11)

# 4. GENERACIÓN DEL PDF
if st.button("🚀 Crear Presupuesto"):
    if cliente and servicio and precio_unit > 0:
        pdf = FPDF()
        pdf.add_page()
        
        # Membrete Profesional
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, EMPRESA_NOMBRE, 0, 1, "R")
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 5, f"RUC: {EMPRESA_RUC}", 0, 1, "R")
        pdf.cell(0, 5, f"Tel: {EMPRESA_TEL}", 0, 1, "R")
        pdf.ln(10)
        
        # Título y Fecha
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "PRESUPUESTO", "B", 1, "L")
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 10, f"Fecha de emisión: {datetime.now().strftime('%d/%m/%Y')}", 0, 1, "L")
        pdf.ln(5)

        # Datos del Cliente
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 10, f"PARA: {cliente}", 0, 1)
        pdf.ln(5)
        
        # Tabla de Items
        pdf.set_fill_color(230, 230, 230)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(90, 10, " Concepto", 1, 0, "L", True)
        pdf.cell(20, 10, "Cant.", 1, 0, "C", True)
        pdf.cell(40, 10, "P. Unit", 1, 0, "C", True)
        pdf.cell(40, 10, "Subtotal", 1, 1, "C", True)
        
        # Fila de Datos
        pdf.set_font("Arial", "", 10)
        pdf.cell(90, 10, f" {servicio[:40]}", 1)
        pdf.cell(20, 10, str(cantidad), 1, 0, "C")
        pdf.cell(40, 10, f"{precio_unit:,}", 1, 0, "R")
        pdf.cell(40, 10, f"{total_general:,}", 1, 1, "R")
        
        # Totales
        pdf.ln(5)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(150, 8, "Liquidación IVA 10%:", 0, 0, "R")
        pdf.cell(40, 8, f"{iva_diez:,}", 0, 1, "R")
        
        pdf.set_fill_color(0, 51, 102) # Azul oscuro profesional
        pdf.set_text_color(255)
        pdf.cell(150, 10, "TOTAL GENERAL (Gs.):", 0, 0, "R", True)
        pdf.cell(40, 10, f"{total_general:,}", 0, 1, "R", True)
        
        # Descarga
        nombre_archivo = f"Presu_{cliente.replace(' ', '_')}.pdf"
        pdf.output(nombre_archivo)
        
        with open(nombre_archivo, "rb") as f:
            st.download_button("📥 Descargar PDF", f, file_name=nombre_archivo)
        st.success("¡Presupuesto generado con éxito!")
    else:
        st.error("Por favor, completa los campos obligatorios.")

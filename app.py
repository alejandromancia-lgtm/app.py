import streamlit as st
from fpdf import FPDF

# 1. Configuración
st.set_page_config(page_title="MboyoValé", page_icon="🇵🇾")

st.title("🇵🇾 MboyoValé")
st.write("Presupuestos profesionales con desglose de IVA.")

# 2. Formulario Simple
cliente = st.text_input("¿Para quién es?", placeholder="Nombre del cliente")
servicio = st.text_input("Servicio a ofrecer", placeholder="Ej: Instalación de Aire")
col1, col2 = st.columns(2)
with col1:
    cantidad = st.number_input("Cantidad", min_value=1, step=1, value=1)
with col2:
    precio_unit = st.number_input("Precio Unitario (Gs.)", min_value=0, step=50000)

# 3. Cálculos
subtotal = cantidad * precio_unit
iva_incluido = int(subtotal / 11) # Cálculo estándar PY para IVA 10%

if st.button("Generar Presupuesto con IVA"):
    if cliente and servicio and precio_unit > 0:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "PRESUPUESTO PROFESIONAL", 0, 1, "C")
        pdf.ln(10)
        
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Cliente: {cliente}", 0, 1)
        pdf.ln(5)
        
        # Tabla de conceptos
        pdf.set_font("Arial", "B", 10)
        pdf.cell(100, 10, "Concepto", 1)
        pdf.cell(20, 10, "Cant.", 1, 0, "C")
        pdf.cell(30, 10, "P. Unit", 1, 0, "C")
        pdf.cell(40, 10, "Subtotal", 1, 1, "C")
        
        pdf.set_font("Arial", "", 10)
        pdf.cell(100, 10, servicio[:45], 1)
        pdf.cell(20, 10, str(cantidad), 1, 0, "C")
        pdf.cell(30, 10, f"{precio_unit:,}", 1, 0, "R")
        pdf.cell(40, 10, f"{subtotal:,}", 1, 1, "R")
        
        pdf.ln(5)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(150, 10, "Liquidacion del IVA (10%):", 0, 0, "R")
        pdf.cell(40, 10, f"Gs. {iva_incluido:,}", 0, 1, "R")
        pdf.cell(150, 10, "TOTAL A PAGAR (Gs.):", 0, 0, "R")
        pdf.cell(40, 10, f"Gs. {subtotal:,}", 0, 1, "R")
        
        pdf_name = f"Presu_{cliente}.pdf"
        pdf.output(pdf_name)
        
        with open(pdf_name, "rb") as f:
            st.download_button("📥 Descargar Presupuesto", f, file_name=pdf_name)
        st.success("¡Presupuesto listo con desglose legal!")
    else:
        st.error("Por favor, completa todos los campos.")

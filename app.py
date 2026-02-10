import streamlit as st
from fpdf import FPDF
from datetime import datetime
import base64
import urllib.parse
import os

# 1. CONFIGURACIÓN DE TU EMPRESA
MI_EMPRESA = "AGM SRL"
MI_RUC = "80012345-6"
MI_CONTACTO = "+595 981 123 456"
MI_DIRECCION = "Asunción, Paraguay"

st.set_page_config(page_title="MboyoValé", page_icon="🇵🇾")

# 2. ENCABEZADO CON LOGO Y TÍTULO
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    if os.path.exists("logo_agm.png"):
        st.image("logo_agm.png", width=100)
    else:
        st.write("📌") 

with col_titulo:
    st.title("MboyoValé")
    st.write(f"Gestión Profesional para **{MI_EMPRESA}**")

# 3. FORMULARIO DE CARGA (Esto es lo que faltaba)
st.write("---")
with st.container():
    tel_cliente = st.text_input("WhatsApp del Cliente (ej: 595981...)", placeholder="5959xxxxxxxx")
    cliente = st.text_input("Nombre o Razón Social del Cliente")
    servicio = st.text_input("Descripción del Servicio o Producto")
    
    c1, c2 = st.columns(2)
    with c1:
        cantidad = st.number_input("Cantidad", min_value=1, value=1)
    with c2:
        precio_unit = st.number_input("Precio Unitario (Gs.)", min_value=0, step=50000)

# 4. CÁLCULOS
total_general = cantidad * precio_unit
iva_diez = int(total_general / 11)

# 5. GENERACIÓN DE PDF Y WHATSAPP
if st.button("🚀 Generar Presupuesto y Link"):
    if cliente and servicio and precio_unit > 0 and tel_cliente:
        # Crear PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Membrete AGM
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, MI_EMPRESA, 0, 1, "R")
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 5, f"RUC: {MI_RUC}", 0, 1, "R")
        pdf.cell(0, 5, f"Contacto: {MI_CONTACTO}", 0, 1, "R")
        pdf.ln(10)
        
        # Título Presupuesto
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "PRESUPUESTO", "B", 1, "L")
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 10, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", 0, 1, "L")
        pdf.cell(0, 10, f"Para: {cliente}", 0, 1)
        pdf.ln(5)

        # Tabla de Items
        pdf.set_fill_color(230, 230, 230)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(100, 10, " Concepto", 1, 0, "L", True)
        pdf.cell(20, 10, "Cant.", 1, 0, "C", True)
        pdf.cell(40, 10, "Subtotal", 1, 1, "C", True)
        
        pdf.set_font("Arial", "", 10)
        pdf.cell(100, 10, f" {servicio[:45]}", 1)
        pdf.cell(20, 10, str(cantidad), 1, 0, "C")
        pdf.cell(40, 10, f"{total_general:,}", 1, 1, "R")
        
        # Totales con IVA
        pdf.ln(5)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(120, 8, "Liquidacion IVA 10%:", 0, 0, "R")
        pdf.cell(40, 8, f"{iva_diez:,}", 0, 1, "R")
        pdf.set_fill_color(30, 70, 140)
        pdf.set_text_color(255)
        pdf.cell(120, 10, "TOTAL GENERAL (Gs.):", 0, 0, "R", True)
        pdf.cell(40, 10, f"{total_general:,}", 0, 1, "R", True)

        # Generar link de descarga
        pdf_output = pdf.output(dest='S').encode('latin-1')
        pdf_base64 = base64.b64encode(pdf_output).decode('utf-8')
        link_pdf = f"data:application/pdf;base64,{pdf_base64}"

        # Preparar WhatsApp
        msg = f"Hola {cliente}, adjunto presupuesto de {MI_EMPRESA}. Total: Gs. {total_general:,}. Bajar aqui: {link_pdf}"
        msg_url = f"https://wa.me/{tel_cliente}?text={urllib.parse.quote(msg)}"

        st.success("¡Presupuesto generado!")
        
        # Botones de Acción
        st.markdown(f'<a href="{msg_url}" target="_blank" style="text-decoration: none;"><div style="background-color: #25D366; color: white; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold;">🟢 Enviar por WhatsApp</div></a>', unsafe_allow_html=True)
        st.download_button("📥 Descargar PDF para archivo", pdf_output, file_name=f"Presu_{cliente}.pdf")
    else:
        st.error("Por favor, completa todos los campos para generar el documento.")

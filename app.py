import streamlit as st
from fpdf import FPDF
from datetime import datetime
import base64
import urllib.parse

# 1. CONFIGURACIÓN DE TU EMPRESA
EMPRESA_NOMBRE = "AGM SOLUCIONES"
EMPRESA_RUC = "80012345-6"
EMPRESA_TEL = "+595 981 123 456"

st.set_page_config(page_title="MboyoValé", page_icon="🇵🇾")

st.title("🇵🇾 MboyoValé")
st.write(f"Gestión de Ventas para **{EMPRESA_NOMBRE}**")

# 2. ENTRADA DE DATOS
with st.container():
    tel_cliente = st.text_input("WhatsApp del Cliente (ej: 595981...)", placeholder="5959xxxxxxxx")
    cliente = st.text_input("Nombre del Cliente")
    servicio = st.text_input("Descripción del Servicio/Producto")
    
    col1, col2 = st.columns(2)
    with col1:
        cantidad = st.number_input("Cantidad", min_value=1, value=1)
    with col2:
        precio_unit = st.number_input("Precio Unitario (Gs.)", min_value=0, step=10000)

# 3. CÁLCULOS
total_general = cantidad * precio_unit
iva_diez = int(total_general / 11)

# 4. FUNCIÓN PARA EL LINK
def crear_link_pdf(pdf_obj):
    pdf_base64 = base64.b64encode(pdf_obj).decode('utf-8')
    return f"data:application/pdf;base64,{pdf_base64}"

# 5. GENERACIÓN Y ENVÍO
if st.button("🚀 Generar y Preparar WhatsApp"):
    if cliente and servicio and precio_unit > 0 and tel_cliente:
        # Crear PDF en memoria
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, EMPRESA_NOMBRE, 0, 1, "R")
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 5, f"RUC: {EMPRESA_RUC} | Tel: {EMPRESA_TEL}", 0, 1, "R")
        pdf.ln(10)
        
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "PRESUPUESTO", "B", 1, "L")
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 10, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", 0, 1, "L")
        pdf.cell(0, 10, f"Para: {cliente}", 0, 1)
        
        # Tabla simple
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(100, 10, " Concepto", 1, 0, "L", True)
        pdf.cell(20, 10, "Cant.", 1, 0, "C", True)
        pdf.cell(40, 10, "Total", 1, 1, "C", True)
        pdf.cell(100, 10, f" {servicio[:45]}", 1)
        pdf.cell(20, 10, str(cantidad), 1, 0, "C")
        pdf.cell(40, 10, f"{total_general:,}", 1, 1, "R")
        
        pdf.ln(5)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(120, 10, "TOTAL GENERAL (Gs.):", 0, 0, "R")
        pdf.cell(40, 10, f"{total_general:,}", 0, 1, "R")

        pdf_output = pdf.output(dest='S').encode('latin-1')
        link_pdf = crear_link_pdf(pdf_output)

        # CREAR MENSAJE PARA WHATSAPP
        mensaje = f"¡Hola {cliente}! Te saluda {EMPRESA_NOMBRE}. Adjunto el presupuesto por {servicio}. Total: Gs. {total_general:,}. Podes bajar tu PDF acá: {link_pdf}"
        mensaje_encoded = urllib.parse.quote(mensaje)
        whatsapp_url = f"https://wa.me/{tel_cliente}?text={mensaje_encoded}"

        st.success("¡Presupuesto listo!")
        
        # BOTONES FINALES
        st.markdown(f'''
            <a href="{whatsapp_url}" target="_blank">
                <button style="background-color: #25D366; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px;">
                    🟢 Enviar por WhatsApp al Cliente
                </button>
            </a>
        ''', unsafe_allow_whitespace=True, unsafe_allow_html=True)
        
        st.download_button("📥 Descargar copia PDF", pdf_output, file_name=f"Presu_{cliente}.pdf")
    else:
        st.error("Por favor, completa todos los campos (incluyendo el celular del cliente).")

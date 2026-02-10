import streamlit as st
from fpdf import FPDF
from datetime import datetime
import base64

# 1. DATOS DE TU EMPRESA
EMPRESA_NOMBRE = "AGM SRL"
EMPRESA_RUC = "80085750-0"
EMPRESA_TEL = "+595 981 925 071"

st.set_page_config(page_title="MboyoValé", page_icon="🇵🇾")

st.title("🇵🇾 MboyoValé")
st.write(f"Generador de Enlaces para **{EMPRESA_NOMBRE}**")

# 2. ENTRADA DE DATOS
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

# 4. FUNCIÓN PARA CREAR EL LINK DE DESCARGA
def crear_link_descarga(pdf_obj, nombre_archivo):
    pdf_base64 = base64.b64encode(pdf_obj).decode('utf-8')
    # Este es el link "mágico" que se puede compartir
    href = f"data:application/pdf;base64,{pdf_base64}"
    return href

# 5. GENERACIÓN
if st.button("🚀 Generar Presupuesto y Link"):
    if cliente and servicio and precio_unit > 0:
        pdf = FPDF()
        pdf.add_page()
        
        # Diseño del PDF (Membrete y Datos)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, EMPRESA_NOMBRE, 0, 1, "R")
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 5, f"RUC: {EMPRESA_RUC}", 0, 1, "R")
        pdf.cell(0, 5, f"Tel: {EMPRESA_TEL}", 0, 1, "R")
        pdf.ln(10)
        
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "PRESUPUESTO", "B", 1, "L")
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 10, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", 0, 1, "L")
        pdf.ln(5)
        pdf.cell(0, 10, f"PARA: {cliente}", 0, 1)
        
        # Detalle
        pdf.set_fill_color(230, 230, 230)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(100, 10, " Concepto", 1, 0, "L", True)
        pdf.cell(20, 10, "Cant.", 1, 0, "C", True)
        pdf.cell(40, 10, "Subtotal", 1, 1, "C", True)
        
        pdf.set_font("Arial", "", 10)
        pdf.cell(100, 10, f" {servicio[:45]}", 1)
        pdf.cell(20, 10, str(cantidad), 1, 0, "C")
        pdf.cell(40, 10, f"{total_general:,}", 1, 1, "R")
        
        # Totales
        pdf.ln(5)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(120, 8, "IVA 10%:", 0, 0, "R")
        pdf.cell(40, 8, f"{iva_diez:,}", 0, 1, "R")
        pdf.cell(120, 10, "TOTAL GENERAL (Gs.):", 0, 0, "R")
        pdf.cell(40, 10, f"{total_general:,}", 0, 1, "R")
        
        # Generar el PDF en memoria
        pdf_output = pdf.output(dest='S').encode('latin-1')
        bin_link = crear_link_descarga(pdf_output, "presupuesto.pdf")
        
        # MOSTRAR LINK AL USUARIO
        st.success("¡Presupuesto generado con éxito!")
        
        st.markdown(f"""
            ### 🔗 Enlace de descarga para el cliente:
            Copiá este link y envialo por WhatsApp:
            
            [CLIC AQUÍ PARA DESCARGAR EL PDF]({bin_link})
        """)
        
        # Botón de respaldo
        st.download_button("📥 O descargar directamente aquí", pdf_output, file_name=f"Presu_{cliente}.pdf")

    else:
        st.error("Por favor, completa los campos obligatorios.")

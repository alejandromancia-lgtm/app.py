import streamlit as st
from fpdf import FPDF

# 1. Configuración de la página
st.set_page_config(page_title="MboyoValé", page_icon="🇵🇾")

# 2. Encabezado con Logo y Título
st.title("🇵🇾 MboyoValé")
st.image("https://raw.githubusercontent.com/alejandromancia-lgtm/app.py/main/logo_pro.png", width=200)
st.write("Presupuestos rápidos para profesionales valé.")

# 3. Formulario simple
with st.container():
    cliente = st.text_input("¿Para quién es el presupuesto?")
    monto = st.number_input("Monto total (Gs.)", min_value=0, step=50000)

if st.button("Generar PDF Profesional"):
    if cliente and monto > 0:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "MBOYOVALÉ - PRESUPUESTO", 0, 1, "C")
        pdf.ln(10)
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Cliente: {cliente}", 0, 1)
        pdf.cell(0, 10, f"Monto Total: Gs. {monto:,}", 0, 1)
        pdf.ln(20)
        pdf.set_font("Arial", "I", 10)
        pdf.cell(0, 10, "Gracias por su confianza.", 0, 1, "C")
        
        pdf_name = f"Presu_{cliente}.pdf"
        pdf.output(pdf_name)
        
        with open(pdf_name, "rb") as f:
            st.download_button("📥 Descargar Presupuesto", f, file_name=pdf_name)
        st.success("¡Documento listo!")
    else:
        st.error("Por favor, completa el nombre y el monto.")

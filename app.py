import streamlit as st
from fpdf import FPDF

# Configuración básica
st.set_page_config(page_title="MboyoValé", page_icon="🇵🇾")

st.title("🇵🇾 MboyoValé")
st.subheader("Presupuestos rápidos y profesionales")

# Entradas del usuario
cliente = st.text_input("Nombre del Cliente")
detalle = st.text_area("Descripción del trabajo")
monto = st.number_input("Monto total (Gs.)", min_value=0, step=10000)

if st.button("Generar Presupuesto"):
    if cliente and detalle and monto:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "PRESUPUESTO", 0, 1, "C")
        pdf.ln(10)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, f"Cliente: {cliente}\nDetalle: {detalle}\nTotal: Gs. {monto:,}")
        
        pdf_file = "presupuesto.pdf"
        pdf.output(pdf_file)
        
        with open(pdf_file, "rb") as f:
            st.download_button("📥 Descargar PDF", f, file_name=f"Presu_{cliente}.pdf")
    else:
        st.warning("Por favor completa los datos.")

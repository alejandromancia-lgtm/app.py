import streamlit as st
from fpdf import FPDF

st.title("🇵🇾 MboyoValé")
st.image("http://googleusercontent.com/image_collection/image_retrieval/8861008225319494113_0", width=200)
st.write("Presupuestos rápidos para profesionales valé.")

cliente = st.text_input("¿Para quién es?")
monto = st.number_input("Monto (Gs.)", min_value=0)

if st.button("Generar PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"PRESUPUESTO: {cliente}", 0, 1)
    pdf.cell(0, 10, f"TOTAL: Gs. {monto:,}", 0, 1)
    pdf.output("presu.pdf")
    with open("presu.pdf", "rb") as f:
        st.download_button("📥 Descargar", f, file_name="presupuesto.pdf")

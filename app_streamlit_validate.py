import streamlit as st
import requests

st.set_page_config(page_title="Validador de Certificados - IADados", page_icon="🎓", layout="centered")

st.title("🎓 Validador de Certificados")
st.markdown("Digite o **código do certificado** (ex: `ABC123`) ou use o QRCode.")

cert_id = st.text_input("Código do certificado")

if st.button("Validar"):
    if not cert_id:
        st.warning("Digite o código antes de validar.")
        st.stop()
    
    try:
        url = f"http://127.0.0.1:8000/validate?id={cert_id}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            st.success(f"✅ Certificado Válido!")
            st.write(f"**Nome:** {data['nome']}")
            st.write(f"**Curso:** {data['curso']}")
            st.write(f"**Status:** {data['status'].capitalize()}")
        else:
            st.error("❌ Certificado inválido ou não encontrado.")
    except Exception as e:
        st.error(f"Erro na validação: {e}")

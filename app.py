import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np

# Configuração visual do site
st.set_page_config(page_title="Vete-IA: Detecção Leucocitária", layout="wide")

st.title("🔬 Sistema Inteligente de Triagem de Neutrófilos")
st.sidebar.info("Projeto de TCC - Medicina Veterinária (São Judas)")

# 1. Carregar o melhor modelo (V3)
@st.cache_resource
def load_model():
    return YOLO("best.pt")

model = load_model()

# 2. Interface de Upload
st.sidebar.header("Configurações")
conf_threshold = st.sidebar.slider("Confiança Mínima", 0.0, 1.0, 0.30)

file = st.file_uploader("Suba a foto do esfregaço sanguíneo", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    
    # Rodar a Inteligência Artificial
    results = model.predict(img, conf=conf_threshold)
    res_plotted = results[0].plot() # Imagem com os quadrados
    
    # Mostrar lado a lado
    col1, col2 = st.columns(2)
    with col1:
        st.image(img, caption="Imagem Original", use_container_width=True)
    with col2:
        st.image(res_plotted, caption="Análise da IA", use_container_width=True)
        
    # 3. Relatório de Contagem
    st.divider()
    st.subheader("📊 Relatório Automático")
    detecoes = results[0].boxes.cls.tolist()
    nomes = model.names
    
    if detecoes:
        for classe_idx in set(detecoes):
            nome = nomes[int(classe_idx)]
            qtd = detecoes.count(classe_idx)
            st.write(f"✅ **{nome}:** {qtd} encontrada(s)")
    else:
        st.warning("Nenhuma célula detectada. Tente baixar o slider de confiança.")
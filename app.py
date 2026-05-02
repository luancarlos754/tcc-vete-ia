import streamlit as st
from ultralytics import YOLO
from PIL import Image


st.set_page_config(
    page_title="Vete-IA | Triagem Leucocitária",
    page_icon="🔬",
    layout="wide",
)


st.markdown(
    """
    <style>
        :root {
            --vete-primary: #155e75;
            --vete-accent: #16a34a;
            --vete-ink: #102a43;
            --vete-muted: #627d98;
            --vete-soft: #eef8f6;
            --vete-line: #d9e8e5;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(22, 163, 74, 0.14), transparent 28rem),
                linear-gradient(180deg, #f7fbfb 0%, #eef6f5 46%, #ffffff 100%);
            color: var(--vete-ink);
        }

        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid var(--vete-line);
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: var(--vete-primary);
        }

        .main .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .hero {
            border: 1px solid rgba(21, 94, 117, 0.14);
            border-radius: 8px;
            background:
                linear-gradient(135deg, rgba(21, 94, 117, 0.96), rgba(12, 74, 110, 0.9)),
                linear-gradient(45deg, rgba(22, 163, 74, 0.18), transparent);
            color: #ffffff;
            padding: 2.3rem;
            box-shadow: 0 18px 42px rgba(15, 76, 92, 0.14);
        }

        .hero-label {
            width: fit-content;
            border: 1px solid rgba(255, 255, 255, 0.34);
            border-radius: 999px;
            padding: 0.35rem 0.75rem;
            margin-bottom: 1rem;
            color: #d8fff0;
            font-size: 0.83rem;
            font-weight: 700;
            letter-spacing: 0;
            text-transform: uppercase;
        }

        .hero h1 {
            max-width: 780px;
            margin: 0 0 0.85rem;
            color: #ffffff;
            font-size: clamp(2rem, 4vw, 3.65rem);
            line-height: 1.03;
            letter-spacing: 0;
        }

        .hero p {
            max-width: 780px;
            margin: 0;
            color: #d8eef0;
            font-size: 1.05rem;
            line-height: 1.7;
        }

        .metric-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1rem;
            margin: 1.2rem 0 1.6rem;
        }

        .metric-card,
        .upload-card,
        .result-card {
            border: 1px solid var(--vete-line);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.88);
            padding: 1rem;
            box-shadow: 0 10px 28px rgba(15, 76, 92, 0.08);
        }

        .metric-card strong {
            display: block;
            color: var(--vete-primary);
            font-size: 1.45rem;
            line-height: 1.15;
        }

        .metric-card span {
            display: block;
            margin-top: 0.35rem;
            color: var(--vete-muted);
            font-size: 0.93rem;
        }

        .section-title {
            margin: 0.25rem 0 0.55rem;
            color: var(--vete-primary);
            font-size: 1.45rem;
            font-weight: 800;
            letter-spacing: 0;
        }

        .section-copy {
            margin: 0 0 1rem;
            color: var(--vete-muted);
            line-height: 1.65;
        }

        .result-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            border-radius: 999px;
            background: var(--vete-soft);
            color: var(--vete-primary);
            padding: 0.35rem 0.75rem;
            font-weight: 700;
            margin: 0.2rem 0.35rem 0.2rem 0;
        }

        .creator {
            border-top: 1px solid var(--vete-line);
            margin-top: 1rem;
            padding-top: 1rem;
            color: var(--vete-muted);
            font-size: 0.92rem;
        }

        div[data-testid="stFileUploader"] {
            border: 1px dashed rgba(21, 94, 117, 0.35);
            border-radius: 8px;
            background: #ffffff;
            padding: 0.6rem;
        }

        .stButton button,
        [data-testid="stFileUploaderDropzone"] button {
            border-radius: 8px;
            border-color: var(--vete-primary);
            color: var(--vete-primary);
        }

        @media (max-width: 780px) {
            .hero {
                padding: 1.45rem;
            }

            .metric-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


with st.sidebar:
    st.markdown("## Vete-IA")
    st.caption("Projeto de TCC em Medicina Veterinária")
    st.divider()
    st.markdown("### Configurações da análise")
    conf_threshold = st.slider("Confiança mínima", 0.0, 1.0, 0.30, 0.05)
    st.caption(
        "Ajuste a sensibilidade do modelo. Valores menores mostram mais achados; "
        "valores maiores priorizam detecções mais confiáveis."
    )
    st.markdown(
        """
        <div class="creator">
            Criado por<br>
            <strong>Luan Carlos Verteiro Pereira</strong><br>
            Universidade São Judas
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <section class="hero">
        <div class="hero-label">Triagem assistida por inteligência artificial</div>
        <h1>Sistema Inteligente de Triagem de Neutrófilos</h1>
        <p>
            Envie uma imagem de esfregaço sanguíneo e receba uma análise visual com
            marcações automáticas para apoiar a contagem e a triagem leucocitária.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="metric-grid">
        <div class="metric-card">
            <strong>YOLO</strong>
            <span>Modelo treinado para detecção em imagens microscópicas.</span>
        </div>
        <div class="metric-card">
            <strong>Upload rápido</strong>
            <span>Compatível com arquivos JPG, JPEG e PNG.</span>
        </div>
        <div class="metric-card">
            <strong>Relatório</strong>
            <span>Resumo automático das classes encontradas na imagem.</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_model():
    return YOLO("best.pt")


model = load_model()

st.markdown('<div class="upload-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Enviar imagem para análise</div>', unsafe_allow_html=True)
st.markdown(
    '<p class="section-copy">Use uma foto nítida do campo microscópico para obter uma marcação mais precisa.</p>',
    unsafe_allow_html=True,
)
file = st.file_uploader(
    "Selecione a foto do esfregaço sanguíneo",
    type=["jpg", "png", "jpeg"],
    label_visibility="collapsed",
)
st.markdown("</div>", unsafe_allow_html=True)


if file:
    img = Image.open(file)

    with st.spinner("Analisando a imagem com o modelo..."):
        results = model.predict(img, conf=conf_threshold)
        res_plotted = results[0].plot()

    st.divider()
    st.markdown('<div class="section-title">Resultado da análise</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.image(img, caption="Imagem original", use_container_width=True)
    with col2:
        st.image(res_plotted, caption="Imagem analisada pela IA", use_container_width=True)

    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Relatório automático</div>', unsafe_allow_html=True)

    detections = results[0].boxes.cls.tolist()
    names = model.names

    if detections:
        for class_idx in sorted(set(detections)):
            name = names[int(class_idx)]
            quantity = detections.count(class_idx)
            st.markdown(
                f'<span class="result-pill">{name}: {quantity} encontrada(s)</span>',
                unsafe_allow_html=True,
            )
    else:
        st.warning("Nenhuma célula detectada. Tente reduzir a confiança mínima na barra lateral.")

    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Envie uma imagem para iniciar a análise.")
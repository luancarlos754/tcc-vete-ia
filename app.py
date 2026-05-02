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
                radial-gradient(circle at 9% 14%, rgba(124, 58, 237, 0.13) 0 3.4rem, transparent 3.5rem),
                radial-gradient(circle at 82% 12%, rgba(21, 94, 117, 0.12) 0 4.5rem, transparent 4.6rem),
                radial-gradient(circle at 92% 72%, rgba(22, 163, 74, 0.10) 0 5rem, transparent 5.1rem),
                radial-gradient(circle at top left, rgba(22, 163, 74, 0.14), transparent 28rem),
                linear-gradient(180deg, #f7fbfb 0%, #eef6f5 46%, #ffffff 100%);
            color: var(--vete-ink);
        }

        .brand-lockup {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            margin-bottom: 1rem;
        }

        .brand-mark {
            position: relative;
            width: 3.15rem;
            height: 3.15rem;
            flex: 0 0 auto;
            border-radius: 50%;
            background:
                radial-gradient(circle at 50% 50%, #ffffff 0 18%, transparent 19%),
                radial-gradient(circle at 34% 33%, #f0abfc 0 11%, transparent 12%),
                radial-gradient(circle at 66% 35%, #a7f3d0 0 10%, transparent 11%),
                radial-gradient(circle at 45% 68%, #bae6fd 0 12%, transparent 13%),
                linear-gradient(135deg, #155e75, #16a34a);
            box-shadow: 0 12px 24px rgba(21, 94, 117, 0.22);
        }

        .brand-mark::after {
            content: "";
            position: absolute;
            inset: -0.28rem;
            border: 2px solid rgba(22, 163, 74, 0.22);
            border-radius: 50%;
        }

        .brand-text strong {
            display: block;
            color: var(--vete-primary);
            font-size: 1.25rem;
            line-height: 1.1;
        }

        .brand-text span {
            display: block;
            color: var(--vete-muted);
            font-size: 0.86rem;
            margin-top: 0.15rem;
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
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(21, 94, 117, 0.14);
            border-radius: 8px;
            background:
                linear-gradient(135deg, rgba(21, 94, 117, 0.96), rgba(12, 74, 110, 0.9)),
                linear-gradient(45deg, rgba(22, 163, 74, 0.18), transparent);
            color: #ffffff;
            padding: 2.3rem;
            box-shadow: 0 18px 42px rgba(15, 76, 92, 0.14);
        }

        .hero::before,
        .hero::after {
            content: "";
            position: absolute;
            pointer-events: none;
            border-radius: 50%;
        }

        .hero::before {
            width: 20rem;
            height: 20rem;
            right: -5rem;
            top: -5.5rem;
            background:
                radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.46) 0 10%, transparent 11%),
                radial-gradient(circle at 35% 35%, rgba(216, 180, 254, 0.55) 0 10%, transparent 11%),
                radial-gradient(circle at 65% 36%, rgba(167, 243, 208, 0.48) 0 9%, transparent 10%),
                radial-gradient(circle at 45% 67%, rgba(186, 230, 253, 0.50) 0 11%, transparent 12%),
                radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.14) 0 42%, transparent 43%);
            opacity: 0.95;
        }

        .hero::after {
            width: 9rem;
            height: 9rem;
            right: 11rem;
            bottom: -3.7rem;
            background:
                radial-gradient(circle at 48% 50%, rgba(255, 255, 255, 0.5) 0 12%, transparent 13%),
                radial-gradient(circle at 34% 38%, rgba(240, 171, 252, 0.5) 0 13%, transparent 14%),
                radial-gradient(circle at 63% 61%, rgba(167, 243, 208, 0.48) 0 12%, transparent 13%),
                radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.12) 0 44%, transparent 45%);
        }

        .hero .brand-lockup,
        .hero-label,
        .hero h1,
        .hero p {
            position: relative;
            z-index: 1;
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
    st.markdown(
        """
        <div class="brand-lockup">
            <div class="brand-mark"></div>
            <div class="brand-text">
                <strong>Vete-IA</strong>
                <span>Triagem leucocitária</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
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
        <div class="brand-lockup">
            <div class="brand-mark"></div>
            <div class="brand-text">
                <strong style="color: #ffffff;">Vete-IA</strong>
                <span style="color: #c7f9e6;">Análise microscópica assistida</span>
            </div>
        </div>
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
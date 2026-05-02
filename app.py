import streamlit as st
from ultralytics import YOLO
from PIL import Image


st.set_page_config(
    page_title="Vet-IA | Triagem Leucocitária",
    page_icon="🔬",
    layout="wide",
)


st.markdown(
    """
    <style>
        :root {
            --vet-bg: #07040d;
            --vet-bg-2: #12081f;
            --vet-purple: #820ad1;
            --vet-purple-2: #b15cff;
            --vet-mint: #20e3b2;
            --vet-ink: #17111f;
            --vet-muted: #756a81;
            --vet-line: #eadff4;
            --vet-panel: #ffffff;
            --vet-soft: #f8f3fc;
        }

        .stApp {
            background:
                linear-gradient(180deg, var(--vet-bg) 0 30rem, #f8f4fb 30rem 100%);
            color: var(--vet-ink);
        }

        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background:
                repeating-linear-gradient(90deg, rgba(255,255,255,0.045) 0 1px, transparent 1px 72px),
                repeating-linear-gradient(0deg, rgba(255,255,255,0.035) 0 1px, transparent 1px 72px);
            mask-image: linear-gradient(180deg, #000 0, transparent 31rem);
        }

        .main .block-container {
            max-width: 1180px;
            padding-top: 1.7rem;
            padding-bottom: 3rem;
        }

        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid var(--vet-line);
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: var(--vet-ink);
        }

        .brand-lockup {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            margin-bottom: 1rem;
        }

        .brand-mark {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 3rem;
            height: 3rem;
            flex: 0 0 auto;
            border: 1px solid rgba(255,255,255,0.16);
            border-radius: 8px;
            background: linear-gradient(135deg, var(--vet-purple), #4d1475);
            color: #ffffff;
            box-shadow: 0 16px 36px rgba(130, 10, 209, 0.26);
            font-weight: 900;
            letter-spacing: 0;
        }

        .brand-text strong {
            display: block;
            color: var(--vet-ink);
            font-size: 1.26rem;
            line-height: 1.1;
        }

        .brand-text span {
            display: block;
            color: var(--vet-muted);
            font-size: 0.9rem;
            margin-top: 0.15rem;
        }

        .hero {
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 8px;
            background:
                linear-gradient(135deg, rgba(255,255,255,0.10), rgba(255,255,255,0.035)),
                linear-gradient(135deg, rgba(130,10,209,0.34), transparent 58%);
            padding: 2rem;
            box-shadow: 0 30px 70px rgba(0, 0, 0, 0.24);
            backdrop-filter: blur(12px);
        }

        .hero-grid {
            display: grid;
            grid-template-columns: minmax(0, 1.18fr) minmax(300px, 0.82fr);
            gap: 2rem;
            align-items: stretch;
        }

        .hero .brand-text strong,
        .hero h1 {
            color: #ffffff;
        }

        .hero .brand-text span,
        .hero p {
            color: rgba(255, 255, 255, 0.72);
        }

        .hero-label {
            width: fit-content;
            border: 1px solid rgba(255,255,255,0.18);
            border-radius: 999px;
            background: rgba(255,255,255,0.08);
            color: #ffffff;
            padding: 0.38rem 0.78rem;
            margin: 0.1rem 0 1rem;
            font-size: 0.8rem;
            font-weight: 800;
            letter-spacing: 0;
            text-transform: uppercase;
        }

        .hero h1 {
            max-width: 760px;
            margin: 0 0 0.9rem;
            font-size: clamp(2.35rem, 5vw, 4.6rem);
            line-height: 0.98;
            letter-spacing: 0;
        }

        .hero p {
            max-width: 680px;
            margin: 0;
            font-size: 1.05rem;
            line-height: 1.65;
        }

        .hero-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            margin-top: 1.4rem;
        }

        .hero-chip {
            display: inline-flex;
            align-items: center;
            min-height: 2.35rem;
            border: 1px solid rgba(255,255,255,0.14);
            border-radius: 999px;
            background: rgba(255,255,255,0.08);
            color: rgba(255,255,255,0.86);
            padding: 0 0.9rem;
            font-size: 0.92rem;
            font-weight: 700;
        }

        .signal-panel {
            border: 1px solid rgba(255,255,255,0.16);
            border-radius: 8px;
            background: rgba(10, 5, 18, 0.64);
            padding: 1rem;
            min-height: 100%;
        }

        .signal-panel-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 1rem;
        }

        .signal-panel strong {
            color: #ffffff;
        }

        .signal-status {
            border-radius: 999px;
            background: rgba(32, 227, 178, 0.12);
            color: var(--vet-mint);
            padding: 0.25rem 0.65rem;
            font-size: 0.78rem;
            font-weight: 800;
        }

        .signal-list {
            display: grid;
            gap: 0.75rem;
        }

        .signal-item {
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 8px;
            background: rgba(255,255,255,0.06);
            padding: 0.85rem;
        }

        .signal-item span {
            display: block;
            color: rgba(255,255,255,0.56);
            font-size: 0.82rem;
            margin-bottom: 0.18rem;
        }

        .signal-item b {
            color: #ffffff;
            font-size: 1.15rem;
        }

        .metric-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1rem;
            margin: 1rem 0 1.4rem;
        }

        .metric-card,
        .upload-card,
        .result-card {
            border: 1px solid var(--vet-line);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.98);
            padding: 1rem;
            box-shadow: 0 18px 44px rgba(61, 25, 84, 0.08);
        }

        .metric-card strong {
            display: block;
            color: var(--vet-ink);
            font-size: 1.15rem;
            line-height: 1.2;
        }

        .metric-card span {
            display: block;
            margin-top: 0.35rem;
            color: var(--vet-muted);
            font-size: 0.92rem;
            line-height: 1.45;
        }

        .section-title {
            margin: 0.25rem 0 0.55rem;
            color: var(--vet-ink);
            font-size: 1.35rem;
            font-weight: 850;
            letter-spacing: 0;
        }

        .section-copy {
            margin: 0 0 1rem;
            color: var(--vet-muted);
            line-height: 1.6;
        }

        .result-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            border-radius: 999px;
            background: #f2e5fb;
            color: #43105f;
            padding: 0.38rem 0.8rem;
            font-weight: 800;
            margin: 0.2rem 0.35rem 0.75rem 0;
        }

        .research-note {
            border: 1px solid var(--vet-line);
            border-left: 4px solid var(--vet-purple);
            border-radius: 8px;
            background: #ffffff;
            color: var(--vet-muted);
            padding: 0.9rem 1rem;
            margin: 0 0 1rem;
            line-height: 1.55;
        }

        .research-note strong {
            color: var(--vet-ink);
        }

        .creator {
            border-top: 1px solid var(--vet-line);
            margin-top: 1rem;
            padding-top: 1rem;
            color: var(--vet-muted);
            font-size: 0.92rem;
        }

        div[data-testid="stFileUploader"] {
            border: 1px dashed rgba(130, 10, 209, 0.34);
            border-radius: 8px;
            background: #ffffff;
            padding: 0.6rem;
        }

        .stButton button,
        [data-testid="stFileUploaderDropzone"] button {
            border-radius: 8px;
            border-color: var(--vet-purple);
            color: var(--vet-purple);
        }

        [data-testid="stMetric"] {
            border: 1px solid var(--vet-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 0.8rem 0.9rem;
        }

        [data-testid="stMetricValue"] {
            color: var(--vet-purple);
        }

        @media (max-width: 900px) {
            .hero {
                padding: 1.35rem;
            }

            .hero-grid,
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
            <div class="brand-mark">VI</div>
            <div class="brand-text">
                <strong>Vet-IA</strong>
                <span>Triagem leucocitária</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Projeto acadêmico em Medicina Veterinária")
    st.divider()
    st.markdown("### Configurações")
    conf_threshold = st.slider("Confiança mínima", 0.0, 1.0, 0.30, 0.05)
    st.caption(
        "Valores menores aumentam a sensibilidade. Valores maiores priorizam detecções mais confiáveis."
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
        <div class="hero-grid">
            <div>
                <div class="brand-lockup">
                    <div class="brand-mark">VI</div>
                    <div class="brand-text">
                        <strong>Vet-IA</strong>
                        <span>Análise microscópica assistida</span>
                    </div>
                </div>
                <div class="hero-label">Protótipo de inteligência artificial</div>
                <h1>Triagem morfológica de neutrófilos com visão computacional</h1>
                <p>
                    Uma interface premium para demonstrar detecção, classificação e contagem
                    de neutrófilos segmentados e bastonetes em microfotografias de esfregaços sanguíneos.
                </p>
                <div class="hero-actions">
                    <span class="hero-chip">YOLOv8</span>
                    <span class="hero-chip">Desvio à esquerda</span>
                    <span class="hero-chip">Hematologia veterinária</span>
                </div>
            </div>
            <div class="signal-panel">
                <div class="signal-panel-header">
                    <strong>Fluxo de análise</strong>
                    <span class="signal-status">experimental</span>
                </div>
                <div class="signal-list">
                    <div class="signal-item">
                        <span>Entrada</span>
                        <b>Microfotografia</b>
                    </div>
                    <div class="signal-item">
                        <span>Saída visual</span>
                        <b>Bounding boxes</b>
                    </div>
                    <div class="signal-item">
                        <span>Resumo</span>
                        <b>CSV + métricas</b>
                    </div>
                </div>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="metric-grid">
        <div class="metric-card">
            <strong>Detecção inteligente</strong>
            <span>Modelo de visão computacional aplicado a imagens microscópicas.</span>
        </div>
        <div class="metric-card">
            <strong>Triagem organizada</strong>
            <span>Contagem de segmentados, bastonetes e total detectado.</span>
        </div>
        <div class="metric-card">
            <strong>Resultado exportável</strong>
            <span>Resumo em CSV para documentação dos testes e apresentação acadêmica.</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="research-note">
        <strong>Uso experimental:</strong> o Vet-IA é uma ferramenta acadêmica de apoio visual.
        A interpretação final deve ser realizada por profissional habilitado.
    </div>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_model():
    return YOLO("best.pt")


model = load_model()

st.markdown('<div class="upload-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Enviar imagem</div>', unsafe_allow_html=True)
st.markdown(
    '<p class="section-copy">Use uma foto nítida do campo microscópico para obter marcações mais consistentes.</p>',
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
        st.image(res_plotted, caption="Imagem analisada pelo Vet-IA", use_container_width=True)

    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Relatório automático</div>', unsafe_allow_html=True)

    detections = results[0].boxes.cls.tolist()
    names = model.names

    if detections:
        counts = {}
        for class_idx in sorted(set(detections)):
            name = names[int(class_idx)]
            quantity = detections.count(class_idx)
            counts[name] = quantity
            st.markdown(
                f'<span class="result-pill">{name}: {quantity} encontrada(s)</span>',
                unsafe_allow_html=True,
            )

        total_cells = len(detections)
        band_count = sum(qty for name, qty in counts.items() if "baston" in name.lower())
        segmented_count = sum(qty for name, qty in counts.items() if "segment" in name.lower())
        band_ratio = (band_count / total_cells) * 100 if total_cells else 0

        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.metric("Total detectado", total_cells)
        metric_col2.metric("Bastonetes", band_count)
        metric_col3.metric("Bastonetes (%)", f"{band_ratio:.1f}%")

        csv_rows = ["classe,quantidade"]
        for name, quantity in counts.items():
            csv_rows.append(f"{name},{quantity}")
        csv_rows.append(f"total,{total_cells}")
        csv_rows.append(f"segmentados,{segmented_count}")
        csv_rows.append(f"proporcao_bastonetes,{band_ratio:.1f}%")

        st.download_button(
            "Baixar resumo em CSV",
            data="\n".join(csv_rows),
            file_name="resultado-vet-ia.csv",
            mime="text/csv",
        )

        st.caption(
            "A proporção de bastonetes é um indicador experimental e deve ser conferida por avaliação microscópica profissional."
        )
    else:
        st.warning("Nenhuma célula detectada. Tente reduzir a confiança mínima na barra lateral.")

    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Envie uma imagem para iniciar a análise.")
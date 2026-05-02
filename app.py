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
            --vet-purple: #820ad1;
            --vet-purple-dark: #3b0a57;
            --vet-purple-soft: #f4e8ff;
            --vet-green: #00a884;
            --vet-ink: #19151f;
            --vet-muted: #6f667a;
            --vet-line: #e8dff0;
            --vet-surface: #ffffff;
            --vet-page: #fbf8fd;
        }

        .stApp {
            background: linear-gradient(180deg, #fbf8fd 0%, #ffffff 52%, #f7f3fb 100%);
            color: var(--vet-ink);
        }

        .main .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid var(--vet-line);
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: var(--vet-purple-dark);
        }

        .brand-lockup {
            display: flex;
            align-items: center;
            gap: 0.85rem;
            margin-bottom: 1rem;
        }

        .brand-mark {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 3.2rem;
            height: 3.2rem;
            flex: 0 0 auto;
            border-radius: 8px;
            background: var(--vet-purple);
            color: #ffffff;
            box-shadow: 0 14px 30px rgba(130, 10, 209, 0.2);
            font-weight: 900;
            letter-spacing: 0;
        }

        .brand-text strong {
            display: block;
            color: var(--vet-purple-dark);
            font-size: 1.3rem;
            line-height: 1.1;
        }

        .brand-text span {
            display: block;
            color: var(--vet-muted);
            font-size: 0.9rem;
            margin-top: 0.15rem;
        }

        .hero {
            border: 1px solid var(--vet-line);
            border-radius: 8px;
            background: linear-gradient(135deg, #ffffff 0%, #f6ebff 100%);
            padding: 2rem;
            box-shadow: 0 16px 34px rgba(59, 10, 87, 0.08);
        }

        .hero-grid {
            display: grid;
            grid-template-columns: minmax(0, 1.25fr) minmax(280px, 0.75fr);
            gap: 2rem;
            align-items: center;
        }

        .hero-label {
            width: fit-content;
            border: 1px solid rgba(130, 10, 209, 0.18);
            border-radius: 999px;
            background: #ffffff;
            color: var(--vet-purple);
            padding: 0.35rem 0.75rem;
            margin: 0 0 1rem;
            font-size: 0.82rem;
            font-weight: 800;
            letter-spacing: 0;
            text-transform: uppercase;
        }

        .hero h1 {
            max-width: 780px;
            margin: 0 0 0.85rem;
            color: var(--vet-purple-dark);
            font-size: clamp(2rem, 4vw, 3.4rem);
            line-height: 1.04;
            letter-spacing: 0;
        }

        .hero p {
            max-width: 720px;
            margin: 0;
            color: var(--vet-muted);
            font-size: 1.04rem;
            line-height: 1.65;
        }

        .hero-summary {
            border-left: 4px solid var(--vet-green);
            padding-left: 1.1rem;
        }

        .hero-summary strong {
            display: block;
            color: var(--vet-purple-dark);
            font-size: 1.05rem;
            margin-bottom: 0.45rem;
        }

        .hero-summary span {
            display: block;
            color: var(--vet-muted);
            line-height: 1.55;
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
            background: rgba(255, 255, 255, 0.96);
            padding: 1rem;
            box-shadow: 0 10px 26px rgba(59, 10, 87, 0.06);
        }

        .metric-card strong {
            display: block;
            color: var(--vet-purple-dark);
            font-size: 1.18rem;
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
            color: var(--vet-purple-dark);
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
            background: var(--vet-purple-soft);
            color: var(--vet-purple-dark);
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
            color: var(--vet-purple-dark);
        }

        .creator {
            border-top: 1px solid var(--vet-line);
            margin-top: 1rem;
            padding-top: 1rem;
            color: var(--vet-muted);
            font-size: 0.92rem;
        }

        div[data-testid="stFileUploader"] {
            border: 1px dashed rgba(130, 10, 209, 0.35);
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

        @media (max-width: 860px) {
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
                <h1>Triagem de neutrófilos em esfregaços sanguíneos</h1>
                <p>
                    Envie uma microfotografia e visualize a classificação automatizada
                    entre neutrófilos segmentados e bastonetes, com contagem resumida
                    para apoio à triagem do desvio à esquerda.
                </p>
            </div>
            <div class="hero-summary">
                <strong>Foco do protótipo</strong>
                <span>Detecção visual, classificação morfológica e relatório simples para demonstração acadêmica.</span>
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
            <strong>YOLO</strong>
            <span>Modelo de visão computacional aplicado a imagens microscópicas.</span>
        </div>
        <div class="metric-card">
            <strong>Upload rápido</strong>
            <span>Compatível com imagens JPG, JPEG e PNG.</span>
        </div>
        <div class="metric-card">
            <strong>Resumo exportável</strong>
            <span>Contagem por classe e arquivo CSV para documentação dos testes.</span>
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
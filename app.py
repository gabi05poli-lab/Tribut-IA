import streamlit as st
import datetime

# ════════════════════════════════════════════════════════════
#  CONFIG
# ════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Tribut-IA | Asistente Fiscal",
    page_icon="🤖",
    layout="centered",
)

# ════════════════════════════════════════════════════════════
#  CSS
# ════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Space+Grotesk:wght@500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Fondo general */
.stApp {
    background: #0e0e14;
    color: #e2e2e8;
}

/* Header principal */
.tia-header {
    background: linear-gradient(135deg, #1a1035 0%, #2a0d4a 100%);
    border-radius: 16px;
    padding: 32px 36px 24px;
    border: 1px solid #3a2060;
    margin-bottom: 24px;
    box-shadow: 0 0 60px rgba(100,60,200,0.2);
}
.tia-header h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0 0 6px;
    background: linear-gradient(90deg, #b07fff, #5eead4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.tia-header p { color: #8b7fb0; margin: 0; font-size: 0.95rem; }
.tia-badge {
    display: inline-block;
    background: #3a1d6e;
    border: 1px solid #7c4dcc;
    border-radius: 20px;
    padding: 3px 14px;
    font-size: 0.7rem;
    color: #c4a6ff;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 12px;
}

/* Cards de resultado */
.result-card {
    background: #14101f;
    border: 1px solid #2c204a;
    border-radius: 14px;
    padding: 22px 26px;
    margin-top: 16px;
}
.result-card h3 {
    font-family: 'Space Grotesk', sans-serif;
    color: #b07fff;
    margin-top: 0;
    font-size: 1.15rem;
}
.highlight { color: #5eead4; font-weight: 700; }
.warn-box {
    background: #1a1208;
    border: 1px solid #5a3a00;
    border-radius: 8px;
    padding: 10px 14px;
    color: #f0b429;
    font-size: 0.82rem;
    margin-top: 16px;
}

/* Métrica custom */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin: 14px 0;
}
.metric-box {
    background: #1a1028;
    border: 1px solid #2c204a;
    border-radius: 10px;
    padding: 14px;
    text-align: center;
}
.metric-label { color: #6b5e85; font-size: 0.72rem; margin-bottom: 5px; }
.metric-value { color: #b07fff; font-weight: 700; font-size: 1rem; }

/* Categorías */
.cat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-top: 14px;
}
.cat-card {
    background: #1a1028;
    border: 1px solid #2c204a;
    border-radius: 10px;
    padding: 12px;
    text-align: center;
    font-size: 0.78rem;
}
.cat-card.active {
    border-color: #7c4dcc;
    background: #200e3a;
    box-shadow: 0 0 14px rgba(124,77,204,0.35);
}
.cat-name { font-family: 'Space Grotesk',sans-serif; font-size:1.5rem; font-weight:700; color:#b07fff; }
.cat-tope { color:#6b5e85; font-size:0.7rem; margin-top:2px; }
.cat-cuota { color:#c4a6ff; font-weight:600; margin-top:6px; }

/* Calendario */
.cal-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin-top: 12px;
}
.cal-item {
    background: #14101f;
    border: 1px solid #2c204a;
    border-radius: 8px;
    padding: 12px;
    font-size: 0.8rem;
}
.cal-item.current { border-color: #5eead4; background: #0d1f1e; }
.cal-mes { font-family:'Space Grotesk',sans-serif; color:#5eead4; font-weight:600; font-size:0.9rem; }
.cal-evento { color:#8b7fb0; margin-top:4px; line-height:1.4; }

/* Barra de progreso custom */
.progress-wrap { margin: 8px 0; }
.progress-label { display:flex; justify-content:space-between; font-size:0.8rem; color:#8b7fb0; margin-bottom:4px; }
.progress-bar-bg { background:#2c204a; border-radius:4px; height:10px; }
.progress-bar-fill { height:100%; border-radius:4px; }

/* Footer */
.footer-box {
    background: #14101f;
    border: 1px solid #2c204a;
    border-radius: 10px;
    padding: 14px 20px;
    text-align: center;
    color: #6b5e85;
    font-size: 0.78rem;
    margin-top: 32px;
}

/* Streamlit overrides */
div[data-testid="stTabs"] button {
    color: #8b7fb0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #b07fff !important;
    border-bottom-color: #7c4dcc !important;
}
div[data-testid="stNumberInput"] input,
div[data-testid="stSelectbox"] select,
select {
    background: #1a1028 !important;
    color: #e2e2e8 !important;
    border: 1px solid #3a2060 !important;
    border-radius: 8px !important;
}
.stButton button {
    background: linear-gradient(135deg, #7c4dcc, #5eead4) !important;
    color: #0e0e14 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: 0.03em !important;
    transition: opacity 0.2s !important;
}
.stButton button:hover { opacity: 0.88 !important; }
label, .stSelectbox label, .stNumberInput label {
    color: #8b7fb0 !important;
    font-size: 0.85rem !important;
}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
#  DATOS
# ════════════════════════════════════════════════════════════

CATEGORIAS = {
    "A": {"tope": 7_812_251,   "impuesto": 10_537,  "obra_social": 12_000, "jubilacion": 5_186},
    "B": {"tope": 11_524_146,  "impuesto": 13_167,  "obra_social": 12_000, "jubilacion": 5_186},
    "C": {"tope": 16_149_559,  "impuesto": 16_795,  "obra_social": 12_000, "jubilacion": 5_186},
    "D": {"tope": 19_996_219,  "impuesto": 24_553,  "obra_social": 12_000, "jubilacion": 5_186},
    "E": {"tope": 23_548_462,  "impuesto": 33_363,  "obra_social": 12_000, "jubilacion": 5_186},
    "F": {"tope": 29_150_889,  "impuesto": 43_765,  "obra_social": 12_000, "jubilacion": 5_186},
    "G": {"tope": 33_418_971,  "impuesto": 58_143,  "obra_social": 12_000, "jubilacion": 5_186},
    "H": {"tope": 50_837_832,  "impuesto": 82_064,  "obra_social": 12_000, "jubilacion": 5_186},
    "I": {"tope": 56_842_895,  "impuesto": 109_425, "obra_social": 12_000, "jubilacion": 5_186},
    "J": {"tope": 63_566_040,  "impuesto": 145_895, "obra_social": 12_000, "jubilacion": 5_186},
    "K": {"tope": 76_279_250,  "impuesto": 194_520, "obra_social": 12_000, "jubilacion": 5_186},
}

IIBB = {
    "Santa Fe":     {"comercio": 0.040, "servicios": 0.050},
    "Buenos Aires": {"comercio": 0.035, "servicios": 0.060},
    "CABA":         {"comercio": 0.030, "servicios": 0.055},
    "Córdoba":      {"comercio": 0.040, "servicios": 0.050},
    "Mendoza":      {"comercio": 0.035, "servicios": 0.048},
    "Entre Ríos":   {"comercio": 0.040, "servicios": 0.050},
    "Tucumán":      {"comercio": 0.045, "servicios": 0.055},
    "Salta":        {"comercio": 0.040, "servicios": 0.050},
    "Misiones":     {"comercio": 0.040, "servicios": 0.050},
    "Chaco":        {"comercio": 0.040, "servicios": 0.050},
}

CONCEPTOS = {
    "Monotributo": {
        "emoji": "🧾",
        "texto": """
**¿Qué es?**
En lugar de pagar 5 impuestos distintos por separado, los juntás todos en una sola cuota mensual fija.
Esa cuota incluye impuesto integrado (Ganancias + IVA simplificados), jubilación (aporte al SIPA) y obra social.

**¿Cómo funciona?**
Hay categorías de la A a la K según cuánto facturás al año. Cuanto más facturás, mayor es tu categoría y tu cuota mensual.
Los topes se actualizan periódicamente — revisá siempre los valores vigentes en afip.gob.ar.

**¿Quién puede ser Monotributista?**
Personas físicas con ingresos por locación de bienes, obras o servicios, que no superen los topes de cada categoría.
""",
    },
    "Ingresos Brutos (IIBB)": {
        "emoji": "🏛️",
        "texto": """
**¿Qué es?**
Es un impuesto **provincial** — cada provincia cobra un porcentaje sobre tus ventas brutas (antes de descontar costos).

**Ejemplo concreto:**
En Santa Fe, si vendés bebidas (comercio) y facturás $1.000.000 al mes, pagás aprox. $40.000 de IIBB (alícuota del 4%).

**Ojo con esto:**
Si vendés en más de una provincia, puede que debas inscribirte en el **Convenio Multilateral** (sistema que evita pagar IIBB dos veces por la misma operación).
""",
    },
    "SIRCREB / Retenciones bancarias": {
        "emoji": "🏦",
        "texto": """
**¿Por qué me retienen plata del banco?**
El SIRCREB es el Sistema de Recaudación sobre Créditos Bancarios. Cada vez que te entra plata en la cuenta, el banco retiene automáticamente un porcentaje como adelanto de IIBB.

**¿Es un gasto extra?**
No. Es un adelanto. Ese dinero retenido se descuenta de tu declaración mensual de IIBB.

**¿Cómo lo identifico?**
En tu resumen bancario vas a ver la retención bajo el concepto "SIRCREB" o similar. Si te retienen de más, podés pedir la devolución o imputarlo a próximos períodos.
""",
    },
    "IVA": {
        "emoji": "📋",
        "texto": """
**¿Qué es el IVA?**
El IVA (Impuesto al Valor Agregado) es un impuesto al consumo del 21% (general) que recaés vos y le rendís al fisco.

**Monotributistas:** El IVA ya está incluido en tu cuota mensual. No presentás declaraciones de IVA por separado. 🙌

**Responsables Inscriptos:** Debés presentar DDJJ mensual. La lógica es:
- IVA que te cobran tus proveedores → Crédito Fiscal (a tu favor)
- IVA que cobrás en tus ventas → Débito Fiscal (le debés al fisco)
- La diferencia es lo que pagás (o te devuelven)
""",
    },
    "Factura Electrónica": {
        "emoji": "🧾",
        "texto": """
**¿Cómo emito facturas?**
Desde AFIP podés emitir facturas electrónicas gratis en: afip.gob.ar → "Mis Comprobantes en línea"

**Como Monotributista emitís Factura C** para todos tus clientes.

**Pasos básicos:**
1. Entrás a AFIP con Clave Fiscal nivel 2 o superior
2. Seleccionás "Comprobantes en línea"
3. Elegís el punto de venta y tipo de comprobante (Factura C)
4. Completás los datos y la emitís — llegará por mail al cliente

**Tip:** La app "Mis Facturas AFIP" te permite hacerlo directamente desde el celular.
""",
    },
    "Recategorización": {
        "emoji": "🔄",
        "texto": """
**¿Qué es la recategorización?**
Dos veces al año (enero y julio) debés revisar si tu categoría de Monotributo sigue siendo correcta,
comparando tu facturación real de los últimos 12 meses contra los topes de cada categoría.

**¿Qué pasa si no me recategorizo?**
AFIP puede recategorizarte de oficio y cobrarte la diferencia con intereses.

**¿Cómo se hace?**
Entrás a AFIP → "Monotributo" → "Recategorización" y el sistema te guía automáticamente.

**Importante:** si subiste de categoría, empezás a pagar más desde el mes siguiente.
Si bajaste, podés pagar menos.
""",
    },
}

VENCIMIENTOS = {
    1:  ("Ene", "Monotributo (CUIT 0-1) · IIBB Santa Fe"),
    2:  ("Feb", "Monotributo (CUIT 2-3) · IIBB Buenos Aires"),
    3:  ("Mar", "Monotributo (CUIT 4-5) · DDJJ informativas"),
    4:  ("Abr", "Monotributo (CUIT 6-7) · Cuota general"),
    5:  ("May", "Monotributo (CUIT 8-9) · Percepciones"),
    6:  ("Jun", "Cierre 1er semestre · Blanqueo/regímenes"),
    7:  ("Jul", "Recategorización semestral · Monotributo"),
    8:  ("Ago", "Monotributo general · IIBB provincial"),
    9:  ("Sep", "DDJJ informativas · Vencimientos especiales"),
    10: ("Oct", "Monotributo · Retenciones bancarias SIRCREB"),
    11: ("Nov", "Cierre ejercicio RI · Anticipos Ganancias"),
    12: ("Dic", "Aguinaldo SAC (2da cuota) · Venc. especiales"),
}

MES_ACTUAL = datetime.datetime.now().month

# ════════════════════════════════════════════════════════════
#  HELPERS
# ════════════════════════════════════════════════════════════

def fmt(n): return f"$ {n:,.0f}".replace(",", ".")

def barra(pct, color):
    w = max(0, min(100, pct))
    return f"""
<div class="progress-wrap">
  <div class="progress-bar-bg">
    <div class="progress-bar-fill" style="width:{w}%;background:{color};"></div>
  </div>
</div>"""

# ════════════════════════════════════════════════════════════
#  HEADER
# ════════════════════════════════════════════════════════════

st.markdown("""
<div class="tia-header">
  <div class="tia-badge">Trabajo Final IA · Gabriel Poli · UCA Rosario</div>
  <h1>Tribut-IA 🤖</h1>
  <p>Asistente para la educación financiera y fiscal de jóvenes emprendedores argentinos</p>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
#  TABS
# ════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Categoría Monotributo",
    "📐 Margen de Ganancia",
    "📚 Glosario Fiscal",
    "📅 Vencimientos",
])

# ── TAB 1: Monotributo ───────────────────────────────────────
with tab1:
    st.markdown("#### ¿Cuánto facturás por mes?")
    st.markdown("<p style='color:#8b7fb0;font-size:0.85rem;'>Ingresá tu promedio mensual y te decimos qué categoría te corresponde.</p>", unsafe_allow_html=True)

    fac_mensual = st.number_input(
        "Facturación mensual promedio ($)",
        min_value=1_000,
        max_value=999_999_999,
        value=500_000,
        step=10_000,
        format="%d",
    )

    if st.button("Calcular mi categoría →", key="btn_cat"):
        fac_anual = fac_mensual * 12
        cat_resultado = None
        for cat, d in CATEGORIAS.items():
            if fac_anual <= d["tope"]:
                cat_resultado = (cat, d)
                break

        if cat_resultado is None:
            st.markdown(f"""
<div class="result-card">
  <h3>📊 Resultado</h3>
  <p>Tu facturación anual de <span class="highlight">{fmt(fac_anual)}</span> supera el tope máximo del Monotributo (Cat. K).</p>
  <p>Probablemente debas inscribirte como <span class="highlight">Responsable Inscripto (RI)</span>. Consultá con un Contador Público.</p>
  <div class="warn-box">⚠️ Información orientativa. Consultá siempre con un CP matriculado.</div>
</div>""", unsafe_allow_html=True)
        else:
            cat, d = cat_resultado
            total = d["impuesto"] + d["obra_social"] + d["jubilacion"]

            cats_html = '<div class="cat-grid">'
            for c, datos in CATEGORIAS.items():
                t = datos["impuesto"] + datos["obra_social"] + datos["jubilacion"]
                active = "active" if c == cat else ""
                cats_html += f"""
<div class="cat-card {active}">
  <div class="cat-name">{c}</div>
  <div class="cat-tope">Hasta {fmt(datos['tope'])}/año</div>
  <div class="cat-cuota">{fmt(t)}/mes</div>
</div>"""
            cats_html += "</div>"

            st.markdown(f"""
<div class="result-card">
  <h3>📊 Tu categoría es la <span class="highlight" style="font-size:1.4rem;">Categoría {cat}</span></h3>
  <p>Facturación anual estimada: <span class="highlight">{fmt(fac_anual)}</span> &nbsp;|&nbsp; Tope: {fmt(d['tope'])}</p>

  <div class="metric-grid">
    <div class="metric-box">
      <div class="metric-label">Impuesto integrado</div>
      <div class="metric-value">{fmt(d['impuesto'])}/mes</div>
    </div>
    <div class="metric-box">
      <div class="metric-label">Obra Social</div>
      <div class="metric-value">{fmt(d['obra_social'])}/mes</div>
    </div>
    <div class="metric-box">
      <div class="metric-label">Jubilación (SIPA)</div>
      <div class="metric-value">{fmt(d['jubilacion'])}/mes</div>
    </div>
  </div>

  <p style="font-size:1.05rem;">Cuota total mensual: <span class="highlight" style="font-size:1.3rem;">{fmt(total)}</span></p>

  <p style="color:#8b7fb0;font-size:0.8rem;margin-top:16px;margin-bottom:6px;">Mapa de todas las categorías (resaltada la tuya):</p>
  {cats_html}

  <div class="warn-box">⚠️ Valores orientativos 2025/2026. Verificá la RG AFIP vigente y consultá con un Contador Público matriculado.</div>
</div>""", unsafe_allow_html=True)

# ── TAB 2: Margen ────────────────────────────────────────────
with tab2:
    st.markdown("#### Calculá tu margen de ganancia real")
    st.markdown("<p style='color:#8b7fb0;font-size:0.85rem;'>Incluye impuestos para que el número refleje lo que realmente te queda.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        pv  = st.number_input("Ventas mensuales ($)", min_value=1, value=1_000_000, step=10_000, format="%d")
        cp  = st.number_input("Costo del producto ($)", min_value=0, value=500_000, step=10_000, format="%d")
        og  = st.number_input("Otros gastos fijos ($)", min_value=0, value=50_000, step=5_000, format="%d")
    with col2:
        mono_cuota = st.number_input("Cuota Monotributo mensual ($)", min_value=0, value=27_371, step=1_000, format="%d")
        provincia  = st.selectbox("Provincia", list(IIBB.keys()), index=0)
        actividad  = st.selectbox("Tipo de actividad", ["comercio", "servicios"])

    if st.button("Calcular margen →", key="btn_margen"):
        iibb_rate    = IIBB[provincia][actividad]
        iibb_monto   = pv * iibb_rate
        gan_bruta    = pv - cp
        gan_neta     = gan_bruta - mono_cuota - iibb_monto - og
        mb_pct       = (gan_bruta / pv * 100) if pv else 0
        mn_pct       = (gan_neta  / pv * 100) if pv else 0
        color_neto   = "#5eead4" if gan_neta >= 0 else "#f87171"

        alerta_negativa = f'<p style="color:#f87171;margin-top:10px;">⚠️ Tu margen neto es negativo. Revisá tus costos o precio de venta.</p>' if gan_neta < 0 else ""

        st.markdown(f"""
<div class="result-card">
  <h3>📐 Análisis de Margen — {provincia} ({actividad})</h3>

  <div class="metric-grid">
    <div class="metric-box">
      <div class="metric-label">Ventas</div>
      <div class="metric-value">{fmt(pv)}</div>
    </div>
    <div class="metric-box">
      <div class="metric-label">Costo producto</div>
      <div class="metric-value" style="color:#f87171;">{fmt(cp)}</div>
    </div>
    <div class="metric-box">
      <div class="metric-label">Ganancia bruta</div>
      <div class="metric-value">{fmt(gan_bruta)}</div>
    </div>
    <div class="metric-box">
      <div class="metric-label">IIBB ({iibb_rate*100:.1f}%)</div>
      <div class="metric-value" style="color:#f0b429;">{fmt(iibb_monto)}</div>
    </div>
    <div class="metric-box">
      <div class="metric-label">Monotributo</div>
      <div class="metric-value" style="color:#f0b429;">{fmt(mono_cuota)}</div>
    </div>
    <div class="metric-box">
      <div class="metric-label">Otros gastos</div>
      <div class="metric-value" style="color:#f0b429;">{fmt(og)}</div>
    </div>
  </div>

  <div style="margin:16px 0 4px;">
    <div class="progress-label"><span>Margen Bruto</span><span class="highlight">{mb_pct:.1f}%</span></div>
    {barra(mb_pct, "#b07fff")}
  </div>
  <div style="margin:10px 0 16px;">
    <div class="progress-label"><span>Margen Neto Real</span><span style="color:{color_neto};font-weight:700;">{mn_pct:.1f}%</span></div>
    {barra(mn_pct, color_neto)}
  </div>

  <p style="font-size:1.1rem;">Ganancia neta mensual: <span style="color:{color_neto};font-size:1.35rem;font-weight:700;">{fmt(gan_neta)}</span></p>
  {alerta_negativa}

  <div class="warn-box">⚠️ Cálculo orientativo. Las alícuotas de IIBB y otros factores pueden variar. Consultá con un Contador Público.</div>
</div>""", unsafe_allow_html=True)

# ── TAB 3: Glosario ──────────────────────────────────────────
with tab3:
    st.markdown("#### ¿Qué significa este término?")
    st.markdown("<p style='color:#8b7fb0;font-size:0.85rem;'>Explicaciones en lenguaje simple, sin tecnicismos innecesarios.</p>", unsafe_allow_html=True)

    concepto_sel = st.selectbox("Elegí el concepto", list(CONCEPTOS.keys()))

    if st.button("Explicame este concepto →", key="btn_concepto"):
        c = CONCEPTOS[concepto_sel]
        st.markdown(f"""
<div class="result-card">
  <h3>{c['emoji']} {concepto_sel}</h3>
  <div style="line-height:1.8;color:#c4b8d8;">
""", unsafe_allow_html=True)
        st.markdown(c["texto"])
        st.markdown("""
  </div>
  <div class="warn-box">⚠️ Esta explicación es educativa y general. Para tu situación particular, consultá siempre con un Contador Público matriculado.</div>
</div>""", unsafe_allow_html=True)

# ── TAB 4: Calendario ────────────────────────────────────────
with tab4:
    st.markdown("#### Calendario de Vencimientos Fiscales")
    st.markdown("<p style='color:#8b7fb0;font-size:0.85rem;'>Mes actual resaltado en verde. Las fechas exactas dependen de tu CUIT y la RG AFIP vigente.</p>", unsafe_allow_html=True)

    cal_html = '<div class="cal-grid">'
    for mes_num, (abrev, evento) in VENCIMIENTOS.items():
        current = "current" if mes_num == MES_ACTUAL else ""
        cal_html += f"""
<div class="cal-item {current}">
  <div class="cal-mes">{abrev}</div>
  <div class="cal-evento">{evento}</div>
</div>"""
    cal_html += "</div>"

    st.markdown(f"""
<div class="result-card">
  <h3>📅 Vencimientos clave del año fiscal</h3>
  {cal_html}
  <div class="warn-box">⚠️ Las fechas exactas varían según el último dígito de tu CUIT y las resoluciones AFIP del período. Verificá siempre en afip.gob.ar.</div>
</div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
#  FOOTER
# ════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer-box">
  ⚠️ <strong>Aviso legal:</strong> Tribut-IA es una herramienta educativa e informativa.
  No reemplaza la asesoría de un Contador Público matriculado.
  Toda decisión patrimonial debe ser validada por un profesional habilitado.<br><br>
  Proyecto académico · MOT Inteligencia Artificial · UCA Facultad de Ciencias Económicas del Rosario · Gabriel Poli
</div>
""", unsafe_allow_html=True)

# ============================================================
#  TRIBUT-IA 🤖💼  |  Asistente Fiscal para Jóvenes Emprendedores
#  Autor del proyecto: Gabriel Poli
#  Cómo ejecutar: Google Colab → Menú "Entorno de ejecución" → "Ejecutar todo"
# ============================================================

# ── Dependencias (Colab ya las tiene, pero por si acaso) ────
import subprocess, sys

def _install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pkg])

try:
    import ipywidgets as widgets
    from IPython.display import display, HTML, clear_output
except ImportError:
    _install("ipywidgets")
    import ipywidgets as widgets
    from IPython.display import display, HTML, clear_output

import datetime

# ════════════════════════════════════════════════════════════
#  DATOS DE REFERENCIA — Monotributo 2025/2026  (valores estimados,
#  actualizar con RG AFIP vigente)
# ════════════════════════════════════════════════════════════

CATEGORIAS_MONOTRIBUTO = {
    "A": {"tope_anual": 7_812_251,  "cuota_impuesto": 10_537,  "cuota_obra_social": 12_000, "cuota_jubilacion": 5_186},
    "B": {"tope_anual": 11_524_146, "cuota_impuesto": 13_167,  "cuota_obra_social": 12_000, "cuota_jubilacion": 5_186},
    "C": {"tope_anual": 16_149_559, "cuota_impuesto": 16_795,  "cuota_obra_social": 12_000, "cuota_jubilacion": 5_186},
    "D": {"tope_anual": 19_996_219, "cuota_impuesto": 24_553,  "cuota_obra_social": 12_000, "cuota_jubilacion": 5_186},
    "E": {"tope_anual": 23_548_462, "cuota_impuesto": 33_363,  "cuota_obra_social": 12_000, "cuota_jubilacion": 5_186},
    "F": {"tope_anual": 29_150_889, "cuota_impuesto": 43_765,  "cuota_obra_social": 12_000, "cuota_jubilacion": 5_186},
    "G": {"tope_anual": 33_418_971, "cuota_impuesto": 58_143,  "cuota_obra_social": 12_000, "cuota_jubilacion": 5_186},
    "H": {"tope_anual": 50_837_832, "cuota_impuesto": 82_064,  "cuota_obra_social": 12_000, "cuota_jubilacion": 5_186},
    "I": {"tope_anual": 56_842_895, "cuota_impuesto": 109_425, "cuota_obra_social": 12_000, "cuota_jubilacion": 5_186},
    "J": {"tope_anual": 63_566_040, "cuota_impuesto": 145_895, "cuota_obra_social": 12_000, "cuota_jubilacion": 5_186},
    "K": {"tope_anual": 76_279_250, "cuota_impuesto": 194_520, "cuota_obra_social": 12_000, "cuota_jubilacion": 5_186},
}

# Alícuotas de Ingresos Brutos por provincia (valores orientativos)
ALICUOTAS_IIBB = {
    "Santa Fe":         {"comercio": 0.04,  "servicios": 0.05},
    "Buenos Aires":     {"comercio": 0.035, "servicios": 0.06},
    "CABA":             {"comercio": 0.03,  "servicios": 0.055},
    "Córdoba":          {"comercio": 0.04,  "servicios": 0.05},
    "Mendoza":          {"comercio": 0.035, "servicios": 0.048},
    "Tucumán":          {"comercio": 0.045, "servicios": 0.055},
    "Entre Ríos":       {"comercio": 0.04,  "servicios": 0.05},
    "Chaco":            {"comercio": 0.04,  "servicios": 0.05},
    "Salta":            {"comercio": 0.04,  "servicios": 0.05},
    "Misiones":         {"comercio": 0.04,  "servicios": 0.05},
}

CONCEPTOS_DICT = {
    "Monotributo": """
📌 **¿Qué es el Monotributo?**

Imaginate que, en lugar de pagar 5 impuestos distintos por separado cada mes,
los juntás todos en una sola cuota mensual fija. Eso es el Monotributo
(o Régimen Simplificado).

Esa cuota incluye:
• Impuesto integrado (Ganancias + IVA simplificados)
• Jubilación (aporte al SIPA)
• Obra Social

Hay categorías de la A a la K según cuánto facturás al año.
Cuanto más facturás, mayor es tu categoría y tu cuota mensual.

⚠️ Siempre confirmá los valores vigentes con un contador, ya que
los topes se actualizan periódicamente.
""",
    "Ingresos Brutos": """
📌 **¿Qué son los Ingresos Brutos (IIBB)?**

Es un impuesto provincial. Cada provincia cobra un porcentaje
sobre tus ventas brutas — es decir, antes de descontar costos.

Por ejemplo, en Santa Fe, si vendés bebidas (comercio) y facturás
$1.000.000 al mes, pagás aprox. $40.000 de IIBB
(4% sobre el total).

👉 Ojo: si vendés en más de una provincia, puede que
debas inscribirte en el Convenio Multilateral.
""",
    "SIRCREB / Percepciones": """
📌 **¿Por qué me retienen plata del banco? (SIRCREB)**

El SIRCREB es el Sistema de Recaudación sobre Créditos Bancarios.
Funciona así: cada vez que te entra plata en la cuenta, el banco
retiene automáticamente un porcentaje (varía por provincia, aprox. 1-5%).

¿Por qué? Porque la provincia recauda IIBB directamente desde los
acreditaciones bancarias, antes de que vos la retires.

Ese dinero retenido se descuenta de tu declaración mensual de IIBB.
No es un "gasto": es un adelanto.

🏦 Tip: revisá tu resumen bancario, vas a ver la retención bajo
el concepto "SIRCREB" o similar.
""",
    "IVA": """
📌 **¿Qué es el IVA?**

El IVA (Impuesto al Valor Agregado) es un impuesto que pagás como consumidor
y que también cobrás cuando vendés.

• IVA que te cobran tus proveedores → IVA Crédito Fiscal (a tu favor)
• IVA que vos cobrás en tus ventas → IVA Débito Fiscal (le debés al fisco)

En el Monotributo, el IVA ya está incluido en tu cuota mensual,
así que no necesitás presentar declaraciones de IVA por separado.
Eso simplifica mucho la vida 🙌

Si superás los topes y pasás a Responsable Inscripto, ahí sí
debés presentar IVA mensualmente.
""",
    "Factura Electrónica": """
📌 **Factura Electrónica**

Desde AFIP podés emitir facturas electrónicas gratis en:
🔗 https://www.afip.gob.ar → Mis Comprobantes

Como Monotributista emitís **Factura C** para tus clientes.
Si tu cliente es Responsable Inscripto, también usás Factura C
(a diferencia del RI que usa A o B).

Pasos básicos:
1. Entrás a AFIP con Clave Fiscal
2. Seleccionás "Comprobantes en línea"
3. Completás los datos y la emitís

💡 También hay apps como "Mis Facturas AFIP" para hacerlo desde el celular.
""",
}

VENCIMIENTOS = {
    1:  "IIBB Santa Fe / Monotributo (CUIT terminado en 0-1)",
    2:  "IIBB Buenos Aires",
    3:  "Monotributo (CUIT terminado en 2-3)",
    4:  "Pago cuota Monotributo general",
    5:  "Monotributo (CUIT terminado en 4-5)",
    6:  "Declaraciones juradas informativas",
    7:  "Monotributo (CUIT terminado en 6-7)",
    8:  "Blanqueo / regímenes especiales",
    9:  "Monotributo (CUIT terminado en 8-9)",
    10: "Recategorización semestral (enero y julio)",
    11: "Cierre ejercicio fiscal para RI",
    12: "Aguinaldo SAC (1ra cuota) + vencimientos especiales",
}

# ════════════════════════════════════════════════════════════
#  CSS / ESTILOS
# ════════════════════════════════════════════════════════════

ESTILOS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Space+Grotesk:wght@500;700&display=swap');

  .tia-root {
    font-family: 'Inter', sans-serif;
    background: #0e0e14;
    color: #e2e2e8;
    border-radius: 16px;
    padding: 0;
    max-width: 860px;
    margin: 0 auto;
    overflow: hidden;
    box-shadow: 0 0 60px rgba(100,60,200,0.25);
  }
  .tia-header {
    background: linear-gradient(135deg, #1a1035 0%, #2a0d4a 100%);
    padding: 28px 36px 22px;
    border-bottom: 1px solid #3a2060;
  }
  .tia-header h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    margin: 0 0 4px;
    background: linear-gradient(90deg, #b07fff, #5eead4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .tia-header p {
    margin: 0;
    font-size: 0.85rem;
    color: #8b7fb0;
  }
  .tia-badge {
    display: inline-block;
    background: #3a1d6e;
    border: 1px solid #7c4dcc;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.7rem;
    color: #c4a6ff;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 10px;
  }
  .tia-result {
    background: #14101f;
    border: 1px solid #2c204a;
    border-radius: 12px;
    padding: 20px 24px;
    margin: 0 24px 20px;
    font-size: 0.92rem;
    line-height: 1.7;
    white-space: pre-wrap;
  }
  .tia-result h3 {
    font-family: 'Space Grotesk', sans-serif;
    color: #b07fff;
    margin-top: 0;
    font-size: 1.1rem;
  }
  .tia-result .highlight {
    color: #5eead4;
    font-weight: 600;
  }
  .tia-result .warn {
    color: #f0b429;
    font-size: 0.82rem;
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px solid #2c204a;
  }
  .tia-section {
    padding: 20px 24px 6px;
  }
  .tia-section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #7c4dcc;
    margin-bottom: 8px;
  }
  .cat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 10px;
    margin: 12px 0;
  }
  .cat-card {
    background: #1a1028;
    border: 1px solid #2c204a;
    border-radius: 10px;
    padding: 14px 16px;
    font-size: 0.82rem;
  }
  .cat-card .cat-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #b07fff;
  }
  .cat-card.active {
    border-color: #7c4dcc;
    background: #200e3a;
    box-shadow: 0 0 16px rgba(124,77,204,0.3);
  }
  .cat-card .cat-label {
    color: #6b5e85;
    font-size: 0.72rem;
    margin-top: 2px;
  }
  .cal-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 8px;
    margin: 10px 0;
  }
  .cal-item {
    background: #14101f;
    border: 1px solid #2c204a;
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 0.78rem;
  }
  .cal-item .mes {
    font-family: 'Space Grotesk', sans-serif;
    color: #5eead4;
    font-weight: 600;
    font-size: 0.85rem;
  }
  .cal-item .evento {
    color: #8b7fb0;
    margin-top: 3px;
    line-height: 1.4;
  }
  .cal-item.current {
    border-color: #5eead4;
    background: #0d1f1e;
  }
</style>
"""

MESES = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
MES_ACTUAL = datetime.datetime.now().month

# ════════════════════════════════════════════════════════════
#  FUNCIONES LÓGICAS
# ════════════════════════════════════════════════════════════

def calcular_categoria_monotributo(facturacion_mensual: float) -> dict:
    """Dado el promedio mensual, devuelve la categoría correspondiente."""
    facturacion_anual = facturacion_mensual * 12
    for cat, datos in CATEGORIAS_MONOTRIBUTO.items():
        if facturacion_anual <= datos["tope_anual"]:
            cuota_total = datos["cuota_impuesto"] + datos["cuota_obra_social"] + datos["cuota_jubilacion"]
            return {
                "categoria": cat,
                "facturacion_anual": facturacion_anual,
                "tope_anual": datos["tope_anual"],
                "cuota_impuesto": datos["cuota_impuesto"],
                "cuota_obra_social": datos["cuota_obra_social"],
                "cuota_jubilacion": datos["cuota_jubilacion"],
                "cuota_total": cuota_total,
                "excede": False,
            }
    return {"excede": True, "facturacion_anual": facturacion_anual}


def calcular_margen(precio_venta: float, costo_producto: float,
                    cuota_monotributo: float, alicuota_iibb: float,
                    otros_gastos: float) -> dict:
    """Calcula el margen neto real del emprendedor."""
    iibb_mensual = precio_venta * alicuota_iibb
    ganancia_bruta = precio_venta - costo_producto
    ganancia_neta = ganancia_bruta - cuota_monotributo - iibb_mensual - otros_gastos
    margen_bruto_pct = (ganancia_bruta / precio_venta * 100) if precio_venta else 0
    margen_neto_pct = (ganancia_neta / precio_venta * 100) if precio_venta else 0
    return {
        "precio_venta": precio_venta,
        "costo_producto": costo_producto,
        "ganancia_bruta": ganancia_bruta,
        "iibb_mensual": iibb_mensual,
        "cuota_monotributo": cuota_monotributo,
        "otros_gastos": otros_gastos,
        "ganancia_neta": ganancia_neta,
        "margen_bruto_pct": margen_bruto_pct,
        "margen_neto_pct": margen_neto_pct,
    }


# ════════════════════════════════════════════════════════════
#  RENDERIZADORES HTML
# ════════════════════════════════════════════════════════════

def fmt(n: float) -> str:
    """Formatea número como pesos argentinos."""
    return f"$ {n:,.0f}".replace(",", ".")


def html_monotributo(fac_mensual: float) -> str:
    r = calcular_categoria_monotributo(fac_mensual)

    if r.get("excede"):
        return f"""
<div class="tia-result">
  <h3>📊 Resultado Monotributo</h3>
  <p>Tu facturación anual estimada de <span class="highlight">{fmt(r['facturacion_anual'])}</span>
  supera el tope máximo de la categoría K.</p>
  <p>Probablemente debas inscribirte como <span class="highlight">Responsable Inscripto (RI)</span>.
  Consultá urgente con un Contador Público.</p>
  <div class="warn">⚠️ Información orientativa. Confirmá siempre con un CP matriculado.</div>
</div>"""

    # Resaltar categorías
    cats_html = ""
    for cat, datos in CATEGORIAS_MONOTRIBUTO.items():
        active = "active" if cat == r["categoria"] else ""
        total = datos["cuota_impuesto"] + datos["cuota_obra_social"] + datos["cuota_jubilacion"]
        cats_html += f"""
<div class="cat-card {active}">
  <div class="cat-name">Cat. {cat}</div>
  <div class="cat-label">Hasta {fmt(datos['tope_anual'])}/año</div>
  <div style="margin-top:6px;color:#c4a6ff;font-weight:600;">{fmt(total)}/mes</div>
</div>"""

    return f"""
<div class="tia-result">
  <h3>📊 Tu categoría de Monotributo</h3>
  <p>Con una facturación mensual de <span class="highlight">{fmt(fac_mensual)}</span>
  tu facturación anual estimada es <span class="highlight">{fmt(r['facturacion_anual'])}</span>.</p>
  <p>Te corresponde la <span class="highlight" style="font-size:1.1rem">Categoría {r['categoria']}</span>
  (tope anual: {fmt(r['tope_anual'])})</p>

  <div style="margin:16px 0 6px;font-size:0.78rem;color:#7c4dcc;text-transform:uppercase;letter-spacing:0.1em;">Desglose de la cuota mensual</div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:16px;">
    <div style="background:#1a1028;border:1px solid #2c204a;border-radius:8px;padding:12px;text-align:center;">
      <div style="color:#6b5e85;font-size:0.72rem;margin-bottom:4px;">Impuesto integrado</div>
      <div style="color:#b07fff;font-weight:600;">{fmt(r['cuota_impuesto'])}</div>
    </div>
    <div style="background:#1a1028;border:1px solid #2c204a;border-radius:8px;padding:12px;text-align:center;">
      <div style="color:#6b5e85;font-size:0.72rem;margin-bottom:4px;">Obra Social</div>
      <div style="color:#b07fff;font-weight:600;">{fmt(r['cuota_obra_social'])}</div>
    </div>
    <div style="background:#1a1028;border:1px solid #2c204a;border-radius:8px;padding:12px;text-align:center;">
      <div style="color:#6b5e85;font-size:0.72rem;margin-bottom:4px;">Jubilación</div>
      <div style="color:#b07fff;font-weight:600;">{fmt(r['cuota_jubilacion'])}</div>
    </div>
  </div>
  <p style="font-size:1.05rem;">Cuota total mensual: <span class="highlight" style="font-size:1.2rem;">{fmt(r['cuota_total'])}</span></p>

  <div style="margin:20px 0 8px;font-size:0.78rem;color:#7c4dcc;text-transform:uppercase;letter-spacing:0.1em;">Mapa de categorías</div>
  <div class="cat-grid">{cats_html}</div>
  <div class="warn">⚠️ Valores orientativos 2025/2026. Verificá la RG AFIP vigente y consultá con un Contador Público matriculado.</div>
</div>"""


def html_margen(precio_venta, costo_producto, cuota_mono, alicuota_iibb, otros_gastos) -> str:
    r = calcular_margen(precio_venta, costo_producto, cuota_mono, alicuota_iibb, otros_gastos)
    color_neto = "#5eead4" if r["ganancia_neta"] >= 0 else "#f87171"

    barra_bruta = min(100, max(0, r["margen_bruto_pct"]))
    barra_neta  = min(100, max(0, r["margen_neto_pct"]))

    return f"""
<div class="tia-result">
  <h3>📐 Análisis de Margen</h3>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px;">
    <div style="background:#1a1028;border:1px solid #2c204a;border-radius:8px;padding:14px;">
      <div style="color:#6b5e85;font-size:0.72rem;margin-bottom:4px;">Precio de venta mensual</div>
      <div style="color:#e2e2e8;font-weight:600;">{fmt(r['precio_venta'])}</div>
    </div>
    <div style="background:#1a1028;border:1px solid #2c204a;border-radius:8px;padding:14px;">
      <div style="color:#6b5e85;font-size:0.72rem;margin-bottom:4px;">Costo del producto</div>
      <div style="color:#e2e2e8;font-weight:600;">{fmt(r['costo_producto'])}</div>
    </div>
    <div style="background:#1a1028;border:1px solid #2c204a;border-radius:8px;padding:14px;">
      <div style="color:#6b5e85;font-size:0.72rem;margin-bottom:4px;">IIBB mensual estimado</div>
      <div style="color:#f0b429;font-weight:600;">{fmt(r['iibb_mensual'])}</div>
    </div>
    <div style="background:#1a1028;border:1px solid #2c204a;border-radius:8px;padding:14px;">
      <div style="color:#6b5e85;font-size:0.72rem;margin-bottom:4px;">Cuota Monotributo</div>
      <div style="color:#f0b429;font-weight:600;">{fmt(r['cuota_monotributo'])}</div>
    </div>
  </div>

  <div style="margin:10px 0;">
    <div style="display:flex;justify-content:space-between;font-size:0.8rem;color:#8b7fb0;margin-bottom:4px;">
      <span>Margen Bruto</span><span class="highlight">{r['margen_bruto_pct']:.1f}%</span>
    </div>
    <div style="background:#2c204a;border-radius:4px;height:8px;">
      <div style="background:#b07fff;width:{barra_bruta}%;height:100%;border-radius:4px;transition:width 0.5s;"></div>
    </div>
  </div>
  <div style="margin:10px 0 18px;">
    <div style="display:flex;justify-content:space-between;font-size:0.8rem;color:#8b7fb0;margin-bottom:4px;">
      <span>Margen Neto Real</span><span style="color:{color_neto};font-weight:600;">{r['margen_neto_pct']:.1f}%</span>
    </div>
    <div style="background:#2c204a;border-radius:4px;height:8px;">
      <div style="background:{color_neto};width:{barra_neta}%;height:100%;border-radius:4px;transition:width 0.5s;"></div>
    </div>
  </div>

  <p style="font-size:1.1rem;">Ganancia neta mensual: <span style="color:{color_neto};font-size:1.25rem;font-weight:700;">{fmt(r['ganancia_neta'])}</span></p>

  {"<p style='color:#f87171;'>⚠️ Tu margen neto es negativo. Revisá tus costos o tu precio de venta.</p>" if r['ganancia_neta'] < 0 else ""}

  <div class="warn">⚠️ Este análisis es orientativo. La alícuota de IIBB, deducciones y otros factores pueden variar. Consultá con un Contador Público.</div>
</div>"""


def html_concepto(concepto: str) -> str:
    texto = CONCEPTOS_DICT.get(concepto, "Concepto no encontrado.")
    return f"""
<div class="tia-result">
  <h3>📚 {concepto}</h3>
  <div style="line-height:1.8;">{texto}</div>
  <div class="warn">⚠️ Esta explicación es educativa y general. Para tu situación puntual, consultá con un Contador Público matriculado.</div>
</div>"""


def html_calendario() -> str:
    items = ""
    for mes_num, evento in VENCIMIENTOS.items():
        current = "current" if mes_num == MES_ACTUAL else ""
        items += f"""
<div class="cal-item {current}">
  <div class="mes">{MESES[mes_num-1]}</div>
  <div class="evento">{evento}</div>
</div>"""
    return f"""
<div class="tia-result">
  <h3>📅 Calendario de Vencimientos Fiscales</h3>
  <p style="color:#8b7fb0;font-size:0.85rem;">Los meses resaltados corresponden al mes actual. Fechas exactas según AFIP.</p>
  <div class="cal-grid">{items}</div>
  <div class="warn">⚠️ Las fechas exactas varían según tu CUIT y la RG AFIP del período. Confirmá siempre en afip.gob.ar.</div>
</div>"""


# ════════════════════════════════════════════════════════════
#  INTERFAZ PRINCIPAL
# ════════════════════════════════════════════════════════════

def construir_ui():
    display(HTML(ESTILOS))

    # — HEADER —
    display(HTML(f"""
<div class="tia-root">
  <div class="tia-header">
    <div class="tia-badge">Trabajo Final IA · Gabriel Poli</div>
    <h1>Tribut-IA 🤖</h1>
    <p>Asistente conversacional para la educación financiera y fiscal de jóvenes emprendedores argentinos</p>
  </div>
</div>
"""))

    output_area = widgets.Output()

    # ── TAB 1: Categoría Monotributo ─────────────────────────

    lbl_fac = widgets.HTML("<div class='tia-section-title'>Facturación promedio mensual ($)</div>")
    inp_fac = widgets.BoundedFloatText(
        value=500_000, min=1, max=999_999_999,
        step=10_000,
        layout=widgets.Layout(width="260px"),
        style={"description_width": "0px"},
    )
    btn_cat = widgets.Button(
        description="Calcular mi categoría →",
        button_style="",
        style={"button_color": "#7c4dcc", "font_weight": "bold"},
        layout=widgets.Layout(margin="10px 0 0"),
    )

    def on_calcular_cat(_):
        with output_area:
            clear_output(wait=True)
            display(HTML(html_monotributo(inp_fac.value)))

    btn_cat.on_click(on_calcular_cat)

    tab1 = widgets.VBox([
        widgets.HTML("<div class='tia-section'><div class='tia-section-title'>Calculadora de Categoría Monotributo</div></div>"),
        widgets.HBox([
            widgets.VBox([lbl_fac, inp_fac, btn_cat],
                         layout=widgets.Layout(padding="0 24px")),
        ]),
    ])

    # ── TAB 2: Margen de Ganancia ────────────────────────────

    def labeled(label, widget):
        return widgets.VBox([
            widgets.HTML(f"<div class='tia-section-title' style='padding:0;margin-bottom:4px;'>{label}</div>"),
            widget
        ])

    inp_pv   = widgets.BoundedFloatText(value=1_000_000, min=1, max=999_999_999, step=10_000,
                                         layout=widgets.Layout(width="200px"))
    inp_cp   = widgets.BoundedFloatText(value=500_000,   min=0, max=999_999_999, step=10_000,
                                         layout=widgets.Layout(width="200px"))
    inp_mono = widgets.BoundedFloatText(value=27_371,    min=0, max=999_999_999, step=1_000,
                                         layout=widgets.Layout(width="200px"))
    inp_og   = widgets.BoundedFloatText(value=50_000,    min=0, max=999_999_999, step=5_000,
                                         layout=widgets.Layout(width="200px"))

    prov_opciones = list(ALICUOTAS_IIBB.keys())
    dd_prov = widgets.Dropdown(
        options=prov_opciones,
        value="Santa Fe",
        layout=widgets.Layout(width="200px"),
    )
    dd_tipo = widgets.Dropdown(
        options=["comercio", "servicios"],
        value="comercio",
        layout=widgets.Layout(width="200px"),
    )
    btn_margen = widgets.Button(
        description="Calcular margen →",
        style={"button_color": "#7c4dcc", "font_weight": "bold"},
        layout=widgets.Layout(margin="14px 0 0"),
    )

    def on_calcular_margen(_):
        iibb_rate = ALICUOTAS_IIBB[dd_prov.value][dd_tipo.value]
        with output_area:
            clear_output(wait=True)
            display(HTML(html_margen(inp_pv.value, inp_cp.value,
                                     inp_mono.value, iibb_rate, inp_og.value)))

    btn_margen.on_click(on_calcular_margen)

    tab2 = widgets.VBox([
        widgets.HTML("<div class='tia-section'><div class='tia-section-title'>Calculadora de Margen de Ganancia</div></div>"),
        widgets.GridBox(
            [
                labeled("Ventas mensuales ($)", inp_pv),
                labeled("Costo del producto ($)", inp_cp),
                labeled("Cuota Monotributo ($)", inp_mono),
                labeled("Otros gastos fijos ($)", inp_og),
                labeled("Provincia", dd_prov),
                labeled("Tipo de actividad", dd_tipo),
            ],
            layout=widgets.Layout(
                grid_template_columns="repeat(3, 220px)",
                gap="12px",
                padding="0 24px",
            ),
        ),
        widgets.HBox([btn_margen], layout=widgets.Layout(padding="0 24px")),
    ])

    # ── TAB 3: Glosario / Conceptos ─────────────────────────

    dd_concepto = widgets.Dropdown(
        options=list(CONCEPTOS_DICT.keys()),
        value="Monotributo",
        layout=widgets.Layout(width="280px"),
    )
    btn_concepto = widgets.Button(
        description="Explicame este concepto →",
        style={"button_color": "#7c4dcc", "font_weight": "bold"},
        layout=widgets.Layout(margin="10px 0 0"),
    )

    def on_concepto(_):
        with output_area:
            clear_output(wait=True)
            display(HTML(html_concepto(dd_concepto.value)))

    btn_concepto.on_click(on_concepto)

    tab3 = widgets.VBox([
        widgets.HTML("<div class='tia-section'><div class='tia-section-title'>Glosario Fiscal — ¿Qué significa esto?</div></div>"),
        widgets.VBox([dd_concepto, btn_concepto], layout=widgets.Layout(padding="0 24px")),
    ])

    # ── TAB 4: Calendario ────────────────────────────────────

    btn_cal = widgets.Button(
        description="Ver calendario de vencimientos →",
        style={"button_color": "#7c4dcc", "font_weight": "bold"},
        layout=widgets.Layout(margin="10px 0 0"),
    )

    def on_cal(_):
        with output_area:
            clear_output(wait=True)
            display(HTML(html_calendario()))

    btn_cal.on_click(on_cal)

    tab4 = widgets.VBox([
        widgets.HTML("<div class='tia-section'><div class='tia-section-title'>Calendario de Vencimientos Fiscales</div></div>"),
        widgets.VBox([
            widgets.HTML("<div style='padding:0 24px;color:#8b7fb0;font-size:0.85rem;'>Visualizá los vencimientos más importantes del año fiscal argentino.</div>"),
            widgets.HBox([btn_cal], layout=widgets.Layout(padding="0 24px")),
        ]),
    ])

    # ── TABS COMBINADOS ──────────────────────────────────────

    tabs = widgets.Tab()
    tabs.children = [tab1, tab2, tab3, tab4]
    tabs.set_title(0, "📊 Monotributo")
    tabs.set_title(1, "📐 Márgenes")
    tabs.set_title(2, "📚 Glosario")
    tabs.set_title(3, "📅 Vencimientos")

    display(HTML("""<div class="tia-root" style="margin-top:12px;">
<div style="padding:16px 24px 0;border-bottom:1px solid #2c204a;">"""))
    display(tabs)
    display(HTML("""</div></div>"""))

    display(output_area)

    display(HTML("""
<div class="tia-root" style="margin-top:12px;padding:16px 24px;">
  <p style="color:#6b5e85;font-size:0.78rem;text-align:center;margin:0;">
    ⚠️ <strong>Aviso legal:</strong> Tribut-IA es una herramienta educativa e informativa.
    No reemplaza la asesoría de un Contador Público matriculado.
    Toda decisión patrimonial debe ser validada por un profesional habilitado.<br>
    Proyecto académico · MOT Inteligencia Artificial · UCA Rosario · Gabriel Poli
  </p>
</div>
"""))

# ════════════════════════════════════════════════════════════
#  PUNTO DE ENTRADA
# ════════════════════════════════════════════════════════════

construir_ui()

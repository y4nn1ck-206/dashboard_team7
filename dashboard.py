# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ── Pagina configuratie ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="HARTstikke Gezond",
    page_icon=":anatomical_heart:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Styling ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #F5F7FA; }
    [data-testid="stSidebar"] { background-color: #1A2B4A; }

    .topbar {
        background: white;
        border-radius: 14px;
        padding: 18px 24px;
        margin-bottom: 16px;
        border: 1px solid #E8ECF0;
    }
    .page-title { font-size: 22px; font-weight: 700; color: #1A2B4A; margin: 0; }
    .page-sub { font-size: 13px; color: #8A94A6; margin: 2px 0 0 0; }

    .kpi-card {
        background: white;
        border-radius: 14px;
        padding: 20px 22px;
        border: 1px solid #E8ECF0;
        height: 100%;
    }
    .kpi-label {
        font-size: 12px;
        color: #8A94A6;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.4px;
        margin-bottom: 6px;
    }
    .kpi-value { font-size: 32px; font-weight: 700; color: #1A2B4A; line-height: 1; }
    .kpi-delta-up { font-size: 12px; color: #10B981; margin-top: 5px; font-weight: 500; }
    .kpi-delta-down { font-size: 12px; color: #EF4444; margin-top: 5px; font-weight: 500; }
    .kpi-delta-neu { font-size: 12px; color: #8A94A6; margin-top: 5px; }

    .card {
        background: white;
        border-radius: 14px;
        padding: 20px 22px;
        border: 1px solid #E8ECF0;
        margin-bottom: 14px;
    }
    .card-title { font-size: 15px; font-weight: 600; color: #1A2B4A; margin-bottom: 2px; }
    .card-sub { font-size: 12px; color: #8A94A6; margin-bottom: 14px; }

    .wijk-row {
        display: flex;
        align-items: center;
        padding: 9px 0;
        border-bottom: 1px solid #F1F4F8;
    }
    .wijk-row:last-child { border-bottom: none; }
    .wijk-name { font-size: 13px; color: #1A2B4A; font-weight: 500; min-width: 130px; }
    .wijk-val { font-size: 13px; color: #1A2B4A; min-width: 55px; }
    .chip { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 20px; }
    .chip-up { background: #ECFDF5; color: #059669; }
    .chip-down { background: #FEF2F2; color: #DC2626; }

    .insight {
        background: #EFF6FF;
        border-radius: 10px;
        padding: 10px 14px;
        font-size: 12px;
        color: #1D4ED8;
        margin-top: 12px;
    }
    .footer-bar {
        background: white;
        border-radius: 14px;
        padding: 12px 20px;
        border: 1px solid #E8ECF0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 4px;
    }
    .footer-hint { font-size: 12px; color: #8A94A6; }
</style>
""", unsafe_allow_html=True)

# ── Kleuren ───────────────────────────────────────────────────────────────────
BLAUW = "#1A2B4A"
LICHTBLAUW = "#3B82F6"
GROEN = "#10B981"
ROOD = "#EF4444"
GRIJS = "#8A94A6"

# ── Data ─────────────────────────────────────────────────────────────────────
# !! VERVANG LATER MET ECHTE CSV !!
# Verwacht kolommen: wijk, datum, hartslag, stappen, ecg_normaal_pct
# df = pd.read_csv("jouw_data.csv")

wijken_data = {
    "Slotervaart":    {"deelname": 520, "groei": 20,  "hartslag": 68, "h_delta": -2, "stappen": 8942, "s_delta": 12, "sensoren": 12},
    "Indische Buurt": {"deelname": 450, "groei": 5,   "hartslag": 66, "h_delta": -1, "stappen": 8112, "s_delta": 6,  "sensoren": 9},
    "Bos en Lommer":  {"deelname": 410, "groei": 3,   "hartslag": 64, "h_delta": -1, "stappen": 7542, "s_delta": 3,  "sensoren": 8},
    "Bijlmer":        {"deelname": 320, "groei": -2,  "hartslag": 63, "h_delta": -3, "stappen": 6892, "s_delta": -2, "sensoren": 7},
    "Slotermeer":     {"deelname": 250, "groei": -8,  "hartslag": 62, "h_delta": -2, "stappen": 6102, "s_delta": -8, "sensoren": 6},
}

trend_weken = ["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8"]

detail_data = {
    "Slotervaart": {
        "trend_deel": [310, 350, 390, 420, 460, 490, 510, 520],
        "trend_stap": [7800, 8000, 8100, 8300, 8500, 8700, 8900, 8942],
        "ecg": {"Normaal sinusritme": 87, "Onregelmatig ritme": 8, "Bradycardie": 3, "Tachycardie": 2}
    },
    "Indische Buurt": {
        "trend_deel": [360, 370, 390, 400, 410, 430, 440, 450],
        "trend_stap": [7500, 7600, 7700, 7800, 7900, 8000, 8050, 8112],
        "ecg": {"Normaal sinusritme": 91, "Onregelmatig ritme": 5, "Bradycardie": 2, "Tachycardie": 2}
    },
    "Bos en Lommer": {
        "trend_deel": [340, 350, 360, 370, 385, 395, 405, 410],
        "trend_stap": [7000, 7100, 7150, 7200, 7300, 7400, 7500, 7542],
        "ecg": {"Normaal sinusritme": 83, "Onregelmatig ritme": 10, "Bradycardie": 5, "Tachycardie": 2}
    },
    "Bijlmer": {
        "trend_deel": [340, 345, 340, 335, 330, 325, 322, 320],
        "trend_stap": [7100, 7050, 7000, 6950, 6900, 6920, 6900, 6892],
        "ecg": {"Normaal sinusritme": 79, "Onregelmatig ritme": 12, "Bradycardie": 6, "Tachycardie": 3}
    },
    "Slotermeer": {
        "trend_deel": [290, 285, 278, 270, 265, 258, 253, 250],
        "trend_stap": [6700, 6600, 6500, 6400, 6350, 6250, 6150, 6102],
        "ecg": {"Normaal sinusritme": 81, "Onregelmatig ritme": 11, "Bradycardie": 5, "Tachycardie": 3}
    },
}

# ── Session state ─────────────────────────────────────────────────────────────
if "geselecteerde_wijk" not in st.session_state:
    st.session_state["geselecteerde_wijk"] = None

# ═══════════════════════════════════════════════════════════════════════════════
# DETAIL VIEW
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state["geselecteerde_wijk"] is not None:
    wijk = st.session_state["geselecteerde_wijk"]
    d = wijken_data[wijk]
    det = detail_data[wijk]

    col_back, col_title = st.columns([1, 8])
    with col_back:
        if st.button("Terug"):
            st.session_state["geselecteerde_wijk"] = None
            st.rerun()
    with col_title:
        st.markdown(
            "<p class='page-title'>Wijk: " + wijk + "</p>"
            "<p class='page-sub'>Detailweergave ECG, beweging en deelname</p>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # KPI rij
    k1, k2, k3, k4 = st.columns(4)
    g_kleur = "kpi-delta-up" if d["groei"] >= 0 else "kpi-delta-down"
    g_teken = "+" if d["groei"] >= 0 else ""
    s_kleur = "kpi-delta-up" if d["s_delta"] >= 0 else "kpi-delta-down"
    s_teken = "+" if d["s_delta"] >= 0 else ""
    ecg_norm = det["ecg"]["Normaal sinusritme"]
    ecg_kleur = "kpi-delta-up" if ecg_norm >= 80 else "kpi-delta-down"

    with k1:
        st.markdown(
            "<div class='kpi-card'>"
            "<div class='kpi-label'>Actieve deelnemers</div>"
            "<div class='kpi-value'>" + str(d["deelname"]) + "</div>"
            "<div class='" + g_kleur + "'>" + g_teken + str(d["groei"]) + "% t.o.v. vorige week</div>"
            "</div>",
            unsafe_allow_html=True
        )
    with k2:
        st.markdown(
            "<div class='kpi-card'>"
            "<div class='kpi-label'>Sensoren uitgeleend</div>"
            "<div class='kpi-value'>" + str(d["sensoren"]) + "</div>"
            "<div class='kpi-delta-neu'>via OBA locatie</div>"
            "</div>",
            unsafe_allow_html=True
        )
    with k3:
        st.markdown(
            "<div class='kpi-card'>"
            "<div class='kpi-label'>ECG normaal ritme</div>"
            "<div class='kpi-value'>" + str(ecg_norm) + "%</div>"
            "<div class='" + ecg_kleur + "'>van alle ECG-metingen</div>"
            "</div>",
            unsafe_allow_html=True
        )
    with k4:
        st.markdown(
            "<div class='kpi-card'>"
            "<div class='kpi-label'>Gem. dagelijkse stappen</div>"
            "<div class='kpi-value'>" + f"{d['stappen']:,}" + "</div>"
            "<div class='" + s_kleur + "'>" + s_teken + str(d["s_delta"]) + "% t.o.v. vorige week</div>"
            "</div>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Trend grafieken
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            "<div class='card'><div class='card-title'>Deelname trend</div>"
            "<div class='card-sub'>Actieve deelnemers afgelopen 8 weken</div>",
            unsafe_allow_html=True
        )
        fig = go.Figure(go.Scatter(
            x=trend_weken, y=det["trend_deel"],
            mode="lines+markers",
            line=dict(color=BLAUW, width=2.5),
            marker=dict(size=5),
            fill="tozeroy",
            fillcolor="rgba(26,43,74,0.07)"
        ))
        fig.update_layout(
            height=200, margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="white", plot_bgcolor="white",
            xaxis=dict(showgrid=False, tickfont=dict(size=11)),
            yaxis=dict(showgrid=True, gridcolor="#F1F4F8", tickfont=dict(size=11)),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown(
            "<div class='card'><div class='card-title'>Bewegingstrend</div>"
            "<div class='card-sub'>Gemiddelde dagelijkse stappen per week</div>",
            unsafe_allow_html=True
        )
        fig2 = go.Figure(go.Scatter(
            x=trend_weken, y=det["trend_stap"],
            mode="lines+markers",
            line=dict(color=GROEN, width=2.5),
            marker=dict(size=5, color=GROEN),
            fill="tozeroy",
            fillcolor="rgba(16,185,129,0.07)"
        ))
        fig2.update_layout(
            height=200, margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="white", plot_bgcolor="white",
            xaxis=dict(showgrid=False, tickfont=dict(size=11)),
            yaxis=dict(showgrid=True, gridcolor="#F1F4F8", tickfont=dict(size=11), tickformat=","),
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ECG tabel
    st.markdown(
        "<div class='card'><div class='card-title'>ECG-indicatoren</div>"
        "<div class='card-sub'>Verdeling hartritme-categorieen in deze wijk</div>",
        unsafe_allow_html=True
    )
    ecg_df = pd.DataFrame([
        {
            "Type": k,
            "Aandeel (%)": v,
            "Status": "Normaal" if k == "Normaal sinusritme" and v >= 80
                      else ("Let op" if v > 10 else "Laag risico")
        }
        for k, v in det["ecg"].items()
    ])
    st.dataframe(ecg_df, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='footer-bar'>"
        "<div class='footer-hint'>Klik op Terug voor het wijkoverzicht</div>"
        "<div class='footer-hint'>Laatst bijgewerkt: vandaag 10:30</div>"
        "</div>",
        unsafe_allow_html=True
    )

# ═══════════════════════════════════════════════════════════════════════════════
# OVERZICHT VIEW
# ═══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown(
        "<div class='topbar'>"
        "<p class='page-title'>Overzicht alle wijken</p>"
        "<p class='page-sub'>Inzicht in deelname en bewegingspatronen per wijk</p>"
        "</div>",
        unsafe_allow_html=True
    )

    # KPI rij
    totaal_deel = sum(d["deelname"] for d in wijken_data.values())
    totaal_sensor = sum(d["sensoren"] for d in wijken_data.values())
    gem_groei = round(np.mean([d["groei"] for d in wijken_data.values()]), 1)
    g_teken = "+" if gem_groei >= 0 else ""

    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(
            "<div class='kpi-card'>"
            "<div class='kpi-label'>Actieve deelnemers deze week</div>"
            "<div class='kpi-value'>" + str(totaal_deel) + "</div>"
            "<div class='kpi-delta-up'>+63 t.o.v. vorige week</div>"
            "</div>",
            unsafe_allow_html=True
        )
    with k2:
        st.markdown(
            "<div class='kpi-card'>"
            "<div class='kpi-label'>Gemiddelde groei alle wijken</div>"
            "<div class='kpi-value'>" + g_teken + str(gem_groei) + "%</div>"
            "<div class='kpi-delta-up'>over alle 5 wijken</div>"
            "</div>",
            unsafe_allow_html=True
        )
    with k3:
        st.markdown(
            "<div class='kpi-card'>"
            "<div class='kpi-label'>Sensoren uitgeleend (OBA)</div>"
            "<div class='kpi-value'>" + str(totaal_sensor) + "</div>"
            "<div class='kpi-delta-neu'>verspreid over alle wijken</div>"
            "</div>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])

    with col_left:
        # Staafdiagram
        st.markdown(
            "<div class='card'><div class='card-title'>Deelname per wijk</div>"
            "<div class='card-sub'>Aantal actieve deelnemers deze week</div>",
            unsafe_allow_html=True
        )
        namen = list(wijken_data.keys())
        waarden = [wijken_data[w]["deelname"] for w in namen]
        max_groei = max(wijken_data[w]["groei"] for w in namen)
        kleuren = [
            BLAUW if wijken_data[w]["groei"] == max_groei
            else LICHTBLAUW if wijken_data[w]["groei"] > 0
            else "#A8BFDF"
            for w in namen
        ]
        fig_bar = go.Figure(go.Bar(
            x=namen, y=waarden,
            marker_color=kleuren,
            text=waarden,
            textposition="outside",
            textfont=dict(size=12, color=BLAUW)
        ))
        fig_bar.update_layout(
            height=260, margin=dict(l=0, r=0, t=10, b=0),
            paper_bgcolor="white", plot_bgcolor="white",
            xaxis=dict(showgrid=False, tickfont=dict(size=11)),
            yaxis=dict(showgrid=True, gridcolor="#F1F4F8", tickfont=dict(size=11), range=[0, max(waarden) * 1.15]),
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        beste = max(wijken_data, key=lambda w: wijken_data[w]["groei"])
        st.markdown(
            "<div class='insight'>"
            + beste + " heeft de grootste groei deze week (+" + str(wijken_data[beste]["groei"]) + "%)"
            + "</div>",
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Trend grafiek
        st.markdown(
            "<div class='card'><div class='card-title'>Trends over tijd</div>"
            "<div class='card-sub'>Deelname alle wijken - afgelopen 8 weken</div>",
            unsafe_allow_html=True
        )
        trend_kleuren = [BLAUW, GROEN, "#F59E0B", ROOD, GRIJS]
        fig_trend = go.Figure()
        for i, (naam, det) in enumerate(detail_data.items()):
            fig_trend.add_trace(go.Scatter(
                x=trend_weken, y=det["trend_deel"],
                mode="lines", name=naam,
                line=dict(color=trend_kleuren[i], width=2),
                hovertemplate=naam + ": %{y}<extra></extra>"
            ))
        fig_trend.update_layout(
            height=180, margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="white", plot_bgcolor="white",
            xaxis=dict(showgrid=False, tickfont=dict(size=11)),
            yaxis=dict(showgrid=True, gridcolor="#F1F4F8", tickfont=dict(size=11)),
            legend=dict(font=dict(size=10), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        # Hartslag tabel
        st.markdown(
            "<div class='card'><div class='card-title'>Hartslag gemiddeld per wijk</div>"
            "<div class='card-sub'>Gemiddelde hartslag (bpm)</div>",
            unsafe_allow_html=True
        )
        for naam, d in wijken_data.items():
            delta = d["h_delta"]
            chip = "chip-down" if delta < 0 else "chip-up"
            chip_txt = str(delta) + " bpm" if delta < 0 else "+" + str(delta) + " bpm"
            st.markdown(
                "<div class='wijk-row'>"
                "<span class='wijk-name'>" + naam + "</span>"
                "<span class='wijk-val'>" + str(d["hartslag"]) + "</span>"
                "<span style='flex:1'></span>"
                "<span class='chip " + chip + "'>" + chip_txt + "</span>"
                "</div>",
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)

        # Beweging tabel
        st.markdown(
            "<div class='card'><div class='card-title'>Bewegingspatronen per wijk</div>"
            "<div class='card-sub'>Gemiddelde dagelijkse stappen</div>",
            unsafe_allow_html=True
        )
        for naam, d in wijken_data.items():
            delta = d["s_delta"]
            chip = "chip-up" if delta > 0 else "chip-down"
            chip_txt = "+" + str(delta) + "%" if delta > 0 else str(delta) + "%"
            st.markdown(
                "<div class='wijk-row'>"
                "<span class='wijk-name'>" + naam + "</span>"
                "<span class='wijk-val'>" + f"{d['stappen']:,}" + "</span>"
                "<span style='flex:1'></span>"
                "<span class='chip " + chip + "'>" + chip_txt + "</span>"
                "</div>",
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)

        # Doorklik knoppen
        st.markdown(
            "<div class='card'><div class='card-title'>Bekijk wijk in detail</div>"
            "<div class='card-sub'>Klik voor ECG-data, trends en meer</div>",
            unsafe_allow_html=True
        )
        for naam in wijken_data.keys():
            groei = wijken_data[naam]["groei"]
            teken = "+" if groei >= 0 else ""
            if st.button(naam + "  " + teken + str(groei) + "%", key="btn_" + naam):
                st.session_state["geselecteerde_wijk"] = naam
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='footer-bar'>"
        "<div class='footer-hint'>Klik op een wijk voor meer details</div>"
        "<div class='footer-hint'>Laatst bijgewerkt: vandaag 10:30</div>"
        "</div>",
        unsafe_allow_html=True
    )
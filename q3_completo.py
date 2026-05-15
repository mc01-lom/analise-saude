import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

C_PORTO = "#02036C"
C_3778  = "#FF6200"
BG      = "#F8F9FA"
WH      = "white"

plt.rcParams.update({
    "font.family":      "DejaVu Sans",
    "axes.facecolor":   BG,
    "figure.facecolor": WH,
    "axes.spines.top":  False,
    "axes.spines.right":False,
    "axes.grid":        True,
    "grid.alpha":       0.3,
    "grid.linestyle":   "--",
})

SEM_MES     = 4.333
FATOR_PJ    = 1.40
FATOR_CUSTO = 1.83

data = [
    (1,"Médico","SP","3778","PJ",40,43813.74),
    (2,"Médico","RJ","3778","PJ",30,19636.04),
    (3,"Médico","RJ","3778","PJ",30,26578.09),
    (4,"Médico","RJ","3778","PJ",30,27364.31),
    (5,"Médico","RJ","3778","PJ",16,13404.47),
    (6,"Médico","MG","3778","PJ",40,38270.32),
    (7,"Médico","DF","3778","PJ",12,12534.95),
    (8,"Médico","RJ","3778","PJ", 8, 6433.64),
    (9,"Médico","MG","3778","PJ", 4, 3952.17),
    (10,"Médico","RJ","3778","PJ", 4, 3460.68),
    (11,"Médico","AL","Porto","PJ", 4, 3967.00),
    (12,"Médico","PE","Porto","PJ", 4, 8009.57),
    (13,"Médico","ES","Porto","PJ", 4, 7795.18),
    (14,"Enfermeiro","PR","Porto","CLT",40,13956.04),
    (15,"Enfermeiro","BA","Porto","CLT",40,17417.95),
    (16,"Enfermeiro","PE","Porto","CLT",40,21856.57),
    (17,"Enfermeiro","MG","Porto","CLT",40,14029.00),
    (18,"Médico","PR","Porto","CLT",40,55556.06),
    (19,"Médico","RS","Porto","CLT",40,48076.17),
    (20,"Médico","PE","Porto","CLT",40,42618.07),
    (21,"Médico","BA","Porto","CLT",40,66758.07),
    (22,"Médico","SP","Porto","CLT",40,60482.54),
    (23,"Médico","GO","Porto","CLT",40,26169.84),
    (24,"Engenheiro","MG","Porto","CLT",40,21772.03),
    (25,"Engenheiro","PR","Porto","CLT",40,12143.53),
    (26,"Engenheiro","RJ","Porto","CLT",40,21772.03),
    (27,"Engenheiro","RJ","Porto","CLT",40,12143.53),
    (28,"Téc.Segurança","BA","Porto","CLT",40,13973.14),
    (29,"Téc.Segurança","GO","Porto","CLT",40,13973.14),
    (30,"Téc.Segurança","MG","Porto","CLT",40,13973.14),
    (31,"Téc.Segurança","MG","Porto","CLT",40,13973.14),
    (32,"Téc.Segurança","PE","Porto","CLT",40,13973.14),
    (33,"Téc.Segurança","PR","Porto","CLT",40,13973.14),
    (34,"Téc.Segurança","RJ","Porto","CLT",40,13973.14),
    (35,"Téc.Segurança","RJ","Porto","CLT",40,13973.14),
    (36,"Téc.Segurança","RJ","Porto","CLT",40,13973.14),
    (37,"Téc.Segurança","RS","Porto","CLT",40,13973.14),
    (38,"Téc.Segurança","SP","Porto","CLT",40,13889.41),
    (39,"Téc.Segurança","SP","Porto","CLT",40,13889.41),
    (40,"Téc.Segurança","SP","Porto","CLT",40,13889.41),
    (41,"Téc.Segurança","SP","Porto","CLT",40,13889.41),
    (42,"Téc.Segurança","SP","Porto","CLT",40,13889.41),
    (43,"Téc.Segurança","SP","Porto","CLT",40,13889.41),
    (44,"Analista JR","SP","Porto","CLT",40,13476.00),
    (45,"Analista PL","SP","Porto","CLT",40,20975.00),
    (46,"Analista SR","SP","Porto","CLT",40,34505.00),
    (47,"Recepcionista","RJ","3778","PJ",40, 6942.05),
    (48,"Téc.Enfermagem","RJ","3778","CLT",40,10500.00),
    (49,"Enfermeiro","RJ","3778","CLT",30,11893.56),
    (50,"Enfermeiro","RJ","3778","CLT",40,14591.11),
    (51,"Enfermeiro","SP","3778","CLT",44,16704.62),
]

df = pd.DataFrame(data,
    columns=["id","cargo","uf","forn","reg","jh","custo"])
df["custo_hora"] = df["custo"] / (df["jh"] * SEM_MES)
df["rh_norm"] = df.apply(
    lambda r: r["custo_hora"] * FATOR_PJ if r["reg"]=="PJ" else r["custo_hora"],
    axis=1)

def brl(x):
    return f"R$ {x:,.0f}".replace(",","X").replace(".",",").replace("X",".")

UF_REGIAO = {
    "SP":"Sudeste","RJ":"Sudeste","MG":"Sudeste","ES":"Sudeste",
    "BA":"Nordeste","PE":"Nordeste","AL":"Nordeste","SE":"Nordeste",
    "PR":"Sul","RS":"Sul","SC":"Sul",
    "GO":"Centro-Oeste","DF":"Centro-Oeste","MT":"Centro-Oeste","MS":"Centro-Oeste",
    "AM":"Norte","PA":"Norte","AC":"Norte","RO":"Norte",
    "RR":"Norte","AP":"Norte","TO":"Norte",
}

# Benchmarks: cargo → (jornada_ref, {regiao: salario})
BENCHMARKS = {
    "Médico": (30, {
        "Norte":17140,"Nordeste":12896,"Sul":15697,
        "Sudeste":15286,"Centro-Oeste":14241,
    }),
    "Engenheiro": (41, {
        "Norte":13928,"Nordeste":12758,"Sul":12705,
        "Sudeste":14314,"Centro-Oeste":12641,
    }),
    "Enfermeiro": (41, {
        "Norte":5459,"Nordeste":5706,"Sul":6313,
        "Sudeste":6419,"Centro-Oeste":6319,
    }),
    "Téc.Enfermagem": (42, {
        "Norte":4153,"Nordeste":3896,"Sul":3985,
        "Sudeste":4155,"Centro-Oeste":4083,
    }),
    "Téc.Segurança": (43, {
        "Norte":4515,"Nordeste":3868,"Sul":4502,
        "Sudeste":4992,"Centro-Oeste":4511,
    }),
    "Analista JR": (40, {"SP_direto": 4000}),
    "Analista PL": (40, {"SP_direto": 6136}),
    "Analista SR": (40, {"SP_direto": 8132}),
}

CARGO_TITULOS = {
    "Médico":        "Médico do Trabalho",
    "Engenheiro":    "Engenheiro de Segurança do Trabalho",
    "Enfermeiro":    "Enfermeiro do Trabalho",
    "Téc.Enfermagem":"Técnico de Enfermagem do Trabalho",
    "Téc.Segurança": "Técnico em Segurança do Trabalho",
    "Analista JR":   "Analista de Projetos JR",
    "Analista PL":   "Analista de Projetos PL",
    "Analista SR":   "Analista de Projetos SR",
}

CARGO_CORES = {
    "Médico":        C_PORTO,
    "Engenheiro":    "#8E44AD",
    "Enfermeiro":    C_3778,
    "Téc.Enfermagem":"#D4AC0D",
    "Téc.Segurança": "#117A65",
    "Analista JR":   "#AED6F1",
    "Analista PL":   "#2E86C1",
    "Analista SR":   "#1A5276",
}

def get_mercado(cargo, uf):
    if cargo not in BENCHMARKS: return np.nan
    jh_ref, regioes = BENCHMARKS[cargo]
    # direto por UF (Analistas)
    if "SP_direto" in regioes:
        return round(regioes["SP_direto"] / (jh_ref * SEM_MES) * FATOR_CUSTO, 1) \
               if uf == "SP" else np.nan
    # por região
    reg = UF_REGIAO.get(uf)
    if not reg or reg not in regioes: return np.nan
    return round(regioes[reg] / (jh_ref * SEM_MES) * FATOR_CUSTO, 1)

# ── Gráfico por cargo ────────────────────────────────────────────────────────
# Analistas agrupados em um único gráfico
cargos_individuais = ["Médico","Engenheiro","Enfermeiro","Téc.Enfermagem","Téc.Segurança"]
cargos_analistas   = ["Analista JR","Analista PL","Analista SR"]

def plot_cargo(cargo_list, fname, titulo_geral=None, agrupar=False):
    if agrupar:
        # todos no mesmo gráfico (analistas)
        rows = []
        for cargo in cargo_list:
            sub = df[df.cargo==cargo]
            if sub.empty: continue
            jh_ref = BENCHMARKS[cargo][0]
            for uf, grp in sub.groupby("uf"):
                contrato = grp["rh_norm"].median()
                mercado  = get_mercado(cargo, uf)
                if np.isnan(mercado): continue
                gap = (contrato - mercado) / mercado * 100
                rows.append({"cargo":cargo,"uf":uf,
                             "mercado":mercado,"contrato":contrato,"gap_pct":gap})
        if not rows: return
        comp = pd.DataFrame(rows).sort_values("gap_pct", ascending=False)

        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        fig.suptitle(titulo_geral, fontsize=11, fontweight="bold", y=1.02)

        ax1, ax2 = axes
        x, w = np.arange(len(comp)), 0.35
        colors_b = [CARGO_CORES.get(c, "#566573") for c in comp["cargo"]]

        b1 = ax1.bar(x-w/2, comp["mercado"], width=w, color="#95A5A6",
                     edgecolor=WH, zorder=3, label="Referência mercado")
        b2 = ax1.bar(x+w/2, comp["contrato"], width=w, color=colors_b,
                     edgecolor=WH, zorder=3, label="Nosso contrato")
        for bar, val in zip(b1, comp["mercado"]):
            ax1.text(bar.get_x()+bar.get_width()/2, val+0.3,
                     f"R${val:.0f}", ha="center", va="bottom", fontsize=8.5, color="#566573")
        for bar, val in zip(b2, comp["contrato"]):
            ax1.text(bar.get_x()+bar.get_width()/2, val+0.3,
                     f"R${val:.0f}", ha="center", va="bottom",
                     fontsize=8.5, fontweight="bold")
        ax1.set_xticks(x)
        ax1.set_xticklabels(comp["cargo"], fontsize=9)
        ax1.set_ylabel("R$/hora"); ax1.legend(fontsize=9, frameon=False)
        ax1.set_title("Contrato vs. Referência de Mercado (R$/hora)", fontsize=10, pad=8)
        ax1.grid(axis="y", alpha=0.3); ax1.grid(axis="x", alpha=0)

        comp_s = comp.sort_values("gap_pct")
        bc = ["#E74C3C" if g>20 else "#27AE60" if g<-20 else "#F0B27A"
              for g in comp_s["gap_pct"]]
        ax2.barh(range(len(comp_s)), comp_s["gap_pct"],
                 color=bc, height=0.45, edgecolor=WH, zorder=3)
        ax2.axvline(0, color="#1C2833", lw=1.5)
        ax2.axvline(20,  color="#E74C3C", lw=1, ls="--", alpha=0.5)
        ax2.axvline(-20, color="#27AE60", lw=1, ls="--", alpha=0.5)
        for i, (_, row) in enumerate(comp_s.iterrows()):
            sinal = "+" if row["gap_pct"]>=0 else ""
            ha = "left" if row["gap_pct"]>=0 else "right"
            ax2.text(row["gap_pct"]+(0.5 if row["gap_pct"]>=0 else -0.5), i,
                     f"  {sinal}{row['gap_pct']:.0f}%", va="center", ha=ha,
                     fontsize=9, fontweight="bold",
                     color="#E74C3C" if row["gap_pct"]>20
                     else "#27AE60" if row["gap_pct"]<-20 else "#1C2833")
        ax2.set_yticks(range(len(comp_s)))
        ax2.set_yticklabels(comp_s["cargo"], fontsize=9)
        ax2.set_xlabel("Gap %")
        ax2.set_title("Gap % por Cargo", fontsize=10, pad=8)
        ax2.grid(axis="x", alpha=0.3); ax2.grid(axis="y", alpha=0)

    else:
        # gráfico individual por cargo
        cargo = cargo_list[0]
        color = CARGO_CORES.get(cargo, "#566573")
        jh_ref, regioes = BENCHMARKS[cargo]
        titulo = (f"Q3 · {CARGO_TITULOS[cargo]} — Contrato vs. Mercado por UF\n"
                  f"Mercado = salário mediana regional ({jh_ref}h) × fator custo total CLT 1,83×")

        sub = df[df.cargo==cargo]
        rows = []
        for uf, grp in sub.groupby("uf"):
            contrato = grp["rh_norm"].median()
            mercado  = get_mercado(cargo, uf)
            if np.isnan(mercado): continue
            gap = (contrato - mercado) / mercado * 100
            rows.append({"uf":uf,"regiao":UF_REGIAO.get(uf,""),
                         "mercado":mercado,"contrato":contrato,"gap_pct":gap})
        if not rows: return
        comp = pd.DataFrame(rows).sort_values("gap_pct", ascending=False)

        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        fig.suptitle(titulo, fontsize=11, fontweight="bold", y=1.02)

        ax1, ax2 = axes
        x, w = np.arange(len(comp)), 0.35
        b1 = ax1.bar(x-w/2, comp["mercado"], width=w, color="#95A5A6",
                     edgecolor=WH, zorder=3, label="Referência mercado")
        b2 = ax1.bar(x+w/2, comp["contrato"], width=w, color=color,
                     edgecolor=WH, zorder=3, label="Nosso contrato")
        for bar, val in zip(b1, comp["mercado"]):
            ax1.text(bar.get_x()+bar.get_width()/2, val+0.5,
                     f"R${val:.0f}", ha="center", va="bottom", fontsize=8, color="#566573")
        for bar, val in zip(b2, comp["contrato"]):
            ax1.text(bar.get_x()+bar.get_width()/2, val+0.5,
                     f"R${val:.0f}", ha="center", va="bottom",
                     fontsize=8, fontweight="bold", color=color)
        ax1.set_xticks(x); ax1.set_xticklabels(comp["uf"], fontsize=10)
        ax1.set_ylabel("R$/hora"); ax1.legend(fontsize=9, frameon=False)
        ax1.set_title("Contrato vs. Referência de Mercado (R$/hora)", fontsize=10, pad=8)
        ax1.grid(axis="y", alpha=0.3); ax1.grid(axis="x", alpha=0)

        comp_s = comp.sort_values("gap_pct")
        bc = ["#E74C3C" if g>20 else "#27AE60" if g<-20 else "#F0B27A"
              for g in comp_s["gap_pct"]]
        ax2.barh(range(len(comp_s)), comp_s["gap_pct"],
                 color=bc, height=0.5, edgecolor=WH, zorder=3)
        ax2.axvline(0, color="#1C2833", lw=1.5)
        ax2.axvline(20,  color="#E74C3C", lw=1, ls="--", alpha=0.5)
        ax2.axvline(-20, color="#27AE60", lw=1, ls="--", alpha=0.5)
        for i, (_, row) in enumerate(comp_s.iterrows()):
            sinal = "+" if row["gap_pct"]>=0 else ""
            ha = "left" if row["gap_pct"]>=0 else "right"
            reg = row.get("regiao","")
            ax2.text(row["gap_pct"]+(0.5 if row["gap_pct"]>=0 else -0.5), i,
                     f"  {sinal}{row['gap_pct']:.0f}%  ({reg})", va="center", ha=ha,
                     fontsize=9, fontweight="bold",
                     color="#E74C3C" if row["gap_pct"]>20
                     else "#27AE60" if row["gap_pct"]<-20 else "#1C2833")
        ax2.set_yticks(range(len(comp_s)))
        ax2.set_yticklabels(comp_s["uf"], fontsize=10)
        ax2.set_xlabel("Gap %")
        ax2.set_title("Gap % por UF\n(+) acima  |  (−) abaixo", fontsize=10, pad=8)
        ax2.grid(axis="x", alpha=0.3); ax2.grid(axis="y", alpha=0)

    plt.tight_layout()
    plt.savefig(fname, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ {fname}")

# ── Gera gráficos ────────────────────────────────────────────────────────────
for cargo in cargos_individuais:
    fname = f"g3_{cargo.lower().replace('.','').replace(' ','_')}.png"
    plot_cargo([cargo], fname)

plot_cargo(cargos_analistas, "g3_analistas.png", agrupar=True,
           titulo_geral="Q3 · Analistas de Projetos (SP) — Contrato vs. Mercado\n"
                        "Mercado = salário mediana SP (40h) × fator custo total CLT 1,83×")

print("\nQ3 concluída — 6 gráficos gerados.")

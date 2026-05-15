import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

# ── Paleta e estilo ──────────────────────────────────────────────────────────
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
FATOR_CUSTO = 1.83   # encargos CLT (1,59) × margem fornecedor (1,15)

# ── Dataset ──────────────────────────────────────────────────────────────────
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
df["custo_eq40"] = df["custo_hora"] * 40 * SEM_MES
df["custo_norm"] = df.apply(
    lambda r: r["custo_eq40"] * FATOR_PJ if r["reg"]=="PJ" else r["custo_eq40"], axis=1)
df["rh_norm"] = df.apply(
    lambda r: r["custo_hora"] * FATOR_PJ if r["reg"]=="PJ" else r["custo_hora"], axis=1)

def brl(x):
    return f"R$ {x:,.0f}".replace(",","X").replace(".",",").replace("X",".")

print(f"Base carregada: {len(df)} postos\n")


# ════════════════════════════════════════════════════════════════════════════
# 1.0 METODOLOGIA
# ════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
fig.suptitle("1.0 · Premissas Metodológicas — Normalização de Custos",
             fontsize=13, fontweight="bold", y=1.02)

ax1 = axes[0]; ax1.axis("off")
blocos = [
    ("#02036C","ETAPA 1 — Normalização de Jornada",
     ["Problema: postos com jornadas distintas (4h a 44h/sem)",
      "têm custos mensais incomparáveis entre si.","",
      "Solução: converter tudo para custo por hora trabalhada.","",
      "  Custo/hora  =  Custo mensal  ÷  (Jornada × 4,333)","",
      "  Custo equiv. 40h  =  Custo/hora  ×  40  ×  4,333","",
      "Base: 4,333 semanas/mês (52 semanas ÷ 12 meses)"]),
    ("#FF6200","ETAPA 2 — Equiparação PJ → CLT",
     ["Problema: regime PJ e CLT têm estruturas de custo",
      "distintas — comparação direta é enganosa.","",
      "Solução: aplicar fator de equiparação sobre o custo/hora PJ.","",
      "  Custo/hora norm.  =  Custo/hora PJ  ×  1,40","",
      "Composição do fator 1,40:",
      "  +25–30% → impostos pagos pelo PJ (ISS, IRPJ, CSLL)",
      "  +13–15% → benefícios CLT ausentes no PJ",
      "             (férias, 13º, FGTS)",
      "  Resultado líquido: fator ~1,35–1,45 → adotado 1,40"]),
]
for idx, (color, titulo, linhas) in enumerate(blocos):
    y0 = 0.97 - idx * 0.50
    ax1.add_patch(plt.Rectangle((0,y0-0.44),1,0.06,
                                fc=color,ec="none",transform=ax1.transAxes))
    ax1.text(0.5,y0-0.41,titulo,transform=ax1.transAxes,
             ha="center",va="center",fontsize=9.5,fontweight="bold",color=WH)
    for j,linha in enumerate(linhas):
        ax1.text(0.03,y0-0.50-j*0.038,linha,transform=ax1.transAxes,
                 ha="left",va="top",fontsize=8.5,
                 fontfamily="monospace" if linha.strip().startswith("Custo") else "DejaVu Sans")

ax2 = axes[1]; ax2.axis("off")
ax2.set_title("Exemplo numérico — antes e depois da normalização",
              fontsize=10,fontweight="bold",pad=10)
exemplos = df[df.id.isin([1,5,7,22,49])].copy()
rows_tbl = []
for _,r in exemplos.iterrows():
    rows_tbl.append([r["cargo"],r["uf"],r["forn"],r["reg"],
                     f"{int(r['jh'])}h/sem",brl(r["custo"]),
                     f"R${r['custo_hora']:.0f}/h",f"R${r['rh_norm']:.0f}/h"])
col_labels=["Cargo","UF","Forn.","Reg.","Jornada","Custo\nnominal","Custo/h\nbruto","Custo/h\nnorm."]
tbl=ax2.table(cellText=rows_tbl,colLabels=col_labels,
              loc="center",cellLoc="center",bbox=[0,0.05,1,0.88])
tbl.auto_set_font_size(False); tbl.set_fontsize(8.5); tbl.scale(1,2.2)
for (r,c),cell in tbl.get_celld().items():
    cell.set_edgecolor("#D5D8DC")
    if r==0:
        cell.set_facecolor("#1C2833"); cell.set_text_props(color=WH,fontweight="bold")
    else:
        forn=rows_tbl[r-1][2]
        cell.set_facecolor("#EAF0FB" if forn=="Porto" else "#FFF3EA")
        if c==7: cell.set_text_props(fontweight="bold")
ax2.text(0.5,0.0,"Col. destacada (Custo/h norm.) = valor comparável entre todos os postos",
         transform=ax2.transAxes,ha="center",fontsize=7.5,color="#566573",style="italic")
plt.tight_layout()
plt.savefig("g1_0_metodologia.png",dpi=150,bbox_inches="tight"); plt.close()
print("✅ g1_0_metodologia.png")


# ════════════════════════════════════════════════════════════════════════════
# 1.1 INVENTÁRIO
# ════════════════════════════════════════════════════════════════════════════
inv=(df.groupby(["forn","cargo","reg"])
       .agg(N=("id","count"),jornada_med=("jh","median"))
       .reset_index().sort_values(["forn","N"],ascending=[True,False]))

fig,axes=plt.subplots(1,2,figsize=(12,6))
fig.suptitle("1.1 · Inventário de Postos por Cargo, Regime e Fornecedor",
             fontsize=13,fontweight="bold",y=1.01)
for ax,(forn,color) in zip(axes,[("Porto",C_PORTO),("3778",C_3778)]):
    sub=inv[inv.forn==forn]
    labels=[f"{r.cargo}\n({r.reg} · {int(r.jornada_med)}h)" for _,r in sub.iterrows()]
    ax.barh(range(len(sub)),sub["N"],color=color,height=0.55,edgecolor=WH,zorder=3)
    for i,(_,row) in enumerate(sub.iterrows()):
        ax.text(row["N"]+0.1,i,str(int(row["N"])),va="center",
                fontsize=10,fontweight="bold",color=color)
    ax.set_yticks(range(len(sub))); ax.set_yticklabels(labels,fontsize=9)
    ax.set_xlabel("Quantidade de postos")
    ax.set_title("Porto Seguro" if forn=="Porto" else "3778 Gestiona",
                 fontsize=11,fontweight="bold",color=color,pad=8)
    ax.set_xlim(0,sub["N"].max()+2)
    ax.grid(axis="x",alpha=0.3); ax.grid(axis="y",alpha=0)
plt.tight_layout()
plt.savefig("g1_1_inventario.png",dpi=150,bbox_inches="tight"); plt.close()
print("✅ g1_1_inventario.png")


# ════════════════════════════════════════════════════════════════════════════
# 1.2 CUSTO/HORA POR UF — MÉDICO DO TRABALHO
# ════════════════════════════════════════════════════════════════════════════
med=df[df.cargo=="Médico"].copy()
ufs=sorted(med["uf"].unique())
x,w=np.arange(len(ufs)),0.35

fig,axes=plt.subplots(1,2,figsize=(12,6),sharey=True)
fig.suptitle("1.2 · Médico do Trabalho — Custo/Hora por UF\n"
             "Nominal vs. Normalizado (PJ→CLT · fator 1,40×)",
             fontsize=12,fontweight="bold",y=1.02)
for ax,(col,titulo) in zip(axes,[
    ("custo_hora","Custo/hora nominal (R$/h)\nPJ e CLT como estão"),
    ("rh_norm",   "Custo/hora normalizado (R$/h)\ntudo equiparado a CLT"),
]):
    for i,uf in enumerate(ufs):
        vp=med[(med.uf==uf)&(med.forn=="Porto")][col]
        v3=med[(med.uf==uf)&(med.forn=="3778") ][col]
        if len(vp):
            ax.bar(i-w/2,vp.median(),width=w,color=C_PORTO,edgecolor=WH,zorder=3,
                   label="Porto Seguro" if i==0 else "")
            ax.text(i-w/2,vp.median()+2,f"R${vp.median():.0f}",
                    ha="center",va="bottom",fontsize=7.5,fontweight="bold",color=C_PORTO)
        if len(v3):
            ax.bar(i+w/2,v3.median(),width=w,color=C_3778,edgecolor=WH,zorder=3,
                   label="3778 Gestiona" if i==0 else "")
            ax.text(i+w/2,v3.median()+2,f"R${v3.median():.0f}",
                    ha="center",va="bottom",fontsize=7.5,fontweight="bold",color=C_3778)
    ax.set_xticks(x); ax.set_xticklabels(ufs,fontsize=10)
    ax.set_xlabel("UF"); ax.set_ylabel("R$/hora")
    ax.set_title(titulo,fontsize=10,pad=10)
    ax.legend(fontsize=9,frameon=False)
    ax.grid(axis="y",alpha=0.3); ax.grid(axis="x",alpha=0)
plt.tight_layout()
plt.savefig("g1_2_medico_hora_uf.png",dpi=150,bbox_inches="tight"); plt.close()
print("✅ g1_2_medico_hora_uf.png")


# ════════════════════════════════════════════════════════════════════════════
# 1.3 DISTRIBUIÇÃO GEOGRÁFICA
# ════════════════════════════════════════════════════════════════════════════
resumo=med.groupby(["uf","forn"])["rh_norm"].median().reset_index()
med_geral=resumo["rh_norm"].median()
resumo["idx"]=(resumo["rh_norm"]-med_geral)/med_geral*100

fig,axes=plt.subplots(1,2,figsize=(12,6))
fig.suptitle("1.3 · Médico do Trabalho — Custo/Hora Normalizado por UF\n"
             "Índice relativo à mediana geral  |  verde = abaixo  |  vermelho = acima",
             fontsize=12,fontweight="bold",y=1.02)
for ax,(forn,label,color) in zip(axes,[
    ("Porto","Porto Seguro",C_PORTO),("3778","3778 Gestiona",C_3778),
]):
    sub=resumo[resumo.forn==forn].sort_values("rh_norm")
    bar_colors=["#E74C3C" if v>20 else "#27AE60" if v<-20 else "#F0B27A"
                for v in sub["idx"]]
    ax.barh(range(len(sub)),sub["rh_norm"],color=bar_colors,
            height=0.55,edgecolor=WH,zorder=3)
    ax.axvline(med_geral,color="#1C2833",lw=1.5,ls="--",alpha=0.7,
               label=f"Mediana geral R${med_geral:.0f}/h")
    for i,(_,row) in enumerate(sub.iterrows()):
        sinal="+" if row["idx"]>=0 else ""
        ax.text(row["rh_norm"]+2,i,
                f"R${row['rh_norm']:.0f}/h  ({sinal}{row['idx']:.0f}%)",
                va="center",fontsize=8.5,fontweight="bold")
    ax.set_yticks(range(len(sub))); ax.set_yticklabels(sub["uf"],fontsize=10)
    ax.set_xlabel("R$/hora (normalizado CLT eq.)")
    ax.set_title(label,fontsize=11,fontweight="bold",color=color,pad=8)
    ax.set_xlim(0,sub["rh_norm"].max()*1.35)
    ax.legend(fontsize=8,frameon=False)
    ax.grid(axis="x",alpha=0.3); ax.grid(axis="y",alpha=0)
plt.tight_layout()
plt.savefig("g1_3_barras_uf.png",dpi=150,bbox_inches="tight"); plt.close()
print("✅ g1_3_barras_uf.png")


# ════════════════════════════════════════════════════════════════════════════
# 1.4 VARIAÇÃO INTERNA — BOXPLOT
# ════════════════════════════════════════════════════════════════════════════
fig,ax=plt.subplots(figsize=(12,6))
fig.suptitle("1.4 · Médico do Trabalho — Dispersão Interna por Fornecedor\n"
             "Custo/hora normalizado (equiv. 40h · PJ→CLT 1,40×)",
             fontsize=12,fontweight="bold",y=1.02)
dados=[med[med.forn=="Porto"]["rh_norm"].values,
       med[med.forn=="3778" ]["rh_norm"].values]
labels=["Porto Seguro","3778 Gestiona"]
colors=[C_PORTO,C_3778]
for i,(vals,color) in enumerate(zip(dados,colors)):
    ax.boxplot(vals,positions=[i],widths=0.4,patch_artist=True,
               boxprops=dict(facecolor=color,alpha=0.3,linewidth=1.8),
               medianprops=dict(color=color,linewidth=3),
               whiskerprops=dict(color=color,linewidth=1.8,linestyle="--"),
               capprops=dict(color=color,linewidth=2.5),
               flierprops=dict(marker="o",markerfacecolor=color,
                               markeredgecolor=WH,markersize=7,alpha=0.8))
    s=pd.Series(vals); var=(s.max()-s.min())/s.min()*100
    ax.text(i+0.25,s.max(),   f"  máx  R${s.max():.0f}/h",
            va="center",fontsize=9,color="#E74C3C",fontweight="bold")
    ax.text(i+0.25,s.median(),f"  med  R${s.median():.0f}/h",
            va="center",fontsize=9,color=color,fontweight="bold")
    ax.text(i+0.25,s.min(),   f"  mín  R${s.min():.0f}/h",
            va="center",fontsize=9,color="#27AE60",fontweight="bold")
    ax.text(i,-0.10,f"Variação: {var:.0f}%  |  n = {len(vals)} postos",
            transform=ax.get_xaxis_transform(),
            ha="center",fontsize=9.5,color=color,fontweight="bold")
ax.set_xticks([0,1]); ax.set_xticklabels(labels,fontsize=12,fontweight="bold")
ax.set_ylabel("R$/hora (normalizado)",fontsize=10)
ax.set_xlim(-0.6,1.8)
ax.grid(axis="y",alpha=0.3); ax.grid(axis="x",alpha=0)
plt.tight_layout()
plt.savefig("g1_4_boxplot.png",dpi=150,bbox_inches="tight"); plt.close()
print("✅ g1_4_boxplot.png")


# ════════════════════════════════════════════════════════════════════════════
# 1.7 HEATMAP CARGO × UF
# ════════════════════════════════════════════════════════════════════════════
pivot=(df.groupby(["cargo","uf"])["rh_norm"]
         .median().unstack(fill_value=np.nan))
cargo_ord=df.groupby("cargo")["rh_norm"].median().sort_values(ascending=False).index
uf_ord=df.groupby("uf")["id"].count().sort_values(ascending=False).index
pivot=pivot.reindex(index=cargo_ord,columns=uf_ord)
data_arr=pivot.values.astype(float)
vmin,vmax=np.nanmin(data_arr),np.nanmax(data_arr)

fig,ax=plt.subplots(figsize=(12,6))
fig.suptitle("1.7 · Heatmap — Custo/Hora Normalizado por Cargo × UF\n"
             "Mediana · equiv. 40h · PJ→CLT 1,40×  |  cinza = sem dados",
             fontsize=12,fontweight="bold",y=1.02)
im=ax.imshow(data_arr,aspect="auto",cmap="RdYlGn_r",vmin=vmin,vmax=vmax)
for i in range(data_arr.shape[0]):
    for j in range(data_arr.shape[1]):
        if np.isnan(data_arr[i,j]):
            ax.add_patch(plt.Rectangle((j-0.5,i-0.5),1,1,fc="#D5D8DC",ec=WH,lw=1.5))
        else:
            norm=(data_arr[i,j]-vmin)/(vmax-vmin)
            ax.text(j,i,f"R${data_arr[i,j]:.0f}",
                    ha="center",va="center",fontsize=7.5,fontweight="bold",
                    color=WH if norm>0.6 else "#1C2833")
for i in range(data_arr.shape[0]-1): ax.axhline(i+0.5,color=WH,lw=1.5)
for j in range(data_arr.shape[1]-1): ax.axvline(j+0.5,color=WH,lw=1)
ax.set_xticks(range(len(pivot.columns))); ax.set_xticklabels(pivot.columns,fontsize=9)
ax.set_yticks(range(len(pivot.index)));   ax.set_yticklabels(pivot.index,fontsize=9)
ax.set_xlabel("UF",fontsize=10); ax.set_ylabel("Cargo",fontsize=10)
plt.colorbar(im,ax=ax,fraction=0.03,pad=0.02).set_label("R$/hora normalizado",fontsize=9)
plt.tight_layout()
plt.savefig("g1_7_heatmap.png",dpi=150,bbox_inches="tight"); plt.close()
print("✅ g1_7_heatmap.png")


# ════════════════════════════════════════════════════════════════════════════
# Q2/Q3 BENCHMARK EXTERNO — MÉDICO DO TRABALHO
# ════════════════════════════════════════════════════════════════════════════
# Salário mediana regional (30h/sem) fornecido pelo usuário
# Fonte: pesquisa de mercado regional Médico do Trabalho
bench_regional = {
    "Norte":       17140,
    "Nordeste":    12896,
    "Sul":         15697,
    "Sudeste":     15286,
    "Centro-Oeste":14241,
}
JH_REF = 30

uf_regiao = {
    "SP":"Sudeste","RJ":"Sudeste","MG":"Sudeste","ES":"Sudeste",
    "BA":"Nordeste","PE":"Nordeste","AL":"Nordeste","SE":"Nordeste",
    "PR":"Sul","RS":"Sul","SC":"Sul",
    "GO":"Centro-Oeste","DF":"Centro-Oeste","MT":"Centro-Oeste","MS":"Centro-Oeste",
    "AM":"Norte","PA":"Norte","AC":"Norte","RO":"Norte","RR":"Norte","AP":"Norte","TO":"Norte",
}

bench_rh = {reg: round(sal/(JH_REF*SEM_MES)*FATOR_CUSTO,1)
            for reg,sal in bench_regional.items()}

nosso = med.groupby("uf")["rh_norm"].median().to_dict()

rows_q2 = []
for uf,contrato in nosso.items():
    reg     = uf_regiao.get(uf)
    mercado = bench_rh.get(reg,np.nan) if reg else np.nan
    gap     = (contrato-mercado)/mercado*100 if not np.isnan(mercado) else np.nan
    rows_q2.append({"uf":uf,"regiao":reg,"mercado":mercado,
                    "contrato":contrato,"gap_pct":gap})

comp=(pd.DataFrame(rows_q2).dropna(subset=["gap_pct"])
        .sort_values("gap_pct",ascending=False).reset_index(drop=True))

fig,axes=plt.subplots(1,2,figsize=(12,6))
fig.suptitle(
    "Q2/Q3 · Médico do Trabalho — Custo/Hora Contrato vs. Mercado por UF\n"
    "Mercado = salário mediana regional (30h) × fator custo total CLT 1,83×  |  normalizado para 40h",
    fontsize=11,fontweight="bold",y=1.02)

ax1=axes[0]
x,w=np.arange(len(comp)),0.35
bar_colors=["#E74C3C" if g>20 else "#27AE60" if g<-20 else "#F0B27A"
            for g in comp["gap_pct"]]
b1=ax1.bar(x-w/2,comp["mercado"],width=w,color="#95A5A6",
           label="Referência mercado",edgecolor=WH,zorder=3)
b2=ax1.bar(x+w/2,comp["contrato"],width=w,color=bar_colors,
           label="Nosso contrato",edgecolor=WH,zorder=3)
for bar,val in zip(b1,comp["mercado"]):
    ax1.text(bar.get_x()+bar.get_width()/2,val+2,f"R${val:.0f}",
             ha="center",va="bottom",fontsize=7.5,color="#566573")
for bar,val in zip(b2,comp["contrato"]):
    ax1.text(bar.get_x()+bar.get_width()/2,val+2,f"R${val:.0f}",
             ha="center",va="bottom",fontsize=7.5,fontweight="bold")
ax1.set_xticks(x); ax1.set_xticklabels(comp["uf"],fontsize=10)
ax1.set_ylabel("R$/hora"); ax1.set_xlabel("UF")
ax1.set_title("Contrato vs. Referência de Mercado (R$/hora)",fontsize=10,pad=8)
ax1.legend(fontsize=9,frameon=False)
ax1.grid(axis="y",alpha=0.3); ax1.grid(axis="x",alpha=0)

ax2=axes[1]
comp_s=comp.sort_values("gap_pct")
bar_colors2=["#E74C3C" if g>20 else "#27AE60" if g<-20 else "#F0B27A"
             for g in comp_s["gap_pct"]]
ax2.barh(range(len(comp_s)),comp_s["gap_pct"],
         color=bar_colors2,height=0.55,edgecolor=WH,zorder=3)
ax2.axvline(0,color="#1C2833",lw=1.5,zorder=4)
ax2.axvline(20,color="#E74C3C",lw=1,ls="--",alpha=0.5)
ax2.axvline(-20,color="#27AE60",lw=1,ls="--",alpha=0.5)
for i,(_,row) in enumerate(comp_s.iterrows()):
    sinal="+" if row["gap_pct"]>=0 else ""
    ha="left" if row["gap_pct"]>=0 else "right"
    off=0.8 if row["gap_pct"]>=0 else -0.8
    ax2.text(row["gap_pct"]+off,i,f"{sinal}{row['gap_pct']:.0f}%",
             va="center",ha=ha,fontsize=9,fontweight="bold",
             color="#E74C3C" if row["gap_pct"]>20
             else "#27AE60" if row["gap_pct"]<-20 else "#1C2833")
for i,(_,row) in enumerate(comp_s.iterrows()):
    reg_label=row["regiao"][:8] if row["regiao"] else ""
    ax2.text(-1,i,f"{row['uf']} ({reg_label}...)" if len(str(row["regiao"]))>8
             else f"{row['uf']} ({row['regiao']})",
             va="center",ha="right",fontsize=8,color="#566573")
ax2.set_yticks(range(len(comp_s))); ax2.set_yticklabels([""]*len(comp_s))
ax2.set_xlabel("Gap % (Contrato − Mercado) / Mercado")
ax2.set_title("Gap % por UF\n(+) acima do mercado  |  (−) abaixo",fontsize=10,pad=8)
ax2.grid(axis="x",alpha=0.3); ax2.grid(axis="y",alpha=0)

plt.tight_layout()
plt.savefig("g2_benchmark_regional.png",dpi=150,bbox_inches="tight"); plt.close()
print("✅ g2_benchmark_regional.png")

print("\nQ1 + Q2 concluídas — 7 gráficos gerados.")

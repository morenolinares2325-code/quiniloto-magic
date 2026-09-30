4. Reinicia la app
""")
else:
st.warning("No hay datos disponibles.")


# ═══════════════════════════════════════════════
# ⚽ QUINIELA
# ═══════════════════════════════════════════════
elif seccion == "⚽ Quiniela":
st.title("⚽ Quiniela + Pleno al 15")
st.caption(f"Precio: {PRECIO_QUINIELA} €/apuesta · Mínimo {MIN_QUINIELA} apuestas")

st.subheader("1️⃣ Configura los 14 partidos")
opciones = ["1", "X", "2", "1X", "X2", "12", "1X2"]
cols = st.columns(2)
for i in range(14):
with cols[i % 2]:
    st.session_state.signos[i] = st.selectbox(
        f"Partido {i+1}", opciones,
        index=opciones.index(st.session_state.signos[i]),
        key=f"p{i}",
    )

dobles, triples = contar_dobles_triples(st.session_state.signos)
st.info(f"📊 Dobles: {dobles} · Triples: {triples} · Directas: {3**triples * 2**dobles:,}")

st.divider()
st.subheader("2️⃣ Reducción oficial")
tipo_red = st.selectbox(
"Sistema",
list(REDUCCIONES_QUINIELA.keys()),
format_func=lambda x: REDUCCIONES_QUINIELA[x]["nombre"],
)

st.divider()
st.subheader("1️⃣5️⃣ Pleno al 15")
col_pl1, col_pl2 = st.columns(2)
with col_pl1:
pleno_loc = st.multiselect("Goles local", PLENO_OPCIONES, default=[st.session_state.pleno_local], key="pleno_loc_ms")
with col_pl2:
pleno_vis = st.multiselect("Goles visitante", PLENO_OPCIONES, default=[st.session_state.pleno_visit], key="pleno_vis_ms")

st.session_state.pleno_local = pleno_loc[0] if pleno_loc else "1"
st.session_state.pleno_visit = pleno_vis[0] if pleno_vis else "0"
pleno_mult = max(1, len(pleno_loc)) * max(1, len(pleno_vis))
st.info(f"Multiplicador del Pleno: ×{pleno_mult}")

st.divider()
st.subheader("3️⃣ Coste")
directas = generar_combinaciones(st.session_state.signos)
total_directas = len(directas) * pleno_mult

c1, c2 = st.columns(2)
c1.metric("Apuestas directas", f"{total_directas:,}")
c2.metric("Coste directo", f"{total_directas * PRECIO_QUINIELA:,.2f} €")

if st.button("🎯 Generar combinaciones", type="primary", use_container_width=True):
st.session_state.combinaciones = directas
st.session_state.baritas = []
st.rerun()

st.divider()

if st.session_state.combinaciones:
st.subheader("4️⃣ Barita Mágica 🪄")
reducidas = aplicar_reduccion_oficial(st.session_state.combinaciones, tipo_red, st.session_state.signos)
factores = st.session_state.barita_factores["quiniela"]
actuales = aplicar_baritas(reducidas, st.session_state.baritas, factores, min_ap=MIN_QUINIELA)

n_sin_pleno = len(actuales)
n_total = n_sin_pleno * pleno_mult
coste_act, aviso = coste_real(n_total, PRECIO_QUINIELA, MIN_QUINIELA)

st.markdown(
    f'<div class="card" style="text-align:center;">'
    f'<div style="color:#a0a0b8;font-size:14px;">APUESTAS TOTALES</div>'
    f'<div class="precio-grande">{n_total:,}</div>'
    f'<div style="color:#a0a0b8;font-size:14px;margin-top:8px;">COSTE FINAL</div>'
    f'<div style="color:#FFD700;font-size:32px;font-weight:800;">{coste_act:,.2f} €</div>'
    f'</div>',
    unsafe_allow_html=True,
)

if aviso:
    st.warning(f"⚠️ Mínimo oficial: {MIN_QUINIELA} apuestas ({MIN_QUINIELA*PRECIO_QUINIELA:.2f} €).")

cols_b = st.columns(4)
for idx, capa in enumerate(BARITA_DEFAULT):
    with cols_b[idx]:
        usada = capa["id"] in st.session_state.baritas
        pct = int(factores[idx] * 100)
        label = f"{'✅ ' if usada else ''}{capa['nombre']} ({pct}%)"
        if st.button(label, key=f"b{capa['id']}", use_container_width=True, disabled=usada):
            st.session_state.baritas.append(capa["id"])
            st.rerun()

if st.session_state.baritas:
    if st.button("↩️ Deshacer última barita", use_container_width=True):
        st.session_state.baritas.pop()
        st.rerun()

st.divider()
st.subheader("5️⃣ Descargar .txt")
contenido = a_txt_quiniela(actuales, st.session_state.pleno_local, st.session_state.pleno_visit)
st.download_button(
    "📥 Descargar .txt",
    data=contenido.encode("utf-8"),
    file_name="quiniela_reducida.txt",
    mime="text/plain",
    use_container_width=True,
    type="primary",
)


# ═══════════════════════════════════════════════
# 🧠 PROBABILIDADES
# ═══════════════════════════════════════════════
elif seccion == "🧠 Probabilidades 1X2 + Pleno":
st.title("🧠 Probabilidades 1X2 + Pleno al 15")

equipos_disponibles = sorted(st.session_state.equipos.keys())

st.markdown("### 1️⃣ Emparejamientos (14 partidos)")
for i in range(14):
local_actual, visit_actual = st.session_state.partidos_equipos[i]
cols = st.columns([1, 3, 3])
cols[0].markdown(f"**#{i+1}**")
local = cols[1].selectbox("Local", equipos_disponibles,
    index=equipos_disponibles.index(local_actual) if local_actual in equipos_disponibles else 0,
    key=f"loc{i}")
visit = cols[2].selectbox("Visitante", equipos_disponibles,
    index=equipos_disponibles.index(visit_actual) if visit_actual in equipos_disponibles else 1,
    key=f"vis{i}")
st.session_state.partidos_equipos[i] = (local, visit)

st.divider()
st.markdown("### 1️⃣5️⃣ Pleno al 15")
p_loc, p_vis = st.columns(2)
pl_local = p_loc.selectbox("Local", equipos_disponibles,
index=equipos_disponibles.index(st.session_state.pleno_equipos[0]) if st.session_state.pleno_equipos[0] in equipos_disponibles else 0,
key="pleno_loc_eq")
pl_visit = p_vis.selectbox("Visitante", equipos_disponibles,
index=equipos_disponibles.index(st.session_state.pleno_equipos[1]) if st.session_state.pleno_equipos[1] in equipos_disponibles else 1,
key="pleno_vis_eq")
st.session_state.pleno_equipos = (pl_local, pl_visit)

st.divider()

if st.button("📊 Calcular", type="primary", use_container_width=True):
st.subheader("📈 14 partidos")
for i, (local, visit) in enumerate(st.session_state.partidos_equipos):
    lam_l, lam_v = estimar_lambdas(local, visit, st.session_state.equipos)
    probs = predecir_1x2(lam_l, lam_v)
    favorito = max(probs, key=probs.get)
    st.markdown(f"**P{i+1}: {local} vs {visit}**")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("1", f"{probs['1']}%")
    c2.metric("X", f"{probs['X']}%")
    c3.metric("2", f"{probs['2']}%")
    c4.metric("Fav.", favorito)
    st.divider()

st.subheader("1️⃣5️⃣ Pleno al 15")
lam_l, lam_v = estimar_lambdas(pl_local, pl_visit, st.session_state.equipos)
pl = predecir_pleno(lam_l, lam_v)
c1, c2 = st.columns(2)
with c1:
    st.markdown(f"**{pl_local}**")
    for k in ["0", "1", "2", "M"]:
        st.metric(f"{k} goles", f"{pl['local'][k]}%")
with c2:
    st.markdown(f"**{pl_visit}**")
    for k in ["0", "1", "2", "M"]:
        st.metric(f"{k} goles", f"{pl['visitante'][k]}%")

st.divider()
st.subheader("🔧 Editar fuerzas")
with st.expander("Editar equipos"):
for nombre in sorted(st.session_state.equipos.keys()):
    eq = st.session_state.equipos[nombre]
    cols = st.columns([3, 2, 2])
    cols[0].markdown(f"**{nombre}**")
    eq["ataque"] = cols[1].number_input("Ataque", 0.0, 5.0, eq["ataque"], 0.05, key=f"at_{nombre}", label_visibility="collapsed")
    eq["defensa"] = cols[2].number_input("Defensa", 0.0, 5.0, eq["defensa"], 0.05, key=f"df_{nombre}", label_visibility="collapsed")


# ═══════════════════════════════════════════════
# 🎲 BONOLOTO
# ═══════════════════════════════════════════════
elif seccion == "🎲 Bonoloto":
st.title("🎲 Bonoloto")
st.caption(f"Precio: {PRECIO_BONOLOTO} €/apuesta · Mínimo {MIN_BONOLOTO} apuestas ({MIN_BONOLOTO*PRECIO_BONOLOTO:.2f} €)")

if "bono_nums" not in st.session_state: st.session_state.bono_nums = []
if "bono_combs" not in st.session_state: st.session_state.bono_combs = None
if "bono_baritas" not in st.session_state: st.session_state.bono_baritas = []

st.subheader("1️⃣ Selecciona números (1-49)")
cols = st.columns(10)
for n in range(1, 50):
with cols[(n-1) % 10]:
    activo = n in st.session_state.bono_nums
    label = f"**{n}**" if activo else str(n)
    if st.button(label, key=f"bn{n}", use_container_width=True):
        if activo: st.session_state.bono_nums.remove(n)
        else: st.session_state.bono_nums.append(n)
        st.rerun()

st.info(f"Seleccionados: {len(st.session_state.bono_nums)} → {sorted(st.session_state.bono_nums)}")

c1, c2 = st.columns(2)
if c1.button("🎲 Aleatorio", use_container_width=True):
st.session_state.bono_nums = random.sample(range(1, 50), 6)
st.rerun()
if c2.button("🗑️ Limpiar", use_container_width=True):
st.session_state.bono_nums = []
st.session_state.bono_combs = None
st.session_state.bono_baritas = []
st.rerun()

st.divider()

if len(st.session_state.bono_nums) >= 6:
combs = generar_bonoloto(st.session_state.bono_nums)
n_ap = len(combs)
coste_dir, aviso_dir = coste_real(n_ap, PRECIO_BONOLOTO, MIN_BONOLOTO)

st.subheader("2️⃣ Coste directo")
c1, c2 = st.columns(2)
c1.metric("Apuestas", f"{n_ap:,}")
c2.metric("Coste", f"{coste_dir:,.2f} €")
if aviso_dir:
    st.warning(f"⚠️ Mínimo: {MIN_BONOLOTO} apuestas ({MIN_BONOLOTO*PRECIO_BONOLOTO:.2f} €).")

if st.button("✅ Generar", type="primary", use_container_width=True):
    st.session_state.bono_combs = combs
    st.session_state.bono_baritas = []
    st.rerun()

if st.session_state.bono_combs:
    st.divider()
    st.subheader("3️⃣ Barita Mágica 🪄")
    factores = st.session_state.barita_factores["bonoloto"]
    actuales = baritas_loteria(st.session_state.bono_combs, st.session_state.bono_baritas, factores, MIN_BONOLOTO)
    n_act = len(actuales)
    coste_act, aviso = coste_real(n_act, PRECIO_BONOLOTO, MIN_BONOLOTO)

    st.markdown(
        f'<div class="card" style="text-align:center;">'
        f'<div style="color:#a0a0b8;font-size:14px;">APUESTAS</div>'
        f'<div class="precio-grande">{n_act:,}</div>'
        f'<div style="color:#FFD700;font-size:32px;font-weight:800;">{coste_act:,.2f} €</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if aviso:
        st.warning(f"⚠️ Mínimo: {MIN_BONOLOTO} apuestas ({MIN_BONOLOTO*PRECIO_BONOLOTO:.2f} €).")

    cols_b = st.columns(4)
    for idx, capa in enumerate(BARITA_DEFAULT):
        with cols_b[idx]:
            usada = capa["id"] in st.session_state.bono_baritas
            pct = int(factores[idx] * 100)
            label = f"{'✅ ' if usada else ''}{capa['nombre']} ({pct}%)"
            if st.button(label, key=f"bb{capa['id']}", use_container_width=True, disabled=usada):
                st.session_state.bono_baritas.append(capa["id"])
                st.rerun()

    if st.session_state.bono_baritas:
        if st.button("↩️ Deshacer", use_container_width=True, key="undo_bono"):
            st.session_state.bono_baritas.pop()
            st.rerun()

    st.download_button(
        "📥 Descargar .txt",
        data=txt_loteria(actuales).encode("utf-8"),
        file_name="bonoloto_reducida.txt",
        mime="text/plain",
        use_container_width=True,
        type="primary",
    )


# ═══════════════════════════════════════════════
# 🍀 PRIMITIVA
# ═══════════════════════════════════════════════
elif seccion == "🍀 Primitiva":
st.title("🍀 Primitiva")
st.caption(f"Precio: {PRECIO_PRIMITIVA} €/apuesta · Mínimo {MIN_PRIMITIVA} apuesta")

if "pri_nums" not in st.session_state: st.session_state.pri_nums = []
if "pri_combs" not in st.session_state: st.session_state.pri_combs = None
if "pri_baritas" not in st.session_state: st.session_state.pri_baritas = []

st.subheader("1️⃣ Selecciona números (1-49)")
cols = st.columns(10)
for n in range(1, 50):
with cols[(n-1) % 10]:
    activo = n in st.session_state.pri_nums
    label = f"**{n}**" if activo else str(n)
    if st.button(label, key=f"pn{n}", use_container_width=True):
        if activo: st.session_state.pri_nums.remove(n)
        else: st.session_state.pri_nums.append(n)
        st.rerun()

st.info(f"Seleccionados: {len(st.session_state.pri_nums)} → {sorted(st.session_state.pri_nums)}")

c1, c2 = st.columns(2)
if c1.button("🎲 Aleatorio", use_container_width=True):
st.session_state.pri_nums = random.sample(range(1, 50), 6)
st.rerun()
if c2.button("🗑️ Limpiar", use_container_width=True):
st.session_state.pri_nums = []
st.session_state.pri_combs = None
st.session_state.pri_baritas = []
st.rerun()

st.divider()

if len(st.session_state.pri_nums) >= 6:
combs = generar_primitiva(st.session_state.pri_nums)
n_ap = len(combs)
coste_dir = round(n_ap * PRECIO_PRIMITIVA, 2)

st.subheader("2️⃣ Coste directo")
c1, c2 = st.columns(2)
c1.metric("Apuestas", f"{n_ap:,}")
c2.metric("Coste", f"{coste_dir:,.2f} €")

if st.button("✅ Generar", type="primary", use_container_width=True, key="gen_pri"):
    st.session_state.pri_combs = combs
    st.session_state.pri_baritas = []
    st.rerun()

if st.session_state.pri_combs:
    st.divider()
    st.subheader("3️⃣ Barita Mágica 🪄")
    factores = st.session_state.barita_factores["primitiva"]
    actuales = baritas_loteria(st.session_state.pri_combs, st.session_state.pri_baritas, factores, MIN_PRIMITIVA)
    n_act = len(actuales)
    coste_act = round(n_act * PRECIO_PRIMITIVA, 2)

    st.markdown(
        f'<div class="card" style="text-align:center;">'
        f'<div style="color:#a0a0b8;font-size:14px;">APUESTAS</div>'
        f'<div class="precio-grande">{n_act:,}</div>'
        f'<div style="color:#FFD700;font-size:32px;font-weight:800;">{coste_act:,.2f} €</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    cols_b = st.columns(4)
    for idx, capa in enumerate(BARITA_DEFAULT):
        with cols_b[idx]:
            usada = capa["id"] in st.session_state.pri_baritas
            pct = int(factores[idx] * 100)
            label = f"{'✅ ' if usada else ''}{capa['nombre']} ({pct}%)"
            if st.button(label, key=f"pb{capa['id']}", use_container_width=True, disabled=usada):
                st.session_state.pri_baritas.append(capa["id"])
                st.rerun()

    if st.session_state.pri_baritas:
        if st.button("↩️ Deshacer", use_container_width=True, key="undo_pri"):
            st.session_state.pri_baritas.pop()
            st.rerun()

    st.download_button(
        "📥 Descargar .txt",
        data=txt_loteria(actuales).encode("utf-8"),
        file_name="primitiva_reducida.txt",
        mime="text/plain",
        use_container_width=True,
        type="primary",
    )


# ═══════════════════════════════════════════════
# 🌍 EUROMILLONES
# ═══════════════════════════════════════════════
elif seccion == "🌍 Euromillones":
st.title("🌍 Euromillones")
st.caption(f"5 números (1-50) + 2 estrellas (1-12) · {PRECIO_EUROMILLONES} €/apuesta")

if "eu_nums" not in st.session_state: st.session_state.eu_nums = []
if "eu_est" not in st.session_state: st.session_state.eu_est = []
if "eu_combs" not in st.session_state: st.session_state.eu_combs = None
if "eu_baritas" not in st.session_state: st.session_state.eu_baritas = []

st.subheader("1️⃣ Números (1-50)")
cols = st.columns(10)
for n in range(1, 51):
with cols[(n-1) % 10]:
    activo = n in st.session_state.eu_nums
    label = f"**{n}**" if activo else str(n)
    if st.button(label, key=f"en{n}", use_container_width=True):
        if activo: st.session_state.eu_nums.remove(n)
        else: st.session_state.eu_nums.append(n)
        st.rerun()

st.subheader("2️⃣ Estrellas (1-12)")
cols_e = st.columns(12)
for n in range(1, 13):
with cols_e[n-1]:
    activo = n in st.session_state.eu_est
    label = f"**⭐{n}**" if activo else f"⭐{n}"
    if st.button(label, key=f"ee{n}", use_container_width=True):
        if activo: st.session_state.eu_est.remove(n)
        else: st.session_state.eu_est.append(n)
        st.rerun()

st.info(f"Números: {len(st.session_state.eu_nums)} → {sorted(st.session_state.eu_nums)}")
st.info(f"Estrellas: {len(st.session_state.eu_est)} → {sorted(st.session_state.eu_est)}")

c1, c2 = st.columns(2)
if c1.button("🎲 Aleatorio", use_container_width=True, key="rand_eu"):
st.session_state.eu_nums = random.sample(range(1, 51), 5)
st.session_state.eu_est = random.sample(range(1, 13), 2)
st.rerun()
if c2.button("🗑️ Limpiar", use_container_width=True, key="clear_eu"):
st.session_state.eu_nums = []
st.session_state.eu_est = []
st.session_state.eu_combs = None
st.session_state.eu_baritas = []
st.rerun()

st.divider()

if len(st.session_state.eu_nums) >= 5 and len(st.session_state.eu_est) >= 2:
combs = generar_euromillones(st.session_state.eu_nums, st.session_state.eu_est)
n_ap = len(combs)
coste_dir = round(n_ap * PRECIO_EUROMILLONES, 2)

st.subheader("3️⃣ Coste directo")
c1, c2 = st.columns(2)
c1.metric("Apuestas", f"{n_ap:,}")
c2.metric("Coste", f"{coste_dir:,.2f} €")

if st.button("✅ Generar", type="primary", use_container_width=True, key="gen_eu"):
    st.session_state.eu_combs = combs
    st.session_state.eu_baritas = []
    st.rerun()

if st.session_state.eu_combs:
    st.divider()
    st.subheader("4️⃣ Barita Mágica 🪄")
    factores = st.session_state.barita_factores["euromillones"]
    actuales = baritas_loteria(st.session_state.eu_combs, st.session_state.eu_baritas, factores, MIN_EUROMILLONES)
    n_act = len(actuales)
    coste_act = round(n_act * PRECIO_EUROMILLONES, 2)

    st.markdown(
        f'<div class="card" style="text-align:center;">'
        f'<div style="color:#a0a0b8;font-size:14px;">APUESTAS</div>'
        f'<div class="precio-grande">{n_act:,}</div>'
        f'<div style="color:#FFD700;font-size:32px;font-weight:800;">{coste_act:,.2f} €</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    cols_b = st.columns(4)
    for idx, capa in enumerate(BARITA_DEFAULT):
        with cols_b[idx]:
            usada = capa["id"] in st.session_state.eu_baritas
            pct = int(factores[idx] * 100)
            label = f"{'✅ ' if usada else ''}{capa['nombre']} ({pct}%)"
            if st.button(label, key=f"eb{capa['id']}", use_container_width=True, disabled=usada):
                st.session_state.eu_baritas.append(capa["id"])
                st.rerun()

    if st.session_state.eu_baritas:
        if st.button("↩️ Deshacer", use_container_width=True, key="undo_eu"):
            st.session_state.eu_baritas.pop()
            st.rerun()

    st.download_button(
        "📥 Descargar .txt",
        data=txt_loteria(actuales).encode("utf-8"),
        file_name="euromillones_reducida.txt",
        mime="text/plain",
        use_container_width=True,
        type="primary",
    )


# ═══════════════════════════════════════════════
# 🪄 CONFIGURAR BARITA
# ═══════════════════════════════════════════════
elif seccion == "🪄 Configurar Barita":
st.title("🪄 Configurar Barita Mágica")
st.caption("Ajusta el porcentaje de combinaciones que se mantienen al pulsar cada barita.")

juegos = ["quiniela", "bonoloto", "primitiva", "euromillones"]
nombres_bonitos = {
"quiniela": "⚽ Quiniela",
"bonoloto": "🎲 Bonoloto",
"primitiva": "🍀 Primitiva",
"euromillones": "🌍 Euromillones",
}
nombres_capas = ["🪄 Poda básica", "🪄 Filtro histórico", "🪄 Equilibrio", "🪄 Selección élite"]

for juego in juegos:
st.subheader(nombres_bonitos[juego])
cols = st.columns(4)
for i, capa_nombre in enumerate(nombres_capas):
    with cols[i]:
        pct = st.slider(
            capa_nombre,
            min_value=5, max_value=100,
            value=int(st.session_state.barita_factores[juego][i] * 100),
            step=5, key=f"barita_{juego}_{i}",
            format="%d%%",
        )
        st.session_state.barita_factores[juego][i] = pct / 100.0
st.divider()

if st.button("🔄 Restaurar valores por defecto", use_container_width=True):
st.session_state.barita_factores = {
    "quiniela":    [0.75, 0.70, 0.60, 0.55],
    "bonoloto":    [0.75, 0.70, 0.60, 0.55],
    "primitiva":   [0.75, 0.70, 0.60, 0.55],
    "euromillones":[0.75, 0.70, 0.60, 0.55],
}
st.rerun()

st.info("Los cambios se aplican al instante en todas las secciones.")


# ═══════════════════════════════════════════════
# 🤖 IA MAGIC
# ═══════════════════════════════════════════════
elif seccion == "🤖 IA Magic":
st.title("🤖 IA Magic")
st.caption("Cómo funciona todo.")

st.markdown("### 🧠 Poisson")
st.write("""
1. Cada equipo tiene **ataque** y **defensa**.
2. Se calculan **λ (goles esperados)** con factor campo 1.15 local / 0.85 visitante.
3. Con Poisson se obtiene la probabilidad de cada marcador.
4. Se agrupan en **1, X, 2** y en el **Pleno** en 0, 1, 2, **M**.
""")

st.markdown("### 🪄 Barita Mágica")
st.write("Cada pulsación mantiene un % de combinaciones. Puedes ajustar esos % en **🪄 Configurar Barita**.")

st.markdown("### 💶 Precios oficiales")
st.table({
"Juego": ["Quiniela", "Bonoloto", "Primitiva", "Euromillones"],
"€/apuesta": [PRECIO_QUINIELA, PRECIO_BONOLOTO, PRECIO_PRIMITIVA, PRECIO_EUROMILLONES],
"Mín. apuestas": [MIN_QUINIELA, MIN_BONOLOTO, MIN_PRIMITIVA, MIN_EUROMILLONES],
})

# ═══════════════════════════════════════════════
# ⚙️ CUENTA
# ═══════════════════════════════════════════════
elif seccion == "⚙️ Cuenta":
    st.title("Cuenta")
    st.write("**Plan:** Free (demo)")
    st.write("Precios oficiales:")
    st.write(f"Quiniela: {PRECIO_QUINIELA} EUR")
    st.write(f"Bonoloto: {PRECIO_BONOLOTO} EUR")
    st.write(f"Primitiva: {PRECIO_PRIMITIVA} EUR")
    st.write(f"Euromillones: {PRECIO_EUROMILLONES} EUR")
    st.write("Minimos (apuestas):")
    st.write(f"Quiniela: {MIN_QUINIELA}")
    st.write(f"Bonoloto: {MIN_BONOLOTO}")
    st.write(f"Primitiva: {MIN_PRIMITIVA}")
    st.write(f"Euromillones: {MIN_EUROMILLONES}")
    if st.button("Cerrar sesion", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()

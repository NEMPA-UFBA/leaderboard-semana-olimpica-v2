import streamlit as st
from database import get_db
from models import User, Equipe, Regata, Questao, Tentativa
from auth import login_form, require_auth
from scoring import registrar_tentativa, excluir_tentativa, PONTOS_POR_TENTATIVA

db = get_db()

if not login_form(db, User):
    st.stop()

user = require_auth(["juiz", "admin"])
if not user:
    st.error("Acesso restrito a juizes.")
    st.stop()

st.markdown(f"Logado como: **{user['username']}**")

if st.sidebar.button("Sair", use_container_width=True):
    del st.session_state["user"]
    st.rerun()

# Find active regata
regata = db.query(Regata).filter_by(ativa=True).first()

if not regata:
    st.warning("Nenhuma regata ativa no momento. Aguarde o admin ativar uma regata.")
    db.close()
    st.stop()

st.markdown(f"**Regata:** {regata.nome}")
st.divider()

equipes = db.query(Equipe).order_by(Equipe.nome).all()
questoes = db.query(Questao).filter_by(regata_id=regata.id).all()

if not equipes:
    st.warning("Nenhuma equipe cadastrada.")
    db.close()
    st.stop()

if not questoes:
    st.warning("Nenhuma questao nesta regata.")
    db.close()
    st.stop()

# --- Selection ---
col_eq, col_qt = st.columns(2, gap="large")

with col_eq:
    equipe_selecionada = st.selectbox(
        "Equipe", equipes, format_func=lambda e: e.nome
    )

niveis_display = {"facil": "🟢 Facil", "medio": "🟡 Medio", "dificil": "🔴 Dificil"}
with col_qt:
    questao_selecionada = st.selectbox(
        "Questao",
        questoes,
        format_func=lambda q: f"{niveis_display.get(q.nivel, q.nivel)} — {q.imagem_filename or q.enunciado[:30] if q.enunciado else 'Sem titulo'}",
    )

st.divider()

# --- Attempt status ---
tentativas_anteriores = (
    db.query(Tentativa)
    .filter_by(equipe_id=equipe_selecionada.id, questao_id=questao_selecionada.id)
    .order_by(Tentativa.numero)
    .all()
)

ja_acertou = any(t.acertou for t in tentativas_anteriores)
num_tentativas = len(tentativas_anteriores)

# Status indicator
if ja_acertou:
    t_acerto = next(t for t in tentativas_anteriores if t.acertou)
    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg,#1b5e20,#2e7d32); border-radius:12px; padding:1.5rem;
                    text-align:center; margin-bottom:1rem;">
            <div style="font-family:'Bebas Neue',sans-serif; font-size:1.8rem; color:#a5d6a7;
                        letter-spacing:2px;">JA ACERTOU!</div>
            <div style="font-family:'Outfit',sans-serif; color:#e8f5e9; font-size:1rem; margin-top:4px;">
                Tentativa {t_acerto.numero} — +{t_acerto.pontos} pontos</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
elif num_tentativas >= 3:
    st.markdown(
        """
        <div style="background:linear-gradient(135deg,#b71c1c,#c62828); border-radius:12px; padding:1.5rem;
                    text-align:center; margin-bottom:1rem;">
            <div style="font-family:'Bebas Neue',sans-serif; font-size:1.8rem; color:#ef9a9a;
                        letter-spacing:2px;">TENTATIVAS ESGOTADAS</div>
            <div style="font-family:'Outfit',sans-serif; color:#ffcdd2; font-size:1rem; margin-top:4px;">
                3/3 tentativas usadas — 0 pontos</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    proxima = num_tentativas + 1
    pontos_possiveis = {1: 100, 2: 80, 3: 50}

    # Attempt dots
    dots = ""
    for i in range(1, 4):
        if i <= num_tentativas:
            dots += '<span style="color:#ef5350; font-size:1.5rem; margin:0 4px;">●</span>'
        elif i == proxima:
            dots += '<span style="color:#ffd200; font-size:1.5rem; margin:0 4px;">●</span>'
        else:
            dots += '<span style="color:#555; font-size:1.5rem; margin:0 4px;">○</span>'

    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg,#1a1a2e,#16213e); border:1px solid #333;
                    border-radius:12px; padding:1.5rem; text-align:center; margin-bottom:1rem;">
            <div style="margin-bottom:8px;">{dots}</div>
            <div style="font-family:'Outfit',sans-serif; color:#ccc; font-size:1rem;">
                {proxima}a tentativa — vale <strong style="color:#ffd200;">{pontos_possiveis[proxima]} pontos</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Hidden Streamlit buttons (triggered by long-press JS below)
    col1, col2 = st.columns(2, gap="large")
    acertou_clicked = False
    errou_clicked = False

    with col1:
        acertou_clicked = st.button("ACERTOU_HIDDEN", use_container_width=True, key="hidden_acertou")

    with col2:
        errou_clicked = st.button("ERROU_HIDDEN", use_container_width=True, key="hidden_errou")

    # Long-press buttons with animation (rendered via components.html for JS support)
    import streamlit.components.v1 as components
    components.html(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap');
        * { box-sizing:border-box; margin:0; padding:0; }
        body { background:transparent; overflow:hidden; }
        .hold-btn-container { display:flex; gap:1rem; padding:4px; }
        .hold-btn {
            flex:1; position:relative; overflow:hidden; border:none; border-radius:10px;
            font-family:'Outfit',sans-serif; font-size:1.05rem; font-weight:700;
            padding:1.1rem 0.8rem; cursor:pointer; user-select:none;
            -webkit-user-select:none; -webkit-touch-callout:none;
            transition: transform 0.1s;
        }
        .hold-btn:active { transform:scale(0.97); }
        .hold-btn-acertou {
            background:linear-gradient(135deg,#2e7d32,#43a047); color:#fff;
            box-shadow:0 4px 15px rgba(46,125,50,0.4);
        }
        .hold-btn-errou {
            background:linear-gradient(135deg,#c62828,#e53935); color:#fff;
            box-shadow:0 4px 15px rgba(198,40,40,0.4);
        }
        .progress-overlay {
            position:absolute; top:0; left:0; width:0; height:100%;
            background:rgba(255,255,255,0.25); pointer-events:none;
        }
        .hold-btn.holding .progress-overlay {
            width:100%; transition:width 1s linear;
        }
        .btn-label { position:relative; z-index:1; display:flex; align-items:center;
                     justify-content:center; gap:8px; }
        .spinner { display:none; width:18px; height:18px; border:3px solid rgba(255,255,255,0.3);
                   border-top-color:#fff; border-radius:50%; animation:spin 0.6s linear infinite; }
        .hold-btn.holding .spinner { display:inline-block; }
        .hold-btn.done { opacity:0.6; pointer-events:none; }
        .hold-hint { text-align:center; font-family:'Outfit',sans-serif; color:#888;
                     font-size:0.78rem; margin-top:6px; letter-spacing:0.3px; }
        @keyframes spin { to { transform:rotate(360deg); } }
        </style>

        <div class="hold-btn-container">
            <button class="hold-btn hold-btn-acertou" id="btn-acertou">
                <div class="progress-overlay" id="progress-acertou"></div>
                <div class="btn-label"><span class="spinner"></span> ✅ ACERTOU</div>
            </button>
            <button class="hold-btn hold-btn-errou" id="btn-errou">
                <div class="progress-overlay" id="progress-errou"></div>
                <div class="btn-label"><span class="spinner"></span> ❌ ERROU</div>
            </button>
        </div>
        <div class="hold-hint">Segure o botao por 1 segundo para confirmar</div>

        <script>
        const timers = {};

        function findAndClickHidden(keyword) {
            const btns = window.parent.document.querySelectorAll('button');
            for (const b of btns) {
                if (b.textContent.includes(keyword)) {
                    b.click();
                    return;
                }
            }
        }

        function setup(action, keyword) {
            const btn = document.getElementById('btn-' + action);
            let timer = null;

            function start(e) {
                e.preventDefault();
                if (timer) return;
                btn.classList.add('holding');
                timer = setTimeout(() => {
                    btn.classList.remove('holding');
                    btn.classList.add('done');
                    findAndClickHidden(keyword);
                    timer = null;
                }, 1000);
            }

            function end(e) {
                e.preventDefault();
                if (!timer) return;
                clearTimeout(timer);
                timer = null;
                btn.classList.remove('holding');
            }

            btn.addEventListener('mousedown', start);
            btn.addEventListener('mouseup', end);
            btn.addEventListener('mouseleave', end);
            btn.addEventListener('touchstart', start, {passive:false});
            btn.addEventListener('touchend', end, {passive:false});
            btn.addEventListener('touchcancel', end, {passive:false});
        }

        // Hide the real Streamlit trigger buttons on load
        function hideHiddenBtns() {
            const btns = window.parent.document.querySelectorAll('button');
            for (const b of btns) {
                const txt = b.textContent.trim();
                if (txt === 'ACERTOU_HIDDEN' || txt === 'ERROU_HIDDEN') {
                    // Hide the nearest stVerticalBlock parent or the button's column container
                    let container = b.closest('[data-testid="column"]') || b.parentElement;
                    if (container) {
                        container.style.height = '0';
                        container.style.overflow = 'hidden';
                        container.style.margin = '0';
                        container.style.padding = '0';
                    }
                }
            }
        }
        // Run after a small delay to ensure Streamlit has rendered
        setTimeout(hideHiddenBtns, 100);
        setTimeout(hideHiddenBtns, 500);

        setup('acertou', 'ACERTOU_HIDDEN');
        setup('errou', 'ERROU_HIDDEN');
        </script>
        """,
        height=110,
    )

    # Process the results
    if acertou_clicked:
        result = registrar_tentativa(
            db, equipe_selecionada.id, questao_selecionada.id, True, user["id"]
        )
        if "erro" in result:
            st.error(result["erro"])
        else:
            st.success(
                f"**{equipe_selecionada.nome}** — {niveis_display.get(questao_selecionada.nivel, '')} — "
                f"{result['numero']}a tentativa — **+{result['pontos']} pontos!**"
            )
            st.balloons()

    if errou_clicked:
        result = registrar_tentativa(
            db, equipe_selecionada.id, questao_selecionada.id, False, user["id"]
        )
        if "erro" in result:
            st.error(result["erro"])
        else:
            restantes = 3 - result["numero"]
            st.warning(
                f"**{equipe_selecionada.nome}** — {niveis_display.get(questao_selecionada.nivel, '')} — "
                f"Errou tentativa {result['numero']}. Restam {restantes} tentativa(s)."
            )

# --- Attempt history & correction ---
if tentativas_anteriores:
    st.divider()
    st.markdown("#### Historico de tentativas")
    for t in tentativas_anteriores:
        with st.container(border=True):
            status_icon = "✅" if t.acertou else "❌"
            c1, c2, c3 = st.columns([5, 1, 1])
            c1.markdown(
                f"**Tentativa {t.numero}** — {status_icon} {'Acertou' if t.acertou else 'Errou'} — **{t.pontos} pts**"
            )
            can_modify = (t.juiz_id == user["id"]) or (user["role"] == "admin")
            if can_modify:
                if c2.button("Corrigir", key=f"corrigir_{t.id}"):
                    t.acertou = not t.acertou
                    if t.acertou:
                        t.pontos = PONTOS_POR_TENTATIVA.get(t.numero, 0)
                    else:
                        t.pontos = 0
                    db.commit()
                    st.rerun()
                if c3.button("Excluir", key=f"excluir_{t.id}", type="primary"):
                    excluir_tentativa(db, t.id)
                    st.rerun()

db.close()

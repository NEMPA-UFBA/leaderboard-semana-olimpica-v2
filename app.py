import streamlit as st
from database import init_db
import importlib.util

# Ensure DB is ready (tables + default admin)
init_db()

st.set_page_config(
    page_title="Batalha Olimpica",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Hide default Streamlit sidebar navigation
st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize default page
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;600;700&display=swap');

    .nav-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 2rem;
        letter-spacing: 2px;
        background: linear-gradient(135deg, #f7971e, #ffd200);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- HEADER WITH NAVIGATION ---
col_title, col_nav = st.columns([1, 2])

with col_title:
    st.markdown('<div class="nav-title">BATALHA OLIMPICA</div>', unsafe_allow_html=True)

with col_nav:
    nav_cols = st.columns([1, 1, 1, 1, 1])

    if nav_cols[0].button("🏠 HOME", use_container_width=True, help="Pagina inicial"):
        st.session_state.current_page = "home"
        st.rerun()

    if nav_cols[1].button("🏆 LEADERBOARD", use_container_width=True, help="Ranking em tempo real"):
        st.session_state.current_page = "leaderboard"
        st.rerun()

    if nav_cols[2].button("📝 QUESTOES", use_container_width=True, help="Desafios da regata ativa"):
        st.session_state.current_page = "questoes"
        st.rerun()

    if nav_cols[3].button("⚙️ ADMIN", use_container_width=True, help="Painel de administrador"):
        st.session_state.current_page = "admin"
        st.rerun()

    if nav_cols[4].button("🔒 JUIZ", use_container_width=True, help="Area de acesso restrito"):
        st.session_state.current_page = "juiz"
        st.rerun()

st.divider()

# --- LOAD SELECTED PAGE ---
if st.session_state.current_page == "home":
    col_l, col_logo, col_r = st.columns([1, 1, 1])
    with col_logo:
        st.image("assets/images/semana-olimpica.jpeg", width=250)
    st.markdown(
        """
        <div style="text-align:center; padding:1rem 1rem 4rem;">
            <div style="font-family:'Bebas Neue',sans-serif; font-size:4.5rem; letter-spacing:4px; line-height:1;
                        background:linear-gradient(135deg,#f7971e,#ffd200); -webkit-background-clip:text;
                        -webkit-text-fill-color:transparent;">BATALHA OLIMPICA</div>
            <div style="font-family:'Outfit',sans-serif; color:#999; font-size:1.1rem; margin-top:0.5rem;
                        letter-spacing:2px; text-transform:uppercase;">Semana Olimpica 2026</div>
            <div style="margin-top:3rem; display:flex; justify-content:center; gap:2rem; flex-wrap:wrap;">
                <div style="background:linear-gradient(145deg,#1a1a2e,#16213e); border:1px solid #333;
                            border-radius:16px; padding:2rem 2.5rem; min-width:200px;
                            transition:border-color 0.2s, transform 0.2s; cursor:pointer;"
                     onmouseover="this.style.borderColor='#ffd200'; this.style.transform='translateY(-4px)';"
                     onmouseout="this.style.borderColor='#333'; this.style.transform='translateY(0)';">
                    <div style="font-family:'Bebas Neue',sans-serif; font-size:1.8rem; color:#ffd200;
                                letter-spacing:2px;">LEADERBOARD</div>
                    <div style="font-family:'Outfit',sans-serif; color:#888; font-size:0.85rem; margin-top:4px;">
                        Ranking em tempo real</div>
                </div>
                <div style="background:linear-gradient(145deg,#1a1a2e,#16213e); border:1px solid #333;
                            border-radius:16px; padding:2rem 2.5rem; min-width:200px;
                            transition:border-color 0.2s, transform 0.2s; cursor:pointer;"
                     onmouseover="this.style.borderColor='#ffd200'; this.style.transform='translateY(-4px)';"
                     onmouseout="this.style.borderColor='#333'; this.style.transform='translateY(0)';">
                    <div style="font-family:'Bebas Neue',sans-serif; font-size:1.8rem; color:#ffd200;
                                letter-spacing:2px;">QUESTOES</div>
                    <div style="font-family:'Outfit',sans-serif; color:#888; font-size:0.85rem; margin-top:4px;">
                        Desafios da regata ativa</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

elif st.session_state.current_page == "leaderboard":
    spec = importlib.util.spec_from_file_location("leaderboard_page", "pages/3_Leaderboard.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

elif st.session_state.current_page == "questoes":
    spec = importlib.util.spec_from_file_location("questoes_page", "pages/4_Questoes.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

elif st.session_state.current_page == "admin":
    spec = importlib.util.spec_from_file_location("admin_page", "pages/1_Admin.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

elif st.session_state.current_page == "juiz":
    spec = importlib.util.spec_from_file_location("juiz_page", "pages/2_Juiz.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] img {
            border-radius: 50%;
            clip-path: circle(46%);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.image("assets/images/logo NEMPA.png", width="content")
    st.markdown("### The Team (NEMPA)")

    st.markdown("**Project Lead**")
    st.markdown("*Prof. Dr. Roberto Sant'Anna*")

    st.write("")

    st.markdown("**Core Developers**")
    st.markdown("*Enzo Ribeiro*")
    st.markdown("*Gabriel Siron*")
    st.markdown("*Ikaro Vieira*")

    st.write("")

    st.markdown("**Scientific Developers**")
    st.markdown("*Iago Nunes*")

    st.divider()
    st.markdown("© 2026 NEMPA - UFBA")

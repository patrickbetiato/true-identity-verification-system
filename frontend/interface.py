import streamlit as st
import requests

st.markdown("""
    <style>
    body { background-color: #121212; color: #FFFFFF; }
    .stButton>button { background-color: #2B2B2B; color: white; border-radius: 10px; }
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    h1 {
        font-family: 'Inter', sans-serif !important;
        font-size: 3em;
        background: linear-gradient(to right, #FF0000, #FF7F00, #FFFF00, #00FF00, #0000FF, #8B00FF);
        -webkit-background-clip: text;
        color: transparent;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

st.image("/home/patrick/Documentos/Proj_Detector/data/iconm.png", width=150)
st.markdown("<h1>true-identity-verification-system</h1>", unsafe_allow_html=True)

perfil_link = st.text_input("Insira o link do perfil:")

st.sidebar.title("Verificador De Perfis")
st.sidebar.write("""
- Aqui será feito uma descrição do que é feito e como ele opera.
- Insira o link do perfil.
- Clique em *Analisar*.
- Veja os dados do perfil.
""")

BACKEND_URL = "http://127.0.0.1:8000/analyze/"

if st.button("Analisar"):
    if perfil_link:
        with st.spinner(' Buscando dados do perfil...'):
            try:
                payload = {"profile_link": perfil_link}
                response = requests.post(BACKEND_URL, json=payload, timeout=20)

                if response.status_code == 200:
                    data = response.json()
                    st.success("Dados do perfil carregados!")

                    st.write("---")
                    st.subheader(f"👤 @{data['username']}")
                    st.write(f"**Nome:** {data['full_name']}")
                    st.write(f"**Bio:** {data['bio']}")
                    st.write(f"**Seguidores:** {data['followers']}")
                    st.write(f"**Seguindo:** {data['following']}")
                    st.write(f"**Posts:** {data['posts']}")
                    st.write(f"**Verificado:** {'✅ Sim' if data['is_verified'] else '❌ Não'}")
                    st.write(f"**Privado:** {'🔒 Sim' if data['is_private'] else '🌍 Não'}")

                else:
                    st.error(f"Erro na análise. Código: {response.status_code}")

            except requests.exceptions.ConnectionError:
                st.error("Falha na conexão. Verifique se o backend está rodando.")
            except Exception as e:
                st.error(f"Erro inesperado: {e}")
    else:
        st.warning("Por favor, insira um link de perfil para analisar.")

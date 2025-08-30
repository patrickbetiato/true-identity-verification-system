import requests
import streamlit as st
import os
import matplotlib.pyplot as plt

img_path = os.path.join(os.path.dirname(__file__), "../data/iconm.png")

st.markdown("""
    <a href="https://github.com/patrickbetiato/true-identity-verification-system" target="_blank">
        <div class="github-icon">
            <svg height="32" aria-hidden="true" viewBox="0 0 16 16" version="1.1" width="32" data-view-component="true">
                <path fill="#FFFFFF" fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.67.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
            </svg>
        </div>
    </a>
    """,
    unsafe_allow_html=True,
)

st.markdown("""
    <style>
    body { background-color: #121212; color: #FFFFFF; }
    .stButton>button { background-color: #2B2B2B; color: white; border-radius: 10px; }
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    h1 {
        font-family: 'Inter', sans-serif !important;
        font-size: 3em;
        background: linear-gradient(45deg, #F58529, #DD2A7B, #8134AF, #515BD4);
        -webkit-background-clip: text;
        color: transparent;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
        text-align: center;
    }
            
    .stSidebar {
        width: 350px !important;
        min-width: 350px !important;
    }
    </style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
st.markdown("<h1>true-identity-verification-system</h1>", unsafe_allow_html=True)
with col2:
    st.image(img_path, width=200)

perfil_link = st.text_input("Insira o link do perfil:",
  placeholder="Digite o nome de usuário, exemplo: 'patrickbetiato'")

st.sidebar.title("Verificador de Perfis")

st.sidebar.markdown("""
💡 **Sobre o sistema:**  
O True Identity Verification System analisa perfis públicos do Instagram e fornece uma **estimativa de confiabilidade** baseada em métricas públicas do perfil. Ele utiliza informações como número de seguidores, seguindo, posts, bio, conta verificada e privada para estimar a probabilidade de o perfil ser **real ou falso**.

🛠 **Como usar:**  
1. Insira o link do perfil que deseja analisar.  
2. Clique no botão **Analisar**.  
3. Veja os dados do perfil na tela principal e a estimativa de confiabilidade no gráfico lateral.

📊 **Interpretação do gráfico:**  
- **Barras horizontais:** representam a porcentagem de confiabilidade do perfil.  
- **Cor verde ("Real")**: indica a probabilidade do perfil ser verdadeiro.  
- **Cor vermelha ("Fake")**: indica a probabilidade do perfil ser falso ou suspeito.  
- Quanto maior a barra verde, mais confiável o perfil parece ser.

⚠️ **Avisos importantes:**  
- Apenas **perfis públicos** podem ser analisados.  
- O modelo utiliza apenas **dados disponíveis publicamente**; não acessa mensagens privadas ou seguidores ocultos.  
- É uma **estimativa**, não uma certificação oficial; perfis suspeitos podem ainda ser reais.

🔎 **Detalhes sobre as métricas:**  
- **Seguidores:** quantidade de pessoas que seguem o perfil.  
- **Seguindo:** quantidade de pessoas que o perfil segue.  
- **Posts:** quantidade de publicações no perfil.  
- **Bio:** tamanho do texto da biografia, usado como uma métrica de autenticidade.  
- **Verificado:** contas com selo azul são consideradas mais confiáveis.  
- **Privado:** contas privadas têm dados limitados para análise.

📌 **Uso responsável:**  
- Este sistema é apenas para **avaliação informativa**.  
- Não compartilhe resultados para assediar ou prejudicar outros usuários.
""")

logged_in = st.checkbox("Estou logado no Instagram e posso acessar o perfil público")

BACKEND_URL = "https://true-identity-verification-system.onrender.com/analyze/"

if st.button("Analisar"):
    if not logged_in:
        st.warning("Por favor, conecte-se ao Instagram antes de analisar.")
    elif not perfil_link:
        st.warning("Por favor, insira um link de perfil para analisar.")
    else:
        with st.spinner('Buscando dados do perfil...'):
            try:
                payload = {"profile_link": perfil_link}
                response = requests.post(BACKEND_URL, json=payload, timeout=60)

                if response.status_code == 200:
                    data = response.json()
                    st.success("Dados do perfil carregados!")

                    st.write("---")
                    st.subheader(f"👤 @{data['username']}")

                    col1, col2 = st.columns([2, 1])

                    with col1:
                        st.write(f"**Nome:** {data['full_name']}")
                        st.write(f"**Bio:** {data['bio']}")
                        st.write(f"**Seguidores:** {data['followers']}")
                        st.write(f"**Seguindo:** {data['following']}")
                        st.write(f"**Posts:** {data['posts']}")
                        st.write(f"**Verificado:** {'✅ Sim' if data['is_verified'] else '❌ Não'}")
                        st.write(f"**Privado:** {'🔒 Sim' if data['is_private'] else '🌍 Não'}")

                    prediction = data.get("prediction")
                    prob = data.get("probability")

                    with col2:
                        if prediction is not None and prob is not None:
                            prob_real = prob if prediction == 0 else 1 - prob
                            prob_fake = 1 - prob_real

                            st.write("### 🔮 Confiabilidade")

                            fig, ax = plt.subplots(figsize=(3, 2), facecolor="none")
                            bars = ax.barh(
                                ["Real", "Fake"],
                                [prob_real * 100, prob_fake * 100],
                                color=["#4CAF50", "#F44336"],
                                height=0.6
                            )

                            ax.set_xlim(0, 100)
                            ax.set_facecolor("none")
                            ax.spines["top"].set_visible(False)
                            ax.spines["right"].set_visible(False)
                            ax.spines["left"].set_visible(False)
                            ax.spines["bottom"].set_visible(False)
                            ax.tick_params(left=False, bottom=False, labelsize=10, colors="white")
                            ax.set_yticklabels(["Real", "Fake"], color="white", fontsize=10)

                            for bar in bars:
                                width = bar.get_width()
                                ax.text(
                                    width + 1, bar.get_y() + bar.get_height() / 2,
                                    f"{width:.1f}%",
                                    va="center", ha="left", fontsize=10, color="white"
                                )

                            plt.tight_layout()
                            st.pyplot(fig, transparent=True)

                        else:
                            st.warning("O modelo não retornou probabilidade de classificação.")

                else:
                    st.error(f"Erro na análise. Código: {response.status_code}")

            except requests.exceptions.RequestException as e:
                st.error(f"Erro na conexão com o backend: {e}")
            except Exception as e:
                st.error(f"Erro inesperado: {e}")

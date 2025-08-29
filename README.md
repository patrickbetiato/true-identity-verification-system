# True Identity Verification System

Uma aplicação em Python que utiliza **Streamlit** e **Instaloader** para analisar perfis do Instagram e estimar a probabilidade de serem **fakes ou gerados por IA**.

> ⚠️ Projeto em desenvolvimento: a parte de **aprendizado de máquina** ainda será implementada para análise avançada.

---

## Funcionalidades

* Interface interativa com Streamlit.
* Análise de perfis públicos do Instagram via Instaloader.
* Sistema inicial de detecção de perfis suspeitos.
* Exportação e visualização de dados (CSV).

---

## Estrutura do projeto

```
true-identity-verification-system/
│
├─ data/            # Imagens, CSVs de teste
├─ frontend/        # Código da interface Streamlit
├─ backend/         # Lógica do backend (API, análise de dados)
├─ notebooks/       # Notebooks para experimentos de ML
├─ src/             # Scripts auxiliares
├─ requirements.txt # Dependências do projeto
└─ inicial.py       # Arquivo principal para rodar localmente
```

---

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/SEU_USUARIO/true-identity-verification-system.git
cd true-identity-verification-system
```

2. Crie e ative o ambiente virtual:

```bash
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```


3. Rode a aplicação Streamlit:

```bash
streamlit run frontend/interface.py
```

---

## Uso

* Digite o nome de usuário do Instagram na interface.
* O sistema irá coletar dados do perfil (publicamente disponíveis) e indicar **uma estimativa inicial de probabilidade de ser fake**.
* Futuras versões incluirão **modelos de aprendizado de máquina** para análise mais precisa.

---

## Próximos passos

* Implementar algoritmo de **detecção via aprendizado de máquina**.
* Adicionar métricas de confiabilidade e relatórios gráficos.
* Hospedar a aplicação na nuvem.

---

## Licença

MIT License – veja o arquivo [LICENSE](LICENSE).

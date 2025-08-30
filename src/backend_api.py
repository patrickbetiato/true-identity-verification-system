from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import instaloader
import joblib
import os
import numpy as np

# Caminho do modelo salvo
MODEL_PATH = "./assets/modelo_fake.pkl"

# Carrega o modelo ao iniciar a API
if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")
        model = None
else:
    model = None

# Instância do Instaloader
L = instaloader.Instaloader()

# Cria a aplicação FastAPI
app = FastAPI(title="API do Detector de Perfis")

# Define o formato dos dados recebidos (link do perfil)
class ProfileRequest(BaseModel):
    profile_link: str

@app.get("/")
def read_root():
    return {"status": "API do Detector de Perfis está online."}

@app.post("/analyze/")
def analyze_profile(request: ProfileRequest):
    try:
        if model is None:
            raise HTTPException(status_code=500, detail="Modelo não carregado.")

        # Extrair username do link
        username = request.profile_link.rstrip("/").split("/")[-1]
        profile = instaloader.Profile.from_username(L.context, username)

        # Extrair features na mesma ordem que o treino
        features = [
            profile.followers,             # followers
            profile.followees,             # following
            profile.mediacount,            # posts
            int(profile.is_verified),      # is_verified
            int(profile.is_private),       # is_private
            len(profile.biography)         # bio_length
        ]

        # Converter para numpy array (1 linha de dados)
        X = np.array(features).reshape(1, -1)

        # Fazer a previsão
        prediction = model.predict(X)[0]  # 0 = real, 1 = fake (ajuste se for diferente)

        # Probabilidade (se o modelo suportar)
        prob = None
        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(X)[0][prediction]

        return {
            "username": profile.username,
            "full_name": profile.full_name,
            "bio": profile.biography,
            "followers": profile.followers,
            "following": profile.followees,
            "posts": profile.mediacount,
            "is_verified": profile.is_verified,
            "is_private": profile.is_private,
            "profile_link": f"https://instagram.com/{profile.username}",
            "prediction": int(prediction),  # 0 ou 1
            "probability": float(prob) if prob is not None else None,
            "message": "Perfil analisado com sucesso."
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao analisar perfil: {str(e)}")

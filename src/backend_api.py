from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import instaloader

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
        username = request.profile_link.rstrip("/").split("/")[-1]
        profile = instaloader.Profile.from_username(L.context, username)

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
            "message": "Perfil analisado com sucesso."
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao analisar perfil: {str(e)}")

from fastapi import FastAPI
from app.core.config import settings
from app.api.routes.auth import router as auth_router
from app.api.routes.produtos import router as produtos_router
from app.api.routes.unidades import router as unidades_router
from app.api.routes.produto_unidades import router as produto_unidades_router
from app.api.routes.estoques import router as estoques_router
from app.api.routes import pedidos
from app.api.routes import pagamentos
from app.api.routes import consentimentos
from app.api.routes import fidelidade


app = FastAPI(
    title=settings.APP_NAME,
    description="Backend da Rede Raízes do Nordeste",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(produtos_router)
app.include_router(unidades_router)
app.include_router(produto_unidades_router)
app.include_router(estoques_router)
app.include_router(pedidos.router)
app.include_router(pagamentos.router)
app.include_router(consentimentos.router)
app.include_router(fidelidade.router)

@app.get("/")
def inicio():
    return {
        "mensagem": "API Rede Raízes do Nordeste está funcionando!"
    }

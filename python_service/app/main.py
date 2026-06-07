from fastapi import FastAPI
from app.routers import care_groups, tasks, protocols

app = FastAPI(title="Orquestração de Cuidado API", version="0.1.0")

app.include_router(care_groups.router)
app.include_router(tasks.router)
app.include_router(protocols.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

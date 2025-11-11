from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

app = FastAPI(title="Validador de Certificados - IADados")

# Simulação de base de dados (poderia ser SQLite)
CERTIFICATES = {
    "ABC123": {"nome": "Vitor Rafael Ribeiro Pereira", "curso": "IA Generativa com RAG, Fine Tuning e Agentes de IA", "status": "válido"},
    "XYZ789": {"nome": "Ana Clara Souza", "curso": "IA Generativa com RAG, Fine Tuning e Agentes de IA", "status": "válido"},
    "TEST000": {"nome": "Certificado de Teste", "curso": "Sistema de Validação", "status": "válido"},
}

@app.get("/validate")
def validate_certificate(id: str = Query(..., description="Código do certificado")):
    cert = CERTIFICATES.get(id)
    if not cert:
        raise HTTPException(status_code=404, detail="Certificado não encontrado.")
    
    return JSONResponse(content={
        "codigo": id,
        "status": cert["status"],
        "nome": cert["nome"],
        "curso": cert["curso"]
    })

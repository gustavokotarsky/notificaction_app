from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form
from starlette.responses import JSONResponse
from starlette.requests import Request
from fastapi_mail import FastMail, MessageSchema
from pydantic import BaseModel, EmailStr
from typing import Any, List, Dict
from conf import conf

class EmailSchema(BaseModel):
    email: List[EmailStr]
    walletAddress: str

app = FastAPI()

@app.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:
    walletAddress=email.dict().get("walletAddress")
    link = f"https://www.blockchain.com/en/search?search={walletAddress}"
    html = f"A sua carteira: {walletAddress} houve alteração.\nAcesse o link {link} para monitorar as operações."
    message = MessageSchema(
        subject="Monitoracao de Carteiras: Houve alteracao em uma das suas carteiras monitoradass",
        recipients=email.dict().get("email"),  # List of recipients, as many as you can pass
        body=html,
        )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
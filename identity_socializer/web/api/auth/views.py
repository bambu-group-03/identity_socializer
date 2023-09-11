from fastapi import APIRouter
router = APIRouter()
from identity_socializer.web.api.echo.schema import Message

@router.post("/signup", response_model=Message)
async def obtener_juanito(
    incoming_message: Message,
):
  ret = Message(message="lo que yo quiera 2")
  return ret
from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.db_helper import db_helper
from ..database.models import User
from ..repository.chat import respond
from ..schemas.chat import Response
from ..services.auth import auth_service

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=Response)
async def chat(
    user_query: str = Form(...),
    current_user: User = Depends(auth_service.get_authenticated_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    if not user_query:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    # if file:
    #     # Обрабатываем файл, если он был предоставлен
    #     pdf_extractor(file.filename, current_user, session=session)

    return await respond(current_user, session=session, instruction=user_query)

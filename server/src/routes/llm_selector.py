from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..config.llm_list import LLMNameEnum
from ..database.db_helper import db_helper
from ..database.models import User
from ..repository.llm_selector import llm_selector
from ..services.auth import auth_service

router = APIRouter(prefix="/llm_selector", tags=["Chat"])


@router.post("/")
async def read_comments(
    llm_name: LLMNameEnum = Form(...),
    current_user: User = Depends(auth_service.get_authenticated_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    try:
        await llm_selector(llm_name, current_user, session=session)
        return {"message": "LLM selected successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

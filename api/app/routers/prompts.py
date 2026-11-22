from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/prompts", tags=["prompts"])
DbSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=schemas.PromptRead, status_code=201)
def create_prompt(prompt: schemas.PromptCreate, db: DbSession):
    return crud.create_prompt(db, prompt)


@router.get("", response_model=list[schemas.PromptRead])
def get_prompts(db: DbSession):
    return crud.get_prompts(db)


@router.get("/{prompt_id}", response_model=schemas.PromptRead)
def get_prompt(prompt_id: int, db: DbSession):
    prompt = crud.get_prompt(db, prompt_id)
    if prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt

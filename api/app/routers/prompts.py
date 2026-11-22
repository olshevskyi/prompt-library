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


@router.patch("/{prompt_id}", response_model=schemas.PromptRead)
def update_prompt(
    prompt_id: int, prompt: schemas.PromptUpdate, db: DbSession
):
    db_prompt = crud.get_prompt(db, prompt_id)
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return crud.update_prompt(db, db_prompt, prompt)


@router.delete("/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: int, db: DbSession):
    db_prompt = crud.get_prompt(db, prompt_id)
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    crud.delete_prompt(db, db_prompt)

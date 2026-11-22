from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


def create_prompt(db: Session, prompt: schemas.PromptCreate) -> models.Prompt:
    db_prompt = models.Prompt(**prompt.model_dump(exclude={"tags"}))
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt


def get_prompts(db: Session) -> list[models.Prompt]:
    stmt = select(models.Prompt)
    return list(db.scalars(stmt).all())


def get_prompt(db: Session, prompt_id: int) -> models.Prompt | None:
    result = db.get(models.Prompt, prompt_id)
    return result

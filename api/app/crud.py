from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


def create_prompt(db: Session, prompt: schemas.PromptCreate) -> models.Prompt:
    db_prompt = models.Prompt(**prompt.model_dump(exclude={"tags"}))
    db_prompt.tags = get_or_create_tags(db, prompt.tags)
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt


def get_prompts(
    db: Session,
    category: str | None = None,
    favorite: bool | None = None,
    tag: str | None = None
) -> list[models.Prompt]:
    stmt = select(models.Prompt)
    if category is not None:
        stmt = stmt.where(models.Prompt.category == category)
    if favorite is not None:
        stmt = stmt.where(models.Prompt.is_favorite == favorite)
    if tag is not None:
        stmt = stmt.where(models.Prompt.tags.any(models.Tag.name == tag))
    return list(db.scalars(stmt).all())


def get_prompt(db: Session, prompt_id: int) -> models.Prompt | None:
    result = db.get(models.Prompt, prompt_id)
    return result


def update_prompt(
    db: Session, db_prompt: models.Prompt, prompt: schemas.PromptUpdate
) -> models.Prompt:
    changes = prompt.model_dump(exclude_unset=True, exclude_none=True, exclude={"tags"})
    for field, value in changes.items():
        setattr(db_prompt, field, value)
    if prompt.tags is not None:
        db_prompt.tags = get_or_create_tags(db, prompt.tags)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt


def delete_prompt(db: Session, db_prompt: models.Prompt) -> None:
    db.delete(db_prompt)
    db.commit()


def get_or_create_tags(db: Session, tag_names: list[str]) -> list[models.Tag]:
    tags = []
    for name in set(tag_names):
        tag = db.scalar(select(models.Tag).where(models.Tag.name == name))
        if tag is None:
            tag = models.Tag(name=name)
            db.add(tag)
        tags.append(tag)
    return tags
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.database import get_db
from src.models import Task, User
from src.schemas import TaskCreate, TaskUpdate, Task as TaskSchema
from src.auth import get_current_user

router = APIRouter()

@router.post("/tasks", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_task = Task(**task.dict(), user_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks", response_model=List[TaskSchema])
def read_tasks(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros por página"),
    status: Optional[bool] = Query(None, description="Filtrar por estado de tarea"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # build base query
    query = db.query(Task).filter(Task.user_id == current_user.id)
    
    # apply the filters if any
    if status is not None:
        query = query.filter(Task.status == status)
    
    # apply pagination
    tasks = query.offset(skip).limit(limit).all()
    return tasks

@router.get("/tasks/{task_id}", response_model=TaskSchema)
def read_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # gets the asked task
    task = db.query(Task).filter(
        Task.id == task_id, 
        Task.user_id == current_user.id
    ).first()
    
    # if the asked task doesn't exists, raise 404 error
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return task

@router.put("/tasks/{task_id}", response_model=TaskSchema)
def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # gets the asked task
    task = db.query(Task).filter(
        Task.id == task_id, 
        Task.user_id == current_user.id
    ).first()
    
    # if the asked task doesn't exists, raise 404 error
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Actualizar solo los campos proporcionados
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    db.commit()
    db.refresh(task)
    return task

@router.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id, 
        Task.user_id == current_user.id
    ).first()
    
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
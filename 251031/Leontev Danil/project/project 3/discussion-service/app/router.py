from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID
from .schemas import Message, MessageCreate, MessageUpdate
from .repository import MessageRepository
from .client import main_service_client

router = APIRouter(prefix="/api/v1.0/messages", tags=["messages"])

@router.post("/", response_model=Message)
async def create_message(message: MessageCreate):
    # Проверяем существование пользователя и топика
    if not await main_service_client.verify_user(message.user_id):
        raise HTTPException(status_code=404, detail="User not found")
    if not await main_service_client.verify_topic(message.topic_id):
        raise HTTPException(status_code=404, detail="Topic not found")
    
    return await MessageRepository.create(message)

@router.get("/{message_id}", response_model=Message)
async def get_message(message_id: UUID):
    message = await MessageRepository.get(message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@router.get("/topic/{topic_id}", response_model=List[Message])
async def get_topic_messages(topic_id: UUID):
    # Проверяем существование топика
    if not await main_service_client.verify_topic(topic_id):
        raise HTTPException(status_code=404, detail="Topic not found")
    
    return await MessageRepository.get_by_topic(topic_id)

@router.put("/{message_id}", response_model=Message)
async def update_message(message_id: UUID, message: MessageUpdate):
    updated_message = await MessageRepository.update(message_id, message)
    if not updated_message:
        raise HTTPException(status_code=404, detail="Message not found")
    return updated_message

@router.delete("/{message_id}")
async def delete_message(message_id: UUID):
    if not await MessageRepository.delete(message_id):
        raise HTTPException(status_code=404, detail="Message not found")
    return {"status": "success"} 
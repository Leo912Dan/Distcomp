import httpx
from typing import Optional
from uuid import UUID

class MainServiceClient:
    def __init__(self, base_url: str = "http://main-service:24110"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)

    async def verify_user(self, user_id: UUID) -> bool:
        try:
            response = await self.client.get(f"/api/v1.0/users/{user_id}")
            return response.status_code == 200
        except Exception:
            return False

    async def verify_topic(self, topic_id: UUID) -> bool:
        try:
            response = await self.client.get(f"/api/v1.0/topics/{topic_id}")
            return response.status_code == 200
        except Exception:
            return False

    async def close(self):
        await self.client.aclose()

# Создаем глобальный экземпляр клиента
main_service_client = MainServiceClient() 
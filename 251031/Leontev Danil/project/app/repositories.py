from typing import Dict, Generic, TypeVar, List, Optional

T = TypeVar('T')

class InMemoryRepository(Generic[T]):
    def __init__(self) -> None:
        self.store: Dict[int, T] = {}
        self.current_id: int = 1

    def create(self, entity: T) -> T:
        entity.id = self.current_id
        self.store[self.current_id] = entity
        self.current_id += 1
        return entity

    def find_by_id(self, id: int) -> Optional[T]:
        return self.store.get(id)

    def find_all(self) -> List[T]:
        return list(self.store.values())

    def update(self, id: int, entity: T) -> Optional[T]:
        if id in self.store:
            entity.id = id
            self.store[id] = entity
            return entity
        return None

    def delete(self, id: int) -> bool:
        if id not in self.store:
            return False
        del self.store[id]
        return True
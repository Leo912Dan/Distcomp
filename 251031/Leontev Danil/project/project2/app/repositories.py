from typing import Dict, Generic, TypeVar, List, Optional

# Определяем тип-переменную для дженериков
T = TypeVar('T')

class InMemoryRepository(Generic[T]):
    """
    Репозиторий для хранения данных в памяти.
    Реализует паттерн Repository для работы с сущностями.
    
    Attributes:
        store (Dict[int, T]): Словарь для хранения сущностей, где ключ - id, значение - сущность
        current_id (int): Счетчик для генерации уникальных id
    """
    
    def __init__(self) -> None:
        """
        Инициализирует репозиторий.
        Создает пустой словарь для хранения сущностей и устанавливает начальный id.
        """
        self.store: Dict[int, T] = {}  # Хранилище сущностей
        self.current_id: int = 1  # Начальный id для новых сущностей

    def create(self, entity: T) -> T:
        """
        Создает новую сущность в хранилище.
        
        Args:
            entity (T): Сущность для создания
            
        Returns:
            T: Созданная сущность с присвоенным id
        """
        entity.id = self.current_id
        self.store[self.current_id] = entity
        self.current_id += 1
        return entity

    def find_by_id(self, id: int) -> Optional[T]:
        """
        Находит сущность по её id.
        
        Args:
            id (int): Идентификатор искомой сущности
            
        Returns:
            Optional[T]: Найденная сущность или None, если сущность не найдена
        """
        return self.store.get(id)

    def find_all(self) -> List[T]:
        """
        Возвращает список всех сущностей в хранилище.
        
        Returns:
            List[T]: Список всех сущностей
        """
        return list(self.store.values())

    def update(self, id: int, entity: T) -> Optional[T]:
        """
        Обновляет существующую сущность.
        
        Args:
            id (int): Идентификатор обновляемой сущности
            entity (T): Новая версия сущности
            
        Returns:
            Optional[T]: Обновленная сущность или None, если сущность не найдена
        """
        if id in self.store:
            entity.id = id
            self.store[id] = entity
            return entity
        return None

    def delete(self, id: int) -> bool:
        """
        Удаляет сущность по её id.
        
        Args:
            id (int): Идентификатор удаляемой сущности
            
        Returns:
            bool: True, если сущность была удалена, False, если сущность не найдена
        """
        if id not in self.store:
            return False
        del self.store[id]
        return True
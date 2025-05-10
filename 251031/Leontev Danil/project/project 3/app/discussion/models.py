from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from datetime import datetime
import uuid

class Message(Model):
    __keyspace__ = 'discussion'
    __table_name__ = 'messages'
    
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    content = columns.Text(required=True)
    topic_id = columns.UUID(required=True, index=True)
    user_id = columns.UUID(required=True, index=True)
    created_at = columns.DateTime(default=datetime.utcnow)
    updated_at = columns.DateTime(default=datetime.utcnow)
    
    class Meta:
        get_pk_field = 'id' 
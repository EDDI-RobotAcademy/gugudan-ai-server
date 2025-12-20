from datetime import datetime
from typing import TypedDict, Optional

class CounselRow(TypedDict):
    role: str
    message: str
    parent: Optional[int]
    created_at: datetime
from pydantic import BaseModel


class NetworkSummary(BaseModel):
    total_connections: int
    web_connections: int
    total_web_requests: int
    bots: dict

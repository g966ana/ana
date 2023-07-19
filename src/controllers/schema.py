from pydantic import BaseModel

class HostpoolConfigs(BaseModel):
    subscription_id: str
    resource_group: str
    host_pool_name: str


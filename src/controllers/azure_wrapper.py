from fastapi import APIRouter, HTTPException
from src.controllers.schema import HostpoolConfigs
from azure.identity import InteractiveBrowserCredential
from azure.mgmt.desktopvirtualization import DesktopVirtualizationMgmtClient
from azure.mgmt.desktopvirtualization.models import AgentUpdateProperties, HostPool, MaintenanceWindowProperties, Sku

router = APIRouter()

@router.post("/create_host_pool")
def create_host_pool(hostpool_configs: HostpoolConfigs):
    # Create the credential object using the InteractiveBrowserCredential
    credential = InteractiveBrowserCredential(
        tenant_id="d9914fb9-ea93-4d1e-af87-8bbcd04fcc62"
    )
    client = DesktopVirtualizationMgmtClient(credential, hostpool_configs.subscription_id)

    host_pool = HostPool(
        host_pool_type = "Personal",
        load_balancer_type = "Persistent",
        preferred_app_group_type = "Desktop",
        location = "eastus",
        managed_by = None,
        kind = None,
        tags = None,
        personal_desktop_assignment_type= "Automatic",
        friendly_name="friendly",
        description="des1",
        vm_template="{\"domain\":\"gmail.com\",\"galleryImageOffer\":\"windows-11\",\"galleryImagePublisher\":\"microsoftwindowsdesktop\",\"galleryImageSKU\":\"win11-21h2-ent\",\"imageType\":\"Gallery\",\"customImageId\":null,\"namePrefix\":\"HP-Personal\",\"osDiskType\":\"StandardSSD_LRS\",\"vmSize\":{\"id\":\"Standard_D2s_v3\",\"cores\":2,\"ram\":8},\"galleryItemId\":\"microsoftwindowsdesktop.windows-11win11-21h2-ent\",\"hibernate\":false,\"diskSizeGB\":0,\"securityType\":\"Standard\",\"secureBoot\":false,\"vTPM\":false}",
        sku=Sku(name="Standard_D4s_v3"),  # Replace with your desired VM SKU
        max_session_limit=5,
        agent_update = AgentUpdateProperties(type="Scheduled",
                                             use_session_host_local_time=False,
                                             maintenance_window_time_zone="Alaskan Standard Time",
                                             maintenance_windows=[
                                                 MaintenanceWindowProperties(hour=7, day_of_week="Friday"),
                                                 MaintenanceWindowProperties(hour=8, day_of_week="Saturday")
                                                ]
                                            )
    )

    try:
        client.host_pools.create_or_update(
            hostpool_configs.resource_group,
            hostpool_configs.host_pool_name,
            host_pool
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": f"Host pool '{hostpool_configs.host_pool_name}' created successfully."}

@router.get("/get_host_pools")
def list_host_pools(hostpool_configs: HostpoolConfigs):
    # Create the credential object using the InteractiveBrowserCredential
    credential = InteractiveBrowserCredential(
        tenant_id="d9914fb9-ea93-4d1e-af87-8bbcd04fcc62"
    )
    client = DesktopVirtualizationMgmtClient(credential, hostpool_configs.subscription_id)

    host_pools_paged_object = client.host_pools.list_by_resource_group(
        resource_group_name=hostpool_configs.resource_group
    )
    
    item_list = []

    for host_pool in host_pools_paged_object:
        # Convert each item to a dictionary
        host_pool_dict = vars(host_pool)
        item_list.append(host_pool_dict)

    return {"data" : item_list}

@router.delete("/delete_host_pools")
def delete_host_pool(hostpool_configs: HostpoolConfigs):
    # Create the credential object using the InteractiveBrowserCredential
    credential = InteractiveBrowserCredential(
        tenant_id="d9914fb9-ea93-4d1e-af87-8bbcd04fcc62"
    )
    client = DesktopVirtualizationMgmtClient(credential, hostpool_configs.subscription_id)

    client.host_pools.delete(resource_group_name=hostpool_configs.resource_group, host_pool_name=hostpool_configs.host_pool_name, force=True)
    
    return {"message": f"Host pool '{hostpool_configs.host_pool_name}' deleted successfully"}







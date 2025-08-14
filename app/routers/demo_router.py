from fastapi import APIRouter, Depends
#from app.schema.demo_dto import Demo as DemoDTO
from app.services.demo_serv import Demo as DemoServ
from app.configs.dependencies import get_demo_service

demoRoutes = APIRouter(prefix="/demos", tags=["demos"])

@demoRoutes.get("/{demo_id}")
def find_demo(demo_id: int, service: DemoServ = Depends(get_demo_service)):
    result = service.findDemo(demo_id)
    return result

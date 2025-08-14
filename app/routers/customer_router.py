from fastapi import APIRouter, Depends
#from app.schema.customer_dto import Customer as CustomerDTO
from app.services.customer_serv import Customer as CustomerServ
from app.configs.dependencies import get_customer_service

customerRoutes = APIRouter(prefix="/customers", tags=["customers"])

@customerRoutes.get("/{customer_id}")
def find_customer(customer_id: int, service: CustomerServ = Depends(get_customer_service)):
    result = service.findCustomer(customer_id)
    return result

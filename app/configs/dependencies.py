from fastapi import Depends
from app.repository.user_repo import User as UserRepo
from app.services.user_serv import User as UserServ

from app.repository.customer_repo import Customer as CustomerRepo
from app.services.customer_serv import Customer as CustomerServ

from app.repository.demo_repo import Demo as DemoRepo
from app.services.demo_serv import Demo as DemoServ

from app.repository.email_repo import Email as EmailRepo
from app.services.email_serv import Email as EmailServ

def get_user_repository() -> UserRepo:
    return UserRepo()

def get_user_service(repo: UserRepo = Depends(get_user_repository)):
    return UserServ(repo)


def get_customer_repository() -> CustomerRepo:
    return CustomerRepo()

def get_customer_service(repo: CustomerRepo = Depends(get_customer_repository)):
    return CustomerServ(repo)

def get_demo_repository() -> DemoRepo:
    return DemoRepo()

def get_demo_service(repo: DemoRepo = Depends(get_demo_repository)):
    return DemoServ(repo)

def get_email_repository() -> EmailRepo:
    return EmailRepo()

def get_email_service(repo: EmailRepo = Depends(get_email_repository)):
    return EmailServ(repo)
from app.schema.email_dto import Email as EmailDTO
from app.repository.email_repo import Email as EmailRepo

class Email:
    def __init__(self, repo: EmailRepo):
        self.repo = repo

    def sendEmail(self, email: EmailDTO):
        #result = self.repo.sendEmail(email)
        result = self.repo.sendEmailBackground(email)
        return result
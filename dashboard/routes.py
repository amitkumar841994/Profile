from fastapi import APIRouter
from .views import UserJobsExperience,GitRepo ,UploadFileHandler,MessageHandler


router = APIRouter()

userrxp = UserJobsExperience()
userupload = UploadFileHandler()
gitrepo = GitRepo()
message = MessageHandler()

router.include_router(userrxp.router)
router.include_router(gitrepo.router)
router.include_router(userupload.router)
router.include_router(message.router)

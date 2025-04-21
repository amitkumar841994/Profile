from fastapi import APIRouter
from .views import UserJobsExperience,GitRepo ,UploadFileHandler


router = APIRouter()

userrxp = UserJobsExperience()
userupload = UploadFileHandler()
gitrepo = GitRepo()

router.include_router(userrxp.router)
router.include_router(gitrepo.router)
router.include_router(userupload.router)

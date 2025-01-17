from fastapi import APIRouter
from .views import UserJobsExperience,GitRepo

# Instantiate the class-based view
userrxp = UserJobsExperience()
router = userrxp.router

gitrepo =GitRepo()
router = gitrepo.router
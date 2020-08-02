from .model.UserModel import *
from .model.TutorialRelatedModel import \
    Category, Tutorial, Graph, Code, ExecResultJson, Uploads
from .model.TranslationModels import ENUS, ZHCN, ENUSGraphContent, ZHCNGraphContent

model_list = [User,
              Category, Tutorial, Graph, Code, ExecResultJson, Uploads,
              ENUS, ZHCN,
              ENUSGraphContent, ZHCNGraphContent]

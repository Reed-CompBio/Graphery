from .model.UserModel import *
from .model.TutorialRelatedModel import \
    Category, Tutorial, Graph, Code, ExecResultJson, Uploads
from .model.TranslationModels import ENUS, ZHCN, ENUSGraphContent, ZHCNGraphContent, ESGraphContent, ES

model_list = [User,
              Category, Tutorial, Graph, Code, ExecResultJson, Uploads,
              ENUS, ZHCN, ES,
              ENUSGraphContent, ZHCNGraphContent, ESGraphContent]

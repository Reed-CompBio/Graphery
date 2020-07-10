from .model.UserModel import *
from .model.TutorialRelatedModel import \
    Category, Tutorial, Graph, Code, ExecResultJson
from .model.TranslationModels import ENUS, ZHCN, ENUSGraphContent, ZHCNGraphContent

model_list = [User,
              Category, Tutorial, Graph, Code, ExecResultJson,
              ENUS, ZHCN,
              ENUSGraphContent, ZHCNGraphContent]

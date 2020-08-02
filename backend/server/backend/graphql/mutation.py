import graphene


from backend.graphql.admin_mutations import UpdateCategory, UpdateTutorialAnchor, UpdateGraph, UpdateCode, \
    UploadStatics, UpdateTutorialContent, DeleteStatics, UpdateGraphInfoContent, UpdateResultJson
from backend.graphql.user_mutations import Login, Logout, Register


class Mutation(graphene.ObjectType):
    register = Register.Field()
    login = Login.Field()
    logout = Logout.Field()
    update_category = UpdateCategory.Field()
    update_tutorial_anchor = UpdateTutorialAnchor.Field()
    update_graph = UpdateGraph.Field()
    update_code = UpdateCode.Field()
    upload_statics = UploadStatics.Field()
    delete_statics = DeleteStatics.Field()
    update_tutorial_content = UpdateTutorialContent.Field()
    update_graph_info_content = UpdateGraphInfoContent.Field()
    update_result_json = UpdateResultJson.Field()

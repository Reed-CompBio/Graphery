import graphene


from backend.graphql.admin_mutations import UpdateCategory, UpdateTutorialAnchor, UpdateGraph, UpdateCode, \
    UploadStatic, UpdateTutorialContent, DeleteStatic, UpdateGraphInfoContent, UpdateResultJson, DeleteContent, \
    RefreshInvitationCode, ExecuteAllCode
from backend.graphql.user_mutations import Login, Logout, Register, ChangePassword


class Mutation(graphene.ObjectType):
    refresh_invitation_code = RefreshInvitationCode.Field()
    register = Register.Field()
    login = Login.Field()
    logout = Logout.Field()
    change_password = ChangePassword.Field()
    update_category = UpdateCategory.Field()
    update_tutorial_anchor = UpdateTutorialAnchor.Field()
    update_graph = UpdateGraph.Field()
    update_code = UpdateCode.Field()
    upload_static = UploadStatic.Field()
    delete_static = DeleteStatic.Field()
    update_tutorial_content = UpdateTutorialContent.Field()
    update_graph_info_content = UpdateGraphInfoContent.Field()
    update_result_json = UpdateResultJson.Field()
    delete_content = DeleteContent.Field()
    execute_all_code = ExecuteAllCode.Field()

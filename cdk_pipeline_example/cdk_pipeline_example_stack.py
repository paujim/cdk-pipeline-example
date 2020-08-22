import constants
from aws_cdk import (
    core,
    pipelines,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_ssm as ssm,
)


class SSMStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        param = ssm.StringParameter(
            scope=self,
            id="StringParameter",
            string_value="Initial parameter value",
        )


class SSMStage(core.Stage):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        db_stack = SSMStack(
            scope=self,
            id="SSM")


class CdkPipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        pipeline = pipelines.CdkPipeline(
            scope=self,
            id="cdk-pipeline",
            pipeline_name="SSMComandsPipeline",
            cloud_assembly_artifact=cloud_assembly_artifact,
            source_action=codepipeline_actions.GitHubSourceAction(
                action_name="GitHub",
                output=source_artifact,
                oauth_token=core.SecretValue.secrets_manager(
                    secret_id=constants.SECRET_GITHUB_ID,
                    json_field=constants.SECRET_GITHUB_JSON_FIELD,),
                trigger=codepipeline_actions.GitHubTrigger.POLL,
                owner=constants.GITHUB,
                repo=constants.GITHUB_REPO,
            ),
            synth_action=pipelines.SimpleSynthAction(
                source_artifact=source_artifact,
                cloud_assembly_artifact=cloud_assembly_artifact,
                install_command="npm install -g aws-cdk",
                build_command="pip install -r requirements.txt",
                synth_command="cdk synth",
            ),
        )
        pipeline.add_application_stage(
            app_stage=SSMStage(
                scope=self,
                id='ssmstage',
            ),
            manual_approvals=False,
        )

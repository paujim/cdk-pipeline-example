import constants
from aws_cdk import (
    core,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
)
from aws_cdk.pipelines import CdkPipeline, SimpleSynthAction


class CdkPipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        pipeline = CdkPipeline(
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
            synth_action=SimpleSynthAction.standard_npm_synth(
                source_artifact=source_artifact,
                cloud_assembly_artifact=cloud_assembly_artifact,
                # Use this if you need a build step (if you're not using ts-node
                # or if you have TypeScript Lambdas that need to be compiled).
                install_command="npm install -g aws-cdk",
                build_command="npm run build",
                synth_command="cdk synth",
            )
        )

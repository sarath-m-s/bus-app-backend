from aws_cdk import Stack
from constructs import Construct
from aws_cdk import aws_amplify as amplify
from aws_cdk import SecretValue


class AmplifyStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        amplify_app_properties: dict,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define the properties
        self.amplify_app_properties = amplify_app_properties
        self.amplify_app_name = self.amplify_app_properties["app_name"]
        self.amplify_app_repository = self.amplify_app_properties["app_repository"]
        self.amplify_app_branch = self.amplify_app_properties["app_branch"]

        # Create the Amplify app
        self.app = amplify.App(
            self,
            "MyAmplifyApp",
            source_code_provider=amplify.GitHubSourceCodeProvider(
                owner="<github_owner>",
                repository=self.amplify_app_repository,
                oauth_token=SecretValue.secrets_manager("<secrets_manager_secret>"),
            ),
        )

        # Add a branch to the Amplify app
        self.branch = self.app.add_branch(self.amplify_app_branch)

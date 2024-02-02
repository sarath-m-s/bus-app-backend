from aws_cdk import Stack, aws_iam as iam
from constructs import Construct


class Iam(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        assumed_by,
        policy_statements,
        trusted_services=None,
    ):
        super().__init__(scope, id)

        if trusted_services is None:
            trusted_services = []

        # Create a CompositePrincipal that represents all of the trusted services
        composite_principal = iam.CompositePrincipal(
            *[iam.ServicePrincipal(service) for service in trusted_services],
            iam.ServicePrincipal(assumed_by)
        )

        self.role = iam.Role(
            self,
            id,
            assumed_by=composite_principal,
        )

        for statement in policy_statements:
            self.role.add_to_policy(statement)

    def add_policy_to_role(self, policy_statement):
        self.role.add_to_policy(policy_statement)
        return self.role

    @property
    def get_role(self):
        return self.role

    @property
    def get_role_arn(self):
        return self.role.role_arn

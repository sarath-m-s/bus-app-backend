from aws_cdk import Duration, Stack, aws_logs as logs
from constructs import Construct
from aws_cdk import aws_stepfunctions as sfn


class StepFunctionsStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        state_machine_properties: dict,
        state_machine_definition: sfn.IChainable,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # Define the state machine
        self.state_machine_name = state_machine_properties["state_machine_name"]
        state_machine = sfn.StateMachine(
            self,
            "StateMachine",
            state_machine_name=self.state_machine_name,
            definition=state_machine_definition,
            timeout=Duration.minutes(5),
            logs=sfn.LogOptions(
                destination=logs.LogGroup(self, "StateMachineLogGroup"),
                include_execution_data=True,
                level=sfn.LogLevel.ALL,
            ),
        )

    @property
    def state_machine(self) -> sfn.StateMachine:
        return self.state_machine

    @property
    def state_machine_arn(self) -> str:
        return self.state_machine.state_machine_arn

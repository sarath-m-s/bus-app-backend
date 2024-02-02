from aws_cdk import Stack, aws_events as events, aws_events_targets as targets
from constructs import Construct


class EventBridgeStack(Stack):
    def __init__(self, scope: Construct, id: str, event_properties: dict, **kwargs):
        super().__init__(scope, id, **kwargs)

        """
        EventBridge properties JSON Structure:
        {
            "rule_name": "EventBridgeRuleName",
            "event_bus_name": "EventBridgeEventBusName",
            "event_pattern": "EventBridgeEventPattern",
            "target_type": "EventBridgeTargetType",
            "target": "EventBridgeTarget",
            "event_rule": "EventBridgeEventRule"
        }
        """

        self.event_properties = event_properties
        self.rule_name = self.event_properties.get("rule_name", None)
        self.event_bus_name = self.event_properties.get("event_bus_name", None)
        self.event_pattern = self.event_properties.get("event_pattern", None)
        self.target_type = self.event_properties.get("target_type", None)
        self.target = self.event_properties.get("target", None)

    # this method can be used to update the properties of the event_properties dict after it has been created
    # for example, if you want to update the event_properties dict with target_type or target
    def update_properties(self, new_properties):
        self.rule_name = new_properties.get("rule_name", self.rule_name)
        self.event_bus_name = new_properties.get("event_bus_name", self.event_bus_name)
        self.event_pattern = new_properties.get("event_pattern", self.event_pattern)
        self.target_type = new_properties.get("target_type", self.target_type)
        self.target = new_properties.get("target", self.target)

    def create_event_bus(self):
        self.event_bus = events.EventBus(
            self, "EventBus", event_bus_name=self.event_bus_name
        )
        return self.event_bus

    def create_eventbridge_rule(self):
        _event_bus = events.EventBus.from_event_bus_name(
            self, f"{self.event_bus_name}_EventBus", self.event_bus_name
        )
        self.eventbridge_rule = events.Rule(
            self,
            self.rule_name,
            rule_name=self.rule_name,
            event_bus=_event_bus,
            event_pattern=self.event_pattern,
        )

        return self.eventbridge_rule

    def add_target(self):
        if self.target_type == "lambda":
            return self.eventbridge_rule.add_target(targets.LambdaFunction(self.target))
        elif self.target_type == "sqs":
            return self.eventbridge_rule.add_target(targets.SqsQueue(self.target))
        elif self.target_type == "sns":
            return self.eventbridge_rule.add_target(targets.SnsTopic(self.target))
        return "Target type not supported"

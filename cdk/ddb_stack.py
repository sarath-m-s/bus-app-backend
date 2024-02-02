from aws_cdk import RemovalPolicy, Stack
from constructs import Construct
from aws_cdk import aws_dynamodb as dynamodb


class DynamoDBStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, ddb_properties: dict, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        """
        DynamoDB properties JSON Structure:
        {
            "name": "string",
            "partition_key": "string",
            "gsi_partition_key": "string",
            "sort_key": "string",
            "gsi_sort_key": "string"
        }
        """

        self.ddb_properties = ddb_properties
        self.name = self.ddb_properties["name"]
        self.partition_key = self.ddb_properties["partition_key"]
        self.sort_key = self.ddb_properties.get("sort_key", None)
        self.gsi_partition_key = self.ddb_properties.get("gsi_partition_key", None)
        self.gsi_sort_key = self.ddb_properties.get("gsi_sort_key", None)
        self.gsi_name = self.ddb_properties.get("gsi_name", None)

        self.ddb_table = self.create_dynamodb_table(
            self.name, self.partition_key, self.sort_key
        )

    def create_dynamodb_table(
        self, table_name: str, partition_key: str, sort_key: str = None
    ):
        partition_key_attr = dynamodb.Attribute(
            name=partition_key, type=dynamodb.AttributeType.STRING
        )
        sort_key_attr = (
            dynamodb.Attribute(name=sort_key, type=dynamodb.AttributeType.STRING)
            if sort_key
            else None
        )

        table = dynamodb.Table(
            self,
            table_name,
            table_name=table_name,
            partition_key=partition_key_attr,
            sort_key=sort_key_attr,
            removal_policy=RemovalPolicy.DESTROY,
        )

        if self.gsi_partition_key and self.gsi_sort_key:
            table.add_global_secondary_index(
                index_name=self.gsi_name,
                partition_key=dynamodb.Attribute(
                    name=self.gsi_partition_key, type=dynamodb.AttributeType.STRING
                ),
                sort_key=dynamodb.Attribute(
                    name=self.gsi_sort_key, type=dynamodb.AttributeType.STRING
                ),
            )
        elif self.gsi_partition_key:
            table.add_global_secondary_index(
                index_name=self.gsi_name,
                partition_key=dynamodb.Attribute(
                    name=self.gsi_partition_key, type=dynamodb.AttributeType.STRING
                ),
            )

        return table

    @property
    def get_ddb_table(self):
        return self.ddb_table

    @property
    def get_ddb_table_arn(self):
        return self.ddb_table.table_arn

    @property
    def get_ddb_table_name(self):
        return self.ddb_table.table_name

    @property
    def get_ddb_table_partition_key(self):
        return self.ddb_table.partition_key

    @property
    def get_ddb_table_sort_key(self):
        return self.ddb_table.sort_key

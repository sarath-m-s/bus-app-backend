from aws_cdk import Stack, aws_s3 as s3
from constructs import Construct


class S3Stack(Stack):
    def __init__(self, scope: Construct, id: str, s3_properties: dict, **kwargs):
        super().__init__(scope, id, **kwargs)

        """
        S3 properties JSON Structure:
        {
            "bucket_name": "S3BucketName",
            "versioned": "S3Versioned",
            "encryption": "S3Encryption",
            "block_public_access": "S3BlockPublicAccess",
        }
        """

        self.s3_properties = s3_properties
        self.bucket_name = self.s3_properties["bucket_name"]
        self.versioned = self.s3_properties.get("versioned", False)
        self.encryption = self.s3_properties.get("encryption", True)
        self.block_public_access = self.s3_properties.get("block_public_access", True)

        self.s3_bucket = self.create_s3_bucket(
            self.bucket_name,
            self.versioned,
            self.encryption,
            self.block_public_access,
        )

    def create_s3_bucket(
        self,
        bucket_name: str,
        versioned: bool,
        encryption: bool,
        block_public_access: bool,
    ):
        return s3.Bucket(
            self,
            bucket_name,
            bucket_name=bucket_name,
            versioned=versioned,
            encryption=s3.BucketEncryption.S3_MANAGED if encryption else None,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
            if block_public_access
            else s3.BlockPublicAccess.BLOCK_ACLS,
            cors=[
                s3.CorsRule(
                    allowed_methods=[
                        s3.HttpMethods.GET,
                        s3.HttpMethods.PUT,
                        s3.HttpMethods.POST,
                        s3.HttpMethods.DELETE,
                        s3.HttpMethods.HEAD,
                    ],
                    allowed_origins=["*"],
                    allowed_headers=["*"],
                )
            ],
        )

    @property
    def get_s3_bucket(self):
        return self.s3_bucket

    @property
    def get_s3_bucket_name(self):
        return self.s3_bucket.bucket_name

    @property
    def get_s3_bucket_arn(self):
        return self.s3_bucket.bucket_arn

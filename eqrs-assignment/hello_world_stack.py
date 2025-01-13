from aws_cdk import (
    core,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_iam as iam,
    aws_ecr as ecr,
)

class HelloWorldStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # VPC for networking
        vpc = ec2.Vpc(self, "HelloWorldVpc", max_azs=3)

        # ECS Cluster
        cluster = ecs.Cluster(self, "HelloWorldCluster", vpc=vpc)

        # RDS Database
        db = rds.DatabaseInstance(self, "HelloWorldDb",
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_12_4),
            instance_type=ec2.InstanceType("t3.micro"),
            vpc=vpc,
            removal_policy=core.RemovalPolicy.DESTROY,
            deletion_protection=False,
            database_name="hello_world",
            publicly_accessible=False,
            credentials=rds.Credentials.from_generated_secret("dbadmin"),
        )

        # ECS Task definition
        task_definition = ecs.FargateTaskDefinition(self, "HelloWorldTask")
        container = task_definition.add_container("HelloWorldContainer",
            image=ecs.ContainerImage.from_registry("myusername/hello-world-app"),
            memory_limit_mib=512
        )
        container.add_port_mappings(ecs.PortMapping(container_port=5000))

        # ECS Service
        ecs_service = ecs.FargateService(self, "HelloWorldService",
            cluster=cluster,
            task_definition=task_definition,
            desired_count=2
        )

app = core.App()
HelloWorldStack(app, "HelloWorldStack")
app.synth()

"""
The script using Troposphere to create CloudFormation templates
for several environment types
"""

from troposphere import \
    Ref, Output, Tags
from troposphere.ec2 import \
    InternetGateway, VPC, VPCGatewayAttachment,\
    NetworkAcl, NetworkAclEntry, PortRange

ENV_LIST = ['Development', 'Experimental', 'Production']

"""
Create CloudFormation templates dynamically
"""


def create_template(template, env):
    """Create the CloudFormation template and write it to the json file"""

    template.set_description("Service VPC")

    template.set_metadata(
        {
            "DependsOn": [],
            "Environment": env,
            "StackName": "".join((env, "-VPC"))
        })

    internetGateway = template.add_resource(
        InternetGateway(
            "InternetGateway",
            Tags=Tags(
                Environment=env,
                Name="-".join((env, "InternetGateway")))
        ))

    vpc = template.add_resource(
        VPC(
            "VPC",
            CidrBlock="10.0.0.0/16",
            EnableDnsHostnames="true",
            EnableDnsSupport="true",
            InstanceTenancy="default",
            Tags=Tags(
                Environment=env,
                Name="-".join((env, "ServiceVPC")))
        ))

    vpcgatewayattachment = template.add_resource(
        VPCGatewayAttachment(
            "VpcGatewayAttachment",
            InternetGatewayId=Ref(internetGateway),
            VpcId=Ref(vpc),
        ))

    vpcnetworkacl = template.add_resource(
        NetworkAcl(
            "VpcNetworkAcl",
            VpcId=Ref(vpc),
            Tags=Tags(
                Environment=env,
                Name="-".join((env, "NetworkAcl")))
        ))

    vpcnetworkaclinboundrule = template.add_resource(
        NetworkAclEntry(
            "VpcNetworkAclInboundRule",
            CidrBlock="0.0.0.0/0",
            Egress="false",
            NetworkAclId=Ref(vpcnetworkacl),
            PortRange=PortRange(To="443", From="443"),
            Protocol="6",
            RuleAction="allow",
            RuleNumber=100
        ))

    vpcnetworkacloutboundrule = template.add_resource(
        NetworkAclEntry(
            "VpcNetworkAclOutboundRule",
            CidrBlock="0.0.0.0/0",
            Egress="true",
            NetworkAclId=Ref(vpcnetworkacl),
            Protocol="6",
            RuleAction="allow",
            RuleNumber=200
        ))

    template.add_output(
        Output(
            "InternetGateway",
            Value=Ref(internetGateway),
        ))

    template.add_output(
        Output(
            "VPCID",
            Value=Ref(vpc),
        ))

    return template

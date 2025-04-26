import warnings

from io import StringIO
import sys
import textwrap
import os
from typing import Optional

# External Dependencies:
import boto3
from botocore.config import Config

warnings.filterwarnings('ignore')

def print_ww(*args, width: int = 100, **kwargs):
    """Like print(), but wraps output to `width` characters (default 100)"""
    buffer = StringIO()
    try:
        _stdout = sys.stdout
        sys.stdout = buffer
        print(*args, **kwargs)
        output = buffer.getvalue()
    finally:
        sys.stdout = _stdout
    for line in output.splitlines():
        print("\n".join(textwrap.wrap(line, width=width)))
        

def get_boto_client_tmp_cred(
    retry_config = None,
    target_region: Optional[str] = None,
    runtime: Optional[bool] = True,
    service_name: Optional[str] = None,
):

    if not service_name:
        if runtime:
            service_name='bedrock-runtime'
        else:
            service_name='bedrock'

    bedrock_client = boto3.client(
        service_name=service_name,
        config=retry_config,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN',""),
    )
    print("boto3 Bedrock client successfully created!")
    print(bedrock_client._endpoint)
    return bedrock_client    

def get_boto_client(
    assumed_role: Optional[str] = None,
    region: Optional[str] = None,
    runtime: Optional[bool] = True,
    service_name: Optional[str] = None,
):
    """Create a boto3 client for Amazon Bedrock, with optional configuration overrides

    Parameters
    ----------
    assumed_role :
        Optional ARN of an AWS IAM role to assume for calling the Bedrock service. If not
        specified, the current active credentials will be used.
    region :
        Optional name of the AWS Region in which the service should be called (e.g. "us-east-1").
        If not specified, AWS_REGION or AWS_DEFAULT_REGION environment variable will be used.
    runtime :
        Optional choice of getting different client to perform operations with the Amazon Bedrock service.
    """
    if region is None:
        target_region = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION"))
    else:
        target_region = region

    print(f"Create new client\n  Using region: {target_region}")
    session_kwargs = {"region_name": target_region}
    client_kwargs = {**session_kwargs}

    # profile_name = os.environ.get("AWS_PROFILE", None)
    profile_name = "default"
    retry_config = Config(
        region_name=target_region,
        signature_version = 'v4',
        retries={
            "max_attempts": 50,
            "mode": "standard",
        },
    )
    if profile_name:
        print(f"  Using profile: {profile_name}")
        session_kwargs["profile_name"] = profile_name
    else: # use temp credentials -- add to the client kwargs
        print(f"  Using temp credentials")

        return get_boto_client_tmp_cred(retry_config=retry_config,target_region=target_region, runtime=runtime, service_name=service_name)

    session = boto3.Session(**session_kwargs)

    if assumed_role:
        print(f"  Using role: {assumed_role}", end='')
        sts = session.client("sts")
        response = sts.assume_role(
            RoleArn=str(assumed_role),
            RoleSessionName="langchain-llm-1"
        )
        print(" ... successful!")
        client_kwargs["aws_access_key_id"] = response["Credentials"]["AccessKeyId"]
        client_kwargs["aws_secret_access_key"] = response["Credentials"]["SecretAccessKey"]
        client_kwargs["aws_session_token"] = response["Credentials"]["SessionToken"]

    if not service_name:
        if runtime:
            service_name='bedrock-runtime'
        else:
            service_name='bedrock'

    bedrock_client = session.client(
        service_name=service_name,
        config=retry_config,
        **client_kwargs
    )

    print("boto3 Bedrock client successfully created!")
    print(bedrock_client._endpoint)
    return bedrock_client
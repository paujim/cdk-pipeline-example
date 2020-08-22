#!/usr/bin/env python3

from aws_cdk import core

from cdk_pipeline_example.cdk_pipeline_example_stack import CdkPipelineStack


app = core.App()
CdkPipelineStack(app, "cdk-pipeline-example")

app.synth()

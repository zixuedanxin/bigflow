from bigflow import Workflow

from ..deployment_config import deployment_config
from .processing import SimpleJob

simple_workflow = Workflow(workflow_id="test_workflow", definition=[SimpleJob(deployment_config.resolve(), 'test_workflow')])


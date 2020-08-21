from bigflow import Workflow
# from test.scorer_project_dev.deployment_config import deployment_config
from .processing import SimpleJob

simple_workflow = Workflow(workflow_id="test_workflow", definition=[SimpleJob('test_workflow')])


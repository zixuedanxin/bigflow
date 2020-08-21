from bigflow import Workflow
from .processing import SimpleJob

simple_workflow = Workflow(workflow_id="test_workflow", definition=[SimpleJob('test_workflow')])


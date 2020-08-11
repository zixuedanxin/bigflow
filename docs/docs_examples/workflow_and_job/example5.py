from bigflow.workflow import Workflow
from bigflow.workflow import Definition


class Job(object):
    def __init__(self, id):
        self.id = id

    def run(self, runtime):
        print(runtime)


job1, job2, job3, job4 = Job('1'), Job('2'), Job('3'), Job('4')

graph_workflow = Workflow(workflow_id='graph_workflow', definition=Definition({
    job1: (job2, job3),
    job2: (job4,),
    job3: (job4,)
}))
graph_workflow.run()
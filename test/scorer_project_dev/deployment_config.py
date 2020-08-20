
from bigflow.configuration import Config

deployment_config = Config(name='dev',
                           properties={
                               'docker_repository': '',
                               'gcp_project_id': 'project_id',
                               'project_name': 'scorer_project_name',
                               'dags_bucket': 'bucket'
                           })

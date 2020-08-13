from bigflow import Config

deployment_config = Config(
    name='dev',
    properties={
        'docker_repository': 'eu.gcr.io/docker_repository_project/my-project',
        'dags_bucket': 'test_bucket',
        'gcp_project_id': 'test_gcp_project_xyz'
    })

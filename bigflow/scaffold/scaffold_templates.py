readme_template = ''''''
docker_template = '''
FROM python:3.7
COPY ./dist /dist
RUN apt-get -y update && apt-get install -y libzbar-dev libc-dev musl-dev
RUN for i in /dist/*.whl; do pip install $i; done
'''

basic_deployment_config_template = '''
from bigflow.configuration import Config

deployment_config = Config(name='dev',
                           properties={{
                               'docker_repository': 'test_repository',
                               'gcp_project_id': '{project_id}',
                               'project_name': '{project_name}',
                               'dags_bucket': '{dags_bucket}'
                           }})
'''

advanced_deployment_config_template = '''.add_configuration(name='{env}',
                           properties={{
                               'gcp_project_id': '{project_id}',
                               'dags_bucket': '{dags_bucket}'
                           }})
'''
requirements_template = ''''''

project_setup_template = '''
from setuptools import setup
from bigflow.build import project_setup, auto_configuration

PROJECT_NAME = 'workflows'

if __name__ == '__main__':
    setup(**project_setup(**auto_configuration(PROJECT_NAME)))
'''

beam_pipeline_template = '''
import uuid
from pathlib import Path

import apache_beam as beam

from apache_beam.options.pipeline_options import SetupOptions, StandardOptions, WorkerOptions, GoogleCloudOptions, PipelineOptions

from bigflow.resources import create_file_if_not_exists, find_file, create_setup_body, resolve, get_resource_absolute_path
from .config import workflow_config

def dataflow_pipeline():
    options = PipelineOptions()

    google_cloud_options = options.view_as(GoogleCloudOptions)
    google_cloud_options.project = workflow_config['project_id']
    google_cloud_options.job_name = f"{workflow_config['project_id']}-{uuid.uuid4()}"
    google_cloud_options.staging_location = f"gs://{workflow_config['stagging_location']}"
    google_cloud_options.temp_location = f"gs://{workflow_config['temp_location']}"
    google_cloud_options.region = workflow_config['region']

    options.view_as(WorkerOptions).machine_type = workflow_config['machine_type']
    options.view_as(WorkerOptions).max_num_workers = 1
    options.view_as(WorkerOptions).autoscaling_algorithm = 'THROUGHPUT_BASED'
    options.view_as(StandardOptions).runner = 'DataflowRunner'
    options.view_as(StandardOptions).streaming = True

    options.view_as(SetupOptions).setup_file = resolve(
        create_file_if_not_exists(find_file(workflow_config['project_name'], Path(__file__)).parent / 'setup.py', create_setup_body(workflow_config['project_name'])))
    options.view_as(SetupOptions).requirements_file = resolve(get_resource_absolute_path('requirements.txt', Path(__file__)))
    return beam.Pipeline(options=options)

'''
beam_processing_template = '''

import re
import apache_beam as beam
from apache_beam.io import ReadFromText
from past.builtins import unicode

from .pipeline import dataflow_pipeline
from .config import workflow_config


class SimpleJob(object):
    def __init__(self, config, id):
        self.config = config
        self.id = id
        self.retry_count = 20
        self.retry_pause_sec = 100

    def run(self):
        with dataflow_pipeline(workflow_config['gcp_project_id'], workflow_config['project_name'], workflow_config['dags_bucket']) as p:
            lines = p | ReadFromText('gs://dataflow-samples/shakespeare/kinglear.txt',)

            # Count the occurrences of each word.
            counts = (
                    lines
                    | 'Split' >> (
                        beam.FlatMap(lambda x: re.findall(r'[A-Za-z\']+', x)).
                            with_output_types(unicode))
                    | 'PairWithOne' >> beam.Map(lambda x: (x, 1))
                    | 'GroupAndSum' >> beam.CombinePerKey(sum))

            # Format the counts into a PCollection of strings.
            def format_result(word_count):
                (word, count) = word_count
                print(word,count)
                return '%s: %s' % (word, count)

            counts | 'Format' >> beam.Map(format_result)
        p.run().wait_until_finish()


'''
beam_workflow_template = '''
from bigflow import Workflow
from .processing import SimpleJob

simple_workflow = Workflow(workflow_id="test_workflow", definition=[SimpleJob('test_workflow')])
'''
beam_config_template = '''
from bigflow.configuration import Config

workflow_config = Config(name='dev',
                           properties={
                               'gcp_project_id': '{project_id}',
                               'project_name': '{project_name}',
                               'stagging_location': 'stagging-location',
                               'temp_location': 'temp-location',
                               'region': 'europe-west1',
                               'machine_type': 'n1-standard-1'
                           }).resolve()
'''

bq_config_template = ''''''
bq_processing_template = ''''''
bq_workflow_templatee = ''''''
bq_tables_template = ''''''
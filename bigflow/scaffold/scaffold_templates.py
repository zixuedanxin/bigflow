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
import os
import sys
from pathlib import Path
from setuptools import setup


def add_bigflow_to_path():
    # For Travis
    bf_path_index = str(Path(__file__).absolute()).split(os.sep).index('bigflow')
    bf_path_parts = str(Path(__file__).absolute()).split(os.sep)[:bf_path_index + 1]
    bf_package = os.path.join(os.sep, *bf_path_parts)
    print(f'Adding to path: ' + bf_package)
    sys.path.insert(0, bf_package)
    
PROJECT_DIR = Path(__file__).parent
PROJECT_NAME = '{project_name}'
BUILD_PATH = Path(__file__).parent / 'build'
TEST_PATH = Path(__file__).parent / 'test'
DAGS_DIR_PATH = Path(__file__).parent / '.dags'
DIST_DIR_PATH = Path(__file__).parent / 'dist'
IMAGE_DIR_PATH = Path(__file__).parent / 'image'
EGGS_DIR_PATH = Path(__file__).parent / PROJECT_NAME + '.egg-info'
ROOT_PACKAGE = Path(__file__).parent / '{project_name}'
DOCKER_REPOSITORY = 'test_docker_repository'
DEPLOYMENT_CONFIG_PATH = Path(__file__).parent / 'deployment_config.py'
REQUIREMENTS_PATH = Path(__file__).parent / 'resources' / 'requirements.txt'
RESOURCES_PATH = Path(__file__).parent / 'resources'

if __name__ == '__main__':
    add_bigflow_to_path()
    from bigflow import build

    setup(**build.project_setup(
        root_package=ROOT_PACKAGE,
        project_dir=PROJECT_DIR,
        project_name=PROJECT_NAME,
        build_dir=BUILD_PATH,
        test_package=TEST_PATH,
        dags_dir=DAGS_DIR_PATH,
        dist_dir=DIST_DIR_PATH,
        image_dir=IMAGE_DIR_PATH,
        eggs_dir=EGGS_DIR_PATH,
        deployment_config_file=DEPLOYMENT_CONFIG_PATH,
        docker_repository=DOCKER_REPOSITORY,
        version='0.1.0',
        resources_dir=RESOURCES_PATH,
        project_requirements_file=REQUIREMENTS_PATH))
'''

beam_pipeline_template = '''
import uuid
from pathlib import Path

import apache_beam as beam

from apache_beam.options.pipeline_options import SetupOptions, StandardOptions, WorkerOptions, GoogleCloudOptions, \
    PipelineOptions

from bigflow.resources import create_file_if_not_exists, find_file, create_setup_body, resolve, \
    get_resource_absolute_path


def dataflow_pipeline(project_id, project_name, bucket):
    options = PipelineOptions()

    google_cloud_options = options.view_as(GoogleCloudOptions)
    google_cloud_options.project = project_id
    google_cloud_options.job_name = f'{project_name}-{uuid.uuid4()}'
    google_cloud_options.staging_location = f'gs://{bucket}/beam_runner/staging'
    google_cloud_options.temp_location = f'gs://{bucket}/beam_runner/temp'
    google_cloud_options.region = 'europe-west1'

    options.view_as(WorkerOptions).machine_type = 'n1-standard-1'   
    options.view_as(WorkerOptions).max_num_workers = 1
    options.view_as(WorkerOptions).autoscaling_algorithm = 'THROUGHPUT_BASED'
    options.view_as(StandardOptions).runner = 'DataflowRunner'
    options.view_as(StandardOptions).streaming = True

    options.view_as(SetupOptions).setup_file = resolve(
        create_file_if_not_exists(find_file(project_name, Path(__file__)).parent / 'setup.py', create_setup_body(project_name)))
    options.view_as(SetupOptions).requirements_file = resolve(get_resource_absolute_path('requirements_mcb.txt', Path(__file__)))
    return beam.Pipeline(options=options)
'''
beam_processing_template = '''
import re
import apache_beam as beam
from apache_beam.io import ReadFromText
from past.builtins import unicode
from .pipeline import dataflow_pipeline
from ..deployment_config import deployment_config
def run(config):
    with dataflow_pipeline(config['project_id'], config['project_name'], config['bucket']) as p:
        lines = p | ReadFromText('gs://dataflow-samples/shakespeare/kinglear.txt',)

        # Count the occurrences of each word.
        counts = (
                lines
                | 'Split' >> (
                    beam.FlatMap(lambda x: re.findall(r'[A-Za-z\\']+', x)).
                        with_output_types(unicode))
                | 'PairWithOne' >> beam.Map(lambda x: (x, 1))
                | 'GroupAndSum' >> beam.CombinePerKey(sum))

        # Format the counts into a PCollection of strings.
        def format_result(word_count):
            (word, count) = word_count
            print(word,count)
            return '%s: %s' % (word, count)

        counts | 'Format' >> beam.Map(format_result)
    
if __name__ == '__main__':
    run(deployment_config.resolve())    

'''
beam_workflow_template = ''''''

bq_config_template = ''''''
bq_processing_template = ''''''
bq_workflow_templatee = ''''''
bq_tables_template = ''''''
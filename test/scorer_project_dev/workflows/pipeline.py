
import uuid
from pathlib import Path

import apache_beam as beam

from apache_beam.options.pipeline_options import SetupOptions, StandardOptions, WorkerOptions, GoogleCloudOptions,     PipelineOptions

from bigflow.resources import create_file_if_not_exists, find_file, create_setup_body, resolve,     get_resource_absolute_path


def dataflow_pipeline(project_id, project_name, bucket):
    options = PipelineOptions()

    google_cloud_options = options.view_as(GoogleCloudOptions)
    google_cloud_options.project = project_id
    google_cloud_options.job_name = f'iwo-test{uuid.uuid4()}'
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
    options.view_as(SetupOptions).requirements_file = resolve(get_resource_absolute_path('requirements.txt', Path(__file__)))
    return beam.Pipeline(options=options)
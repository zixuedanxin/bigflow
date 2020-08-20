import os
from pathlib import Path

from bigflow.scaffold.scaffold_templates import beam_workflow_template, beam_processing_template, \
    beam_pipeline_template, project_setup_template, basic_deployment_config_template, \
    advanced_deployment_config_template, docker_template


def start_project(config):
    create_dirs(config)


def create_dirs(config):
    beam_templates = {'workflow.py': beam_workflow_template, 'processing.py': beam_processing_template, 'pipeline.py': beam_pipeline_template}
    bq_templates = {}
    deployment_config_template = basic_deployment_config_template.format(project_id=config['projects_id'][0], dags_bucket=config['composers_bucket'][0], project_name=config['project_name'])
    if not config['is_basic']:
        for i in range(1, len(config['projects_id'])):
            deployment_config_template = deployment_config_template.strip()
            deployment_config_template += advanced_deployment_config_template.format(env=config['envs'][i], project_id=config['projects_id'][i], dags_bucket=config['composers_bucket'][i])
    main_templates = {'project_setup.py': project_setup_template.format(project_name=config['project_name']), 'deployment_config.py': deployment_config_template, 'dockerfile': docker_template}
    project_path = Path(config['project_name']).resolve()
    beam_workflow_path = Path(config['project_name'] + '/beam_workflow')
    bq_workflow_path = Path(config['project_name'] + '/bq_workflow')
    resources_path = Path(config['project_name'] + '/resources')
    test_path = Path(config['project_name'] + '/test')

    os.mkdir(project_path)
    os.mkdir(beam_workflow_path)
    os.mkdir(bq_workflow_path)
    os.mkdir(resources_path)
    os.mkdir(test_path)


    create_module_files(main_templates, project_path.resolve())
    create_module_files(beam_templates, beam_workflow_path.resolve())


def create_module_files(templates, path):
    for filename, template in templates.items():
        with open(os.path.join(path, filename), 'w+') as f:
            f.write(template)

import os
from pathlib import Path

from bigflow.scaffold.scaffold_templates import beam_workflow_template, beam_processing_template, beam_tables_template, \
    beam_pipeline_template, beam_config_template, project_setup_template


def start_project(config):
    create_dirs(config)


def create_dirs(config):
    beam_templates = {'workflow': beam_workflow_template, 'processing': beam_processing_template, 'tables': beam_tables_template, 'pipeline': beam_pipeline_template, 'config': beam_config_template}
    bq_templates = {}
    main_templates = {'project_setup': project_setup_template}
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


def create_module_files(templates, path):
    for filename, template in templates.items():
        filename += '.py'
        with open(os.path.join(path, filename), 'w+') as f:
            f.write(template)

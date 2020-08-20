from setuptools import setup
from bigflow.build import project_setup, auto_configuration

PROJECT_NAME = 'workflows'

if __name__ == '__main__':
    setup(**project_setup(**auto_configuration(PROJECT_NAME)))
dataset_template = '''
from biggerquery import DatasetConfig

INTERNAL_TABLES = []

EXTERNAL_TABLES = {
    'object_ctr': 'sc-11309-content-scorer-prod.content_scorer_v2.score_v1',
    'profiles_per_user_daily': 'sc-11309-content-scorer-prod.scorer_analytics_prod.segments_per_user_daily'
}

EXTRAS = {
    'page-routes-v2': 'page-routes-v2-{env}',
}
DEV_EXTRAS = EXTRAS.copy()
DEV_EXTRAS['is_local'] = True

PROD_EXTRAS = EXTRAS.copy()
PROD_EXTRAS['is_local'] = False

DEV_PROJECT_ID = ''
PROD_PROJECT_ID = ''

dataset_config = DatasetConfig(env='dev',
                               project_id=DEV_PROJECT_ID,
                               dataset_name='scorer_analytics_dev',
                               internal_tables=INTERNAL_TABLES,
                               external_tables=EXTERNAL_TABLES,
                               properties=DEV_EXTRAS
                               )\
            .add_configuration('prod',
                               project_id=PROD_PROJECT_ID,
                               dataset_name='scorer_analytics_prod',
                               properties=PROD_EXTRAS)


'''
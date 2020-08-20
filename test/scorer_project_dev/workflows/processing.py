
import re
import apache_beam as beam
from apache_beam.io import ReadFromText
from past.builtins import unicode
from ..workflows.pipeline import dataflow_pipeline

class SimpleJob(object):
    def __init__(self, config, id):
        self.config = config
        self.id = id
        self.retry_count = 20
        self.retry_pause_sec = 100

    def run(self, runtime):
        with dataflow_pipeline(self.config['gcp_project_id'], self.config['project_name'], self.config['dags_bucket']) as p:
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


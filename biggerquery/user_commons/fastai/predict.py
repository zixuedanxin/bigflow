import apache_beam as beam
from apache_beam.pvalue import AsSingleton


def side_input_factory(p, item, label_name):
    return AsSingleton(p
                       | label_name + ', creating collection' >> beam.Create([item])
                       | label_name + ', combining globally' >> beam.CombineGlobally(beam.combiners.ToListCombineFn()))


class Predictor(beam.DoFn):

    def process(self, element, model_gcs_path_side_input):
        if not hasattr(self, 'learn'):
            from google.cloud import storage
            from fastai.tabular import load_learner
            import io

            model_file = io.BytesIO()
            client = storage.Client()
            client.download_blob_to_file(model_gcs_path_side_input[0], model_file)
            model_file.seek(0)

            self.learn = load_learner('/some/path', file=model_file)

        element['prediction'] = self.learn.predict(element)[1].item()
        yield element


def run(p, input_collection, output, model_gcs_path):
    model_gcs_path_side_input = side_input_factory(p, model_gcs_path, 'creating model gcs path side input')

    p | 'loading variables' >> input_collection \
    | 'predicting' >> beam.ParDo(
        Predictor(),
        model_gcs_path_side_input=model_gcs_path_side_input) \
    | 'saving predictions' >> output

    p.run().wait_until_finish()


if __name__ == '__main__':
    run(**globals()['run_kwargs'])
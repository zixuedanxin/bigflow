import apache_beam as beam


class Predictor(beam.DoFn):

    def __init__(self, model_gcs_path):
        super().__init__()
        self.model_gcs_path = model_gcs_path
        self.learn = None

    def setup(self):
        from google.cloud import storage
        from fastai.tabular import load_learner
        import io

        model_file = io.BytesIO()
        client = storage.Client()
        client.download_blob_to_file(self.model_gcs_path, model_file)
        model_file.seek(0)

        self.learn = load_learner('/some/path', file=model_file)

    def process(self, element):
        element['prediction'] = self.learn.predict(element)[1].item()
        yield element


def run(p, input_collection, output, model_gcs_path):

    p | 'loading variables' >> input_collection \
      | 'predicting' >> beam.ParDo(Predictor(model_gcs_path)) \
      | 'saving predictions' >> output

    p.run().wait_until_finish()


if __name__ == '__main__':
    run(**globals()['run_kwargs'])
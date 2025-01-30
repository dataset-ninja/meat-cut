Dataset **Meat Cut** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzM0MTBfTWVhdCBDdXQvbWVhdC1jdXQtRGF0YXNldE5pbmphLnRhciIsICJzaWciOiAiWkd5UjMzTGVmcUJwMjRFOUloblhuMVBVVzAxU0pnUFdTemc3azVWL3RNVT0ifQ==)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Meat Cut', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://zenodo.org/records/4704391/files/Image%20Dataset.zip?download=1).
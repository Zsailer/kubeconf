# Kubeconf

**A lightweight Python module for creating, manipulating, and editing kubeconfig files**

*Why not use or wrap `kubectl config`?*

`kubectl config` is great, but it's pretty restrictive in what you can change. I wanted more control over my kubenetes config and integrate into Python pipelines. *kubeconf* gives me that control. It does not use *kubectl* at all.

## Getting starting

Install this package using pip:
```
pip install kubeconf
```

**Basic Usage**

```python
from kubeconf import KubeConf

k = KubeConf(path='path/to/config')

# Open the file
k.open()

# Add a cluster
k.add_cluster(
    name='mycluster',
    server='...',
    certificate_authority_data='...',
)

# Add a user for that cluster
k.add_user(
    user='me'
)

# Add a context to map the user to the cluster
k.add_context(
    name='mycontext',
    cluster_name='mycluster',

)
```

## Developing

Download and install this repo from source, and move into the base directory.
```
git clone https://github.com/Zsailer/kubeconf
cd kubeconf
```
If you use [pipenv](https://pipenv.readthedocs.io/en/latest/), you can install a developement version:
```
pipenv install --dev
``` 

Otherwise you can install a development version using pip
```
pip install -e .
```

## Licensing

The code in this project is licensed under MIT license.

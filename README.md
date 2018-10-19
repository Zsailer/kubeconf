# kubeconf

**Lightweight Python module for creating, manipulating, and editing kubeconfig files**

*Why not use or wrap `kubectl config`?*
`kubectl config` is great and writing a Python wrapper is a fine solution. However, `kubectl config` is quite limited in functionality. I wanted more control over my kubernetes config. *kubeconfig* gives me that control. It doesn't use *kubectl* at all. Rather, it reads, edits, and writes config files entirely on its own. 

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
    user_name='me'
)

# Commit change to the file.
k.close()
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

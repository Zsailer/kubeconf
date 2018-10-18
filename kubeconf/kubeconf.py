import os
import yaml
import pathlib

from traitlets.config import Configurable
from traitlets_paths import Path
from traitlets import default

def get_kube_path():
    """Get the current config path. If the KUBECONFIG environment 
    parameter is set, use it. If multiple paths are listed in 
    KUBECONFIG, use the first path.
    """
    try:
        path = pathlib.Path(os.environ["KUBECONFIG"].split(':')[0])
    except KeyError:
        path = pathlib.Path.home().joinpath('.kube', 'config')
    return path


def sanitize_path(path):
    """Sanitize a path. Returns a pathlib.PurePath object. 
    If a path string is given, a PurePath object will be
    returned. All relative paths will be converted to 
    absolute paths.
    """
    pure_path = pathlib.Path(path).resolve()
    return pure_path


class KubeConfError(Exception): 
    """"""

class KubeConfNotOpenError(Exception):
    """"""

class KubeConf(Configurable):
    """Base object that interacts with kubeconfig file.
    """
    path = Path(help="Path to kubeconfig.")

    @default('path')
    def _default_path(self):
        return get_kube_path()

    @property
    def data(self):
        try:
            return self._data
        except AttributeError:
            raise KubeConfNotOpenError("Try calling the `.open` method first.")

    @data.setter
    def data(self, data):
        self._data = data

    def open(self, create_if_not_found=True):
        """Open a kube config file. If the file does not
        exist, it creates a new file.
        """
        try:
            self.data = self._read()
        # If the file does
        except FileNotFoundError as e: 
            if create_if_not_found is True:
                self.data = {}
            else: 
                raise e

        # Enforce the following keys exists in data.
        if 'clusters' not in self.data:
            self.data['clusters'] = []
        if 'contexts' not in self.data:
            self.data['clusters'] = []
        if 'users' not in self.data:
            self.data['users'] = []
        if 'apiVersion' not in self.data:
            self.data['apiVersion'] = 'v1'
        if 'kind' not in self.data:
            self.data['kind'] = 'Config'
        if 'preferences' not in self.data:
            self.data['preferences'] = {}
        if 'current-context' not in self.data:
            self.data['current-context'] = ''

        return self

    def close(self):
        """Commit the changes to the file and close it."""
        self._write(self.data)
        delattr(self, '_data')
        return self

    def _read(self):
        """Read the kube config file. 
        """
        stream = self.path.read_text()
        data = yaml.load(stream)
        return data

    def _write(self, data):
        """Write data to config file."""
        stream = yaml.dump(data)
        self.path.write_text(stream)

    # --------------- Clusters ------------------

    def cluster_exists(self, name):
        """Check if a given cluster exists."""
        clusters = self.data['clusters']
        for cluster in clusters:
            if cluster['name'] == name:
                return True
        return False

    def get_cluster(self, name):
        """Get cluster from kubeconfig."""
        clusters = self.data['clusters']
        for cluster in clusters:
            if cluster['name'] == name:
                return cluster
        raise KubeConfError("Cluster name not found.")

    def get_clusters(self):
        """Get all clusters in config."""
        return self.data['clusters']   

    def add_cluster(
        self, 
        name, 
        server=None,
        certificate_authority_data=None,
        **attrs):
        """Add a cluster to config."""
        if self.cluster_exists(name):
            raise KubeConfError("Cluster with the given name already exists.")

        clusters = self.get_clusters()
        
        # Add parameters.
        new_cluster = {'name': name, 'cluster':{}}
        attrs_ = new_cluster['cluster']
        if server is not None:
            attrs_['server'] = server
        if certificate_authority_data is not None:
            attrs_['certificate-authority-data'] = certificate_authority_data

        attrs_.update(attrs)
        clusters.append(new_cluster)


    def add_to_cluster(self, name, **attrs):
        """Add attributes to a cluster.
        """
        cluster = self.get_cluster(name=name)
        attrs_ = cluster['cluster']
        attrs_.update(**attrs)

    def remove_from_cluster(self, name, *args):
        """Remove attributes from a cluster.
        """
        cluster = self.get_cluster(name=name)
        attrs_ = cluster['cluster']
        for a in args:
            del attrs_[a]

    def remove_cluster(self, name):
        """Remove a cluster from kubeconfig.
        """
        cluster = self.get_cluster(name)
        clusters = self.get_clusters()
        clusters.remove(cluster)

    # --------------- Users ------------------

    def user_exists(self, name):
        """Check if a given user exists."""
        users = self.data['users']
        for user in users:
            if user['name'] == name:
                return True
        return False

    def get_user(self, name):
        """Get user from kubeconfig."""
        users = self.data['users']
        for user in users:
            if user['name'] == name:
                return user
        raise KubeConfError("user name not found.")

    def get_users(self):
        """Get all users in config."""
        return self.data['users']   

    def add_user(
        self,
        name, 
        **attrs
        ):
        """Add a user to config."""
        if self.user_exists(name):
            raise KubeConfError("user with the given name already exists.")

        users = self.get_users()
        
        # Add parameters.
        new_user = {'name': name, 'user':{}}
        attrs_ = new_user['user']
        attrs_.update(attrs)
        users.append(new_user)

    def add_to_user(self, name, **attrs):
        """Add attributes to a user.
        """
        user = self.get_user(name=name)
        attrs_ = user['user']
        attrs_.update(**attrs)

    def remove_from_user(self, name, *args):
        """Remove attributes from a user.
        """
        user = self.get_user(name=name)
        attrs_ = user['user']
        for a in args:
            del attrs_[a]

    def remove_user(self, name):
        """Remove a user from kubeconfig.
        """
        user = self.get_user(name)
        users = self.get_users()
        users.remove(user)

    def add_exec_to_user(
        self, 
        name,
        env,
        command,
        args,
        **attrs
        ):
        """Add an exec option to your user."""
        # Add exec option.
        exec_options = {
            'command': command,
            'env': env
            'args': args,
        }
        exec_options.update(attrs)
        # Add exec to user.
        self.add_to_user(name=name, exec=exec_options)

    # --------------- Contexts ------------------

    def context_exists(self, name):
        """Check if a given context exists."""
        contexts = self.data['contexts']
        for context in contexts:
            if context['name'] == name:
                return True
        return False

    def get_context(self, name):
        """Get context from kubeconfig."""
        contexts = self.data['contexts']
        for context in contexts:
            if context['name'] == name:
                return context
        raise KubeConfError("context name not found.")

    def get_contexts(self):
        """Get all contexts in config."""
        return self.data['contexts']   

    def add_context(
        self,
        name,
        cluster_name=None,
        user_name=None,
        namespace_name=None,
        **attrs
        ):
        """Add a context to config."""
        if self.context_exists(name):
            raise KubeConfError("context with the given name already exists.")

        contexts = self.get_contexts()
        
        # Add parameters.
        new_context = {'name': name, 'context':{}}
        
        # Add attributes
        attrs_ = new_context['context']
        if cluster_name is not None:
            attrs_['cluster'] = cluster_name
        if user_name is not None:
            attrs_['user'] = user_name
        if namespace_name is not None:
            attrs_['namespace'] = namespace_name
        attrs_.update(attrs)

        contexts.append(new_context)

    def add_to_context(self, name, **attrs):
        """Add attributes to a context.
        """
        context = self.get_context(name=name)
        attrs_ = context['context']
        attrs_.update(**attrs)

    def remove_from_context(self, name, *args):
        """Remove attributes from a context.
        """
        context = self.get_context(name=name)
        attrs_ = context['context']
        for a in args:
            del attrs_[a]

    def remove_context(self, name):
        """Remove a context from kubeconfig.
        """
        context = self.get_context(name)
        contexts = self.get_contexts()
        contexts.remove(context)

    def set_current_context(self, name):
        """Set the current context in kubeconfig."""
        if self.context_exists(name):
            self.data['current-context'] = name
        else:
            raise KubeConfError("Context does not exist.")

    
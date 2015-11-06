import pwd
import os

from dockerspawner import SystemUserSpawner
from textwrap import dedent
from traitlets import (
    Integer,
    Unicode,
)
from tornado import gen
import getpass

class VolumeSpawner(SystemUserSpawner):
    """ My modification of SystemUserSpawner. """

    container_image = Unicode("jupyter/volumeuser", config=True)
    container_prefix = Unicode("volumespawner", config=True)

    container_username = Unicode("jupyter", config=True)
    host_username = Unicode(getpass.getuser(), config=True)

    host_homedir_format_string = Unicode(
        u"/home/{host_username}/spawned_users/{username}",
        config=True,
        help=dedent(
            """
            Format string for the path to the user's home directory on the host.
            The format string should include `'`host_username` and `username`
            variable, which will be formatted with the host and user's username.
            """
        )
    )

    @property
    def homedir(self):
        """
        Path to the user's home directory in the docker image.
        """
        return "/home/{container_username}".format(
                container_username=self.container_username)

    @property
    def host_homedir(self):
        """
        Path to the volume containing the user's home directory on the host.
        """
        return self.host_homedir_format_string.format(
                host_username=self.host_username,
                username=self.user.name)

    def _user_id_default(self):
        """
        Get user_id of the host from pwd lookup by name

        If the authenticator stores user_id in the user state dict,
        this will never be called, which is necessary if
        the system users are not on the Hub system (i.e. Hub itself is in a container).
        """
        return pwd.getpwnam(self.host_username).pw_uid

    @gen.coroutine
    def start(self, image=None):
        """
        Start the single-user server in a docker container

        Makes sure that homedir on host side exists.
        """
        if not os.path.exists(self.host_homedir):
            self.log.warn(
                    "Folder '%s' doesn't exist. Creating.",
                    self.host_homedir)
            os.makedirs(self.host_homedir)
        else:
            self.log.info(
                    "Folder '%s' exists.",
                    self.host_homedir)

        yield super(VolumeSpawner, self).start(image=image)

from transporter import *
from storages.SFTPStorage import *


TRANSPORTER_CLASS = "TransporterSFTP"


class TransporterSFTP(Transporter):


    name              = 'SFTP'
    valid_settings    = ImmutableSet(["host", "username", "password", "url", "port", "path", "key"])
    required_settings = ImmutableSet(["host", "url"])

    def __init__(self, settings, callback, error_callback, parent_logger=None):
        Transporter.__init__(self, settings, callback, error_callback, parent_logger)

        # Fill out defaults if necessary.
        configured_settings = Set(self.settings.keys())
        if not "port" in configured_settings:
            self.settings["port"] = 22
        if not "path" in configured_settings:
            self.settings["path"] = ""

        # Map the settings to the format expected by FTPStorage.
        if "username" in configured_settings and "password" in configured_settings:
          location = "sftp://" + self.settings["username"] + ":" + self.settings["password"] + "@" + self.settings["host"] + ":" + str(self.settings["port"]) + self.settings["path"]
        else:
          location = "sftp://" + self.settings["host"] + ":" + str(self.settings["port"]) + self.settings["path"]

        self.storage = SFTPStorage(location, self.settings["url"], self.settings["key"])
        try:
            self.storage._start_connection()
        except Exception, e:            
            raise ConnectionError(e)

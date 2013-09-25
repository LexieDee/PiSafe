#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import dbus
import gobject
import time
import subprocess

#: This is the directory where files should be copied to
target_directory = 'target/' #TODO read the target from stdin at startup

class copyWiper:
    """
    This class monitors the computer for auto-mounted removal storage and copies
    files from this mounted storage to a specified target directory. After copy-
    ing the files it wipes the removal storage by writing zeroes (using the unix
    tool dd). 
    """
    pass

class deviceAddedListener:
    """
    This class listens to the dbus for added devices.
    """
    def __init__(self):
        # Connect to dbus
        self.bus = dbus.SystemBus()
        # We are interested in UDisks2 that takes care of the disks:
        self.proxy = self.bus.get_object("org.freedesktop.UDisks2", 
                                    "/org/freedesktop/UDisks2")
        self.iface = dbus.Interface(self.proxy, "org.freedesktop.DBus.ObjectManager")
        # And we are interested in added interfaces:
        self.iface.connect_to_signal('InterfacesAdded', self._on_device_added)
        
    def _on_device_added(self, dev_path, dev_props):
        """
        This method is called if an interface gets added, i.e. the 
        InterfacesAdded signal is triggered by UDisks2. If the interface is
        a block device and has a filesystem, it copies all contents using rsync
        to the target directory. After copying is completed, the device is over-
        written with zeroes using dd. 
        """
        # Check that the added interface is a block device and has a filesystem:
        if 'org.freedesktop.UDisks2.Block' in dev_props and 
                    'org.freedesktop.UDisks2.Filesystem' in dev_props.keys():
            # give the automount a few seconds to mount the storage:
            time.sleep(5)
            # get the proxy for this Filesystem:
            block_proxy = self.bus.get_object("org.freedesktop.UDisks2", 
                                    dev_path)
            block_iface = dbus.Interface(block_proxy, 
                                    "org.freedesktop.DBus.Properties")
            device_bytes = block_iface.Get("org.freedesktop.UDisks2.Block",
                                    "Device")
            # The device path (/dev/xxxx) is in bytes, we want a string
            # Also, the last byte is a terminating null which leads to problems:
            device = "".join(map(lambda b: chr(b), device_bytes[0:-1]))
            mountpoints = block_iface.Get("org.freedesktop.UDisks2.Filesystem",
                                    "MountPoints")
            mountpoint = "".join(map(lambda b: chr(b), mountpoints[0][0:-1]))
            self._copy_files_from_media(mountpoint+"/",target_directory)
            #TODO check exit value
            self._wipe_media(device)
            #TODO check exit value
    
    def _copy_files_from_media(self, source, target):
        args = ['rsync', '-a', source, target]
        subprocess.call(args)
    
    def _wipe_media(self,dev_path):
        # TODO be kind and unmount first
        subprocess.call(['dd', 'if=/dev/zero', 'of='+dev_path])
        pass

if __name__ == '__main__':
    from dbus.mainloop.glib import DBusGMainLoop
    DBusGMainLoop(set_as_default=True)
    loop = gobject.MainLoop()
    deviceAddedListener()
    loop.run()

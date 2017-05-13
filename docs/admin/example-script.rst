Example Script
==============

To effectively use this module, you will need to write a script that
polls your constellation server for new MAC addresses.  The original
use case this module was written for was feeding MAC addresses into a
DHCP server to facilitate registered device access policies.  To
implement this requires two scripts, one to poll the new MAC
addresses, and one to restart dhcpd, both scripts are provided below
for you to use as examples:


OpenBSD DHCPD Supervisor
------------------------
.. code-block:: python

   #!/usr/bin/python

   import argparse
   import logging
   import requests
   import subprocess
   import sys

   from jinja2 import Template


   def getMacs(url):
       logger = logging.getLogger("MACRetriever")
       try:
           r = requests.get(url)
           if r.status_code == 200:
               logger.debug("API Request OK")
               try:
                   return r.json()
               except ValueError as e:
                   logger.critical(e + "Unpacking data failed.  Bailing out!")
                   sys.exit(2)
           else:
               logger.critical("API request failed.  Bailing out!")
               sys.exit(1)
       except:
           logger.critical("Could not make request to API.  Bailing out!")
           sys.exit(1)


   def templateMacs(macs, fpath):
       try:
           with open(fpath, 'r') as f:
               conf = f.read()
               if len(macs) == conf.count("hardware ethernet"):
                   logging.debug("No change, don't need to update")
                   return
               else:
                   logging.info("Change detected, updating configuration")
       except:
           logging.warning("Couldn't load old configuration file")

       # This line has to be long to avoid a Jinja2 Template error
       templateStr = "{% for device in devices %}host {{ device.hostname }} { hardware ethernet {{ device.MAC }}; } # Device: '{{ device.name }}'; Owned By: {{ device.owner}}\n{% endfor %}" # noqa 401

       template = Template(templateStr)
       conf = template.render({"devices": macs}).encode("utf8")

       with open(fpath, 'w') as f:
           f.write(conf)

       # Restart dhcpd, this command should probably be a script, since it will be
       # necessary to assemble the config file fragment written by this script
       # with the config file that runs the rest of DHCPd.
       subprocess.call(args.restart_cmd.split(" "))


   if __name__ == "__main__":
       parser = argparse.ArgumentParser(
           description='Retrieve MAC addresses and build a config file')
       parser.add_argument("url",
                           help="URL for API access to summon MAC addresses")
       parser.add_argument("path", help="Path to save MAC addresses to")
       parser.add_argument("restart_cmd", help="Full command to restart dhcpd")
       parser.add_argument("-v", "--verbose", action="store_true",
                           help="Increase verbosity")
       args = parser.parse_args()

       if args.verbose:
           logging.basicConfig(level=logging.DEBUG)
       else:
           logging.basicConfig(level=logging.INFO)
       macs = getMacs(args.url)
       logging.debug(macs)
       templateMacs(macs, args.path)

This script does most of the work, it obtains the new MAC addresses,
decides whether or not to restart the DHCPd instance, and tracks state
through the dhcp configuration file.  This is designed to be run on a
cron job such as the one shown below:

.. code-block:: none

   */5 * * * * root /usr/local/sbin/openbsd-dhcpd-supervisor https://constellation.MySite.com/devices/api/v1/device/show/all /etc/dhcpd.conf.d/15-user-macs /usr/local/sbin/dhcpd-reconf >/dev/null 2>&1

   
DHCPd Restart Script
^^^^^^^^^^^^^^^^^^^^
.. code-block:: sh

   #!/bin/sh

   # This assembles all of the snippets into a complete configuration file
   cat /etc/dhcpd.conf.d/* > /etc/dhcpd.conf

   # Restart dhcpd iff the new config file checks out
   if dhcpd -n ; then
       /etc/rc.d/dhcpd restart
   else
       printf "Refusing to restart dhcpd: dhcpd.conf contains errors!\n"
   fi

This script will assemble the configuration files, check the resulting
file for errors, and then restart dhcpd.

.. warning:: As written, the script above will not restart the DHCP
             server if errors are present, but the file will still
             have overwritten the last known good configuration that
             worked.

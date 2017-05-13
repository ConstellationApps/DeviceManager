API Documentation
=================

The MAC addresses stored in the Constellation DeviceManager can be
retrieved using the API.  The general expectation is to use the API to
query for all devices, but an additional API endpoint exists to get a
list of devices for a particular user.


A quick example with curl
-------------------------
.. code-block:: bash

    $ curl https://constellation.MySite.com/devices/api/v1/device/show/all | jq
    
    [
      {
        "owner": "maldridge",
        "hostname": "maldridge-anker-1",
        "name": "Silver Anker Dongle",
        "MAC": "00:E0:97:00:2B:5D"
      },
    ]
    
.. note:: The above example pipes the output through :code:`jq` to
          improve readability for this documentation.  The output you
          recieve from the API does not have whitespace and is
          intended to be machine readable, not human readable.

.. warning:: The feed shown above is unauthenticated, you should
             consider what risks this may or may not pose to your
             environment and take appropriate steps to secure access
             to this feed with your webserver.


Its also possible to query for a particular user by instead hitting
the user endpoint on the API:

.. code-block:: bash

   $ curl https://constellation.MySite.com/devices/api/v1/device/show/user/maldridge | jq
    
   [
     {
       "model": "constellation_devicemanager.device",
       "pk": "00:E0:97:00:2B:5D",
       "fields": {
         "name": "Silver Anker Dongle",
         "hostname": "maldridge-anker-1",
         "owner": 1
       }
     },
   ]

.. note:: The above example pipes the output through :code:`jq` to
          improve readability for this documentation.  The output you
          recieve from the API does not have whitespace and is
          intended to be machine readable, not human readable.

.. warning:: The feed shown above is unauthenticated, you should
             consider what risks this may or may not pose to your
             environment and take appropriate steps to secure access
             to this feed with your webserver.

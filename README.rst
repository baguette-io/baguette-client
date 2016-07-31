baguette-client
===============


Login
-----

::

    [my-code]$ baguette login
    >>> username/email
    >>> password
    >>> Login successfull. Credentials valid for 10 hours.


App creation
------------

::

    [my-code]$ baguette create my_app
    >>> automatically added git://azerty1234.git.baguette.io to your remote
    >>> When you will git push to this remote, your app will be deployed.


Log
---

::

    [my-code]$ baguette log
    [my-code]$ baguette log -f

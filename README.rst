baguette-client
===============


Help
----

::

    [my-code]$ baguette
    Usage: baguette [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

      Commands:
        signup  Create an account on baguette.io
        login   Connect to baguette.io using email/password.
        app create
        app list
        app delete
        key create
        key list
        key delete
        vpc create
        vpc list
        vpc delete


Signup
------

::

    [my-code]$ baguette signup
    Username [test]:
    Email:
    Password:
    Repeat for confirmation:

Login
-----

::

    [my-code]$ baguette login
    Please enter your baguette.io credentials.
    Email: test@test.test
    Password: 
    Successfully logged in as test@test.test.


Create
------

::

    [my-code] baguette create

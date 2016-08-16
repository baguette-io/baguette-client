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
        create  Create an app of the current git repo.
        login   Connect to baguette.io using email/password.
        signup  Create an account on baguette.io :param...


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

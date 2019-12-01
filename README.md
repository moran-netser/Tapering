# Tapering

## How to use this project

In the following I assume that you have a shell open in the root directory of this project.
When you run `ls` you should see a `setup.py` and a `tapering` directory, and this file `README.md`.

    $ ls
    README.md
    setup.py
    tapering

Now, make a python virtual environment (`virtualenv`)

    $ virtualenv -p python3 python3

You only have to do this once.

Once the `virtualenv` is in place, activate it:

   $ source python3/bin/activate
   
You should see a `(python3)` prefix in your prompt. 
Now, if this is the first time, you have to install the `tapering` package like so:

    $ pip install -e .

You only have to do this once.

Now, you should be able to run `tap` - which is the command that actually does the work.

    $ tap -h
    usage: tap [-h] [--resolution RESOLUTION] {constant-hotzone,linear-profile}

    positional arguments:
    {constant-hotzone,linear-profile}

    optional arguments:
    -h, --help            show this help message and exit
    --resolution RESOLUTION, -r RESOLUTION

for instance, to run the `linear-profile` problem:

    $ tap linear-profile

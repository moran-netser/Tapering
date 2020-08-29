# Tapering

## How to use this project

In the following I assume that you have a shell open in the root directory of this project.
When you run `ls` you should see a `setup.py`.

Now, make a python virtual environment (`virtualenv`) and activate it:

    $ virtualenv -p python3 python3
    $ source python3/bin/activate
   
You should see a `(python3)` prefix in your prompt. 
Now, if this is the first time, you have to install the `tapering` package like so:

    $ pip install -e .

You only have to do this once.

Now, you should be able to run `tapering` - which is the command that actually does the work.

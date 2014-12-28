# devcli

`devcli` is a command line tool to create command line tools.

# Creating your new tool

Start by calling `devcli create -n TOOL_NAME -d DIR_TO_CREATE`, where
**TOOL_NAME** is how you want to call your new CLI tool. **DIR_TO_CREATE** is
where you want it be be created. Example:

    ./devcli create -n mytool -d ~/Projects/myproject

# Extending your new tool

In the above example a directory `~/Projects/myproject/mytool.d` will be
created. Any scripts added to this directory will be available as _commands_ to your
tool. Check the `template` script to see an example of a simple command.

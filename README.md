# devcli

`devcli` is a command line tool to create command line tools.

# Creating your new tool

The first thing you need is to download devcli by cloning this repo and `cd` into it.

Start by calling `devcli create -n TOOL_NAME -d DIR_TO_CREATE`, where
**TOOL_NAME** is how you want to call your new CLI tool. **DIR_TO_CREATE** is
where you want it be be created. Example:

```
./devcli create -n mytool -d ~/Projects/myproject
```

Now, if you go to `~/Projects/myproject` you should see the initial structure for
your CLI. Take a look at the scripts to see examples of what you can do!

# Extending your new tool

Any scripts added to the CLI directory will be available as _commands_ to your
tool. Check the `template` script to see an example of a simple command.

Let's create a new hello world command. Create a `hello_world` file (without `.sh`)
and add the following to it:

```
#!/bin/bash

echo "Hello World"
```

Now, whe you run `./mytool hello_world` you should see `Hello World` on your terminal!

For each command you might want to give the user some context on what it does and
how to use it. To do that you'll just need to define two variable, one called
`SUBCOMMAND_DESC` where you can give a shor description of your command and another called
`SUBCOMMAND_HELP` for a more detailed explanation on what subcommands it takes, arguments
that are required and environment variable that it uses.

For now edit your `hello_world` file to include the following right after `#!/bin/bash`:

```
SUBCOMMAND_DESC="Say Hello to the World!"
SUBCOMMAND_HELP=$(cat <<EOH

Say hello and enjoy your day!
EOH
)
```

Now, if you run `./mytool help` you should get back the defined commands, including:

```
  hello_world:          Say Hello to the World!
```

If you run `./mytool hello_world help` you'll get the more detailed version.

# Helper functions

Some functions are defined right at `mytool` and are available to all your scripts.

As an example, let's see how to display information using a color schema:

```
in_red()      # use for failures
in_green()    # use for successes
in_yellow()   # use for warnings / attention
in_magenta()  # use for debug messages
in_cyan()     # use for main actions / progress
```

If you use `in_cyan "Hello World"` you'll see `Hello World` in cyan. Check that file out
to see other useful functions.

You can also change that file to add your own helper functions

# Helper files

If you want to have some functions that are shared accross other commands you can create a
file with `_` at the beginning, like `_my_helper`, and just put your functions there. Now other commands can
use those functions by just including `use 'my_helper'`. Note that you don't need to prefix it with `_`!


Dynamic DNS for WebFaction
==========================

Just a little Python script that updates DNS records on WebFaction.

USAGE
=====
=====

To use this script, all you need to do is 3 things:

###1. Clone the repo.

    git clone git@github.com:o4dev/Dynamic-DNS_WebFraction.git

###2. Create/Edit a config file.

Below is the contents of the example file, `ddns.config`.
**It is recommended that you just edit it to suit your needs.**

    # config for ddns.py
    
    # First line must be WebFaction username
    username
    
    # domains to set
    example.com

In short,
*   all comments start with a  `# `,
*   comments and blank lines are not counted,
*   the first line is your user account,
*   and the following lines are the domains you wish to change.


To avoid saving passwords in plain text,
they are not stored in the config file.
You shall be prompted to enter it at first run
then it will be saved to your system's keyring
using Python's `keyring` module.

###3. Run the script.

If you just edited `ddns.config`, it is as simple as:

    python ddns.py

Otherwise:

    python ddns.py [config_file]


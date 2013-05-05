Dynamic DNS for WebFaction
==========================

Just a little Python script that updates DNS records on WebFaction.

USAGE
=====

To use this all you need to do is 2 things:
    
    1. Create a config file
        
        In short,
                    * all comments start with a '#',
                    * comments and blank lines are not counted,
                    * the first line is your user account,
                    * and the following lines are the domains you wish to change.

        There is an example file, 'ddns.config'.
        You could just edit that if you wish.

        To avoid saving passwords in plain text,
        they are not stored in the config file.
        You shall be prompt to enter it at first run
        then it will be saved to your system's keyring
         using Python's 'keyring' module.

    2. Run the script

        If you just edited 'ddns.config', it is as simple as:
            'python ddns.py'

        Otherwise just:
            'python ddns.py [config_file]'


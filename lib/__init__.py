#!/usr/bin/env python

import os


map(lambda d:
    map(lambda f:
        os.symlink(os.path.join('default', f), os.path.join(d, f)),
        set(os.listdir(os.path.join(d, 'default'))) - set(os.listdir(d))),
    ('config', 'dotfile'))

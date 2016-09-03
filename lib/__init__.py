#!/usr/bin/env python

import shutil
import os


map(lambda d:
    map(lambda f:
        shutil.copyfile(os.path.join(d, 'default', f), os.path.join(d, f)),
        set(os.listdir(os.path.join(d, 'default'))) - set(os.listdir(d))),
    ('config', 'dotfile'))

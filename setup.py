from setuptools import setup
import sys
import os
from dfilter_imaging import version
import json

data = [version.git_origin, version.git_hash, version.git_description, version.git_branch]
with open(os.path.join('dfilter_imaging', 'GIT_INFO'), 'w') as outfile:
    json.dump(data, outfile)

def package_files(package_dir, subdirectory):
    # walk the input package_dir/subdirectory
    # return a package_data list
    paths = []
    directory = os.path.join(package_dir, subdirectory)
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            path = path.replace(package_dir + '/', '')
            paths.append(os.path.join(path, filename))
    return paths
data_files = package_files('dfilter_imaging', 'data') 

setup_args = {
    'name':         'dfilter_imaging',
    'author':       'Ridhima Nunhokee',
    'url':          'https://github.com/Chuneeta/dfilter_imaging',
    'license':      'BSD',
    'version':      version.version,
    'description':  'Delay Filtering Imager.',
    'packages':     ['dfilter_imaging'],
    'package_dir':  {'dfilter_imaging': 'dfilter_imaging'},
    'package_data': {'dfilter_imaging': data_files},
    'install_requires': ['numpy>=1.14', 'beam_solver', 'matplotlib>=2.2'],
    'include_package_data': True,
    #'scripts': ['scripts/pspec_run.py', 'scripts/pspec_red.py',
    #            'scripts/bootstrap_run.py'],
    'zip_safe':     False,
}

if __name__ == '__main__':
    setup(*(), **setup_args)   
# apply(setup, (), setup_args)

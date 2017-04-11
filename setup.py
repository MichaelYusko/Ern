from distutils.core import setup

import ern

setup_kwargs = {
    'name': 'ern',
    'version': ern.__version__,
    'url': 'https://github.com/MichaelYusko/Ern',
    'license': 'GNU',
    'author': 'Fresh Jelly',
    'author_email': 'freshjelly12@yahoo.com',
    'description': (
        'Minimalist tool which will work with oauth authentication,'
        ' and will be able to connect to Slack Api and etc.'),
    'packages': ['ern'],
    'classifiers': [
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: GNU General Public License (GPL)'
    ],
 }

requirements = ['requests>=2.13.0']
setup_kwargs['install_requires'] = requirements

setup(**setup_kwargs)

print(u"\n\n\t\t    "
      "Ern version {} installation succeeded.\n".format(ern.__version__))

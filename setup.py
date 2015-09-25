from distutils.core import setup

__author__ = 'Tim'

setup(name="pyresttest3",
      version="0.1",
      description="Python RESTful API Testing Tools written in python3",
      keywords=['rest', 'web', 'http', 'testing', 'python3'],
      packages=['pyresttest3', 'pyresttest3.utils'],
      license='Apache License, Version 2.0',
      requires=['jinja2', 'requests', 'BeautifulSoup4'],
      scripts=[],  # Make this executable from command line when installed
      provides=['pyresttest3']
      )

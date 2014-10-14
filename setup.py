import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='purple-framework',
	  version='0.1',
	  description='Framework for building dsls.',
	  url='https://github.com/4toblerone/Purple',
	  keywords='dsl framework domain specific language',
	  author='Sasa Trifunovic',
	  author_email='sasa.s.trifunovic@gmail.com',
	  license='BSD',
	  install_requires = ['ply==3.4'],
	  long_description = read('README.md'),
	)
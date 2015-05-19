import os
from setuptools import setup


f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
readme = f.read()
f.close()


setup(
	name='ormconfig',
	version=__import__('ormconfig').__version__,
    description='A little orm for config file',
    long_description=readme,
    author='Sun Jin',
    author_email='sunjinopensource@qq.com',
    url='https://github.com/sunjinopensource/ormconfig/',
	py_modules=['ormconfig'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)

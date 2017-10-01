from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='cfile',
      version='0.1.4',
      description='A python C code generator',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4'
      ],      
      url='http://github.com/cogu/cfile',
      author='Conny Gustafsson',
      author_email='congus8@gmail.com',
      license='MIT',
      packages=['cfile'],
      zip_safe=False)

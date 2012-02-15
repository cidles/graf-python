from distutils.core import setup
setup(name='python-graf',
        version='0.1.0',
        description='Python implementation of the Graph Annotation Framework',
        #long_description='',
        author='Stephen Matysik',
        author_email='smatysik@gmail.com',
        url='http://www.americannationalcorpus.org/graf-wiki',
        packages=[ 'graf' ],
        package_dir={'graf': 'src/graf'},
    )

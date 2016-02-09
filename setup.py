from setuptools import setup

setup(name='glaso',
      version='0.0.1',
      description='Web application library',
      url='https://github.com/korakon/glaso',
      author='Korakon',
      author_email='i@korakon.com',
      license='CC0',
      packages=['glaso'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      install_requires=[
          'Werkzeug'
      ])

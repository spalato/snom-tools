from setuptools import setup, find_packages

setup(name='snom',
      version='0.1',
      description='SNOM data analysis tools',
      url='',
      author='S. Palato',
      author_email='',
      license='',
      packages=find_packages("src"),
      package_dir={"": "src"},
zip_safe=False)

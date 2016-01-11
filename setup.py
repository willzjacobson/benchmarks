from distutils.core import setup

from pip.req import parse_requirements

# parse requirements
install_reqs = parse_requirements("requirements.txt")
# reqs is a list of requirements
reqs = [str(ir.req) for ir in install_reqs]

setup(
        name='Babbage',
        version='0.2',
        packages=['', 'svm', 'arima', 'shared', 'ts_proc', 'weather',
                  'electric', 'occupancy', 'benchmarks', 'benchmarks.steam',
                  'benchmarks.electric', 'space_temp', 'startup_rampdown'],
        url='https://github.com/PrescriptiveData/datascience',
        license='No license',
        author='David Karapetyan',
        author_email='dkarapetyan@prescriptivedata.io',
        description='An analytics and prediction engine'
                    ' for energy and electricity usage in'
                    ' commercial and non-commercial buildings.',
        install_requires=reqs
)

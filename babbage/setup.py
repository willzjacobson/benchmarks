# coding=utf-8
import sys
from setuptools import setup, find_packages
from pip.req import parse_requirements
from pip.download import PipSession

if not sys.version_info.major == 2 and sys.version_info.minor == 7:
    sys.exit("Sorry, Python 3 is not supported")

# parse requirements
install_reqs = parse_requirements("requirements.txt",
                                  session=PipSession())
# reqs is a list of requirements
reqs = [str(ir.req) for ir in install_reqs]
pkgs = find_packages(exclude=["*.tests"])
# magic function for including subpackages in repo
# can list packages with subpackages explicitly later
setup(
        name='Babbage',
        version='0.2',
        packages=pkgs,
        url='https://github.com/PrescriptiveData/datascience',
        license='Proprietary',
        author='PrescriptiveData',
        author_email='dkarapetyan@prescriptivedata.io',
        description=(
            'An analytics and prediction engine'
            ' for energy and electricity usage in'
            ' commercial and non-commercial buildings.'
        ),
        platform='linux2',
        install_requires=reqs
)

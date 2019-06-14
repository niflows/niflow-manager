from setuptools import setup

import versioneer

version = versioneer.get_version()
cmdclass = versioneer.get_cmdclass()

setup(name="niflow-manager", version=version, cmdclass=cmdclass)

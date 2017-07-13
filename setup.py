from setuptools import setup

setup(
      name='fedex_wrapper',
      version='0.0.1',
      description='A wrapper for the FedEx API based on zeep.',
      long_description='Wrapper for the FedEx API based on zeep.',
      url='https://github.com/Vanclief/fedex-wrapper',
      author='iuPick',
      author_email='devops@iupick.com',
      license='Pending',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: API',
        'License :: Pending :: Pending',
        'Programming Language :: Python :: 3.6',
      ],
      keywords='fedex api iuPick',
      install_requires=['zeep'],
      python_requires='>=3.6',
)
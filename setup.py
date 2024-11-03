from setuptools import (
    setup,
    find_packages,
)


setup(
    name='source_iter',
    version='0.24.0',
    python_requires=">=3.6",
    description='This is a tiny Python package that serves read/write iterators '
                'for most mandatory sources via default packages like CSV / JSONL / SQLite',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nicolay-r/source-iter',
    author='Nicolay Rusnachenko',
    author_email='rusnicolay@gmail.com',
    license='MIT License',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='data-iterators',
    packages=find_packages()
)

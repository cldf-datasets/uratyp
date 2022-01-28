from setuptools import setup


setup(
    name='cldfbench_uratyp',
    py_modules=['cldfbench_uratyp'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'uratyp=cldfbench_uratyp:Dataset',
        ],
        'cldfbench.commands': [
            'uratyp=uratypcommands',
        ],
    },
    install_requires=[
        'clldutils>=3.10.1',
        'cldfbench',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)

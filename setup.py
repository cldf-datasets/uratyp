from setuptools import setup


setup(
    name='cldfbench_uratyp',
    py_modules=['cldfbench_uratyp'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'uratyp=cldfbench_uratyp:Dataset',
        ]
    },
    install_requires=[
        'cldfbench',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)

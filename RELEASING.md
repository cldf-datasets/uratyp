# Releasing UraTyp

The dataset should be "installed", i.e. you should have run
```shell
pip install -e .[test]
```
ideally in a separate virtual environment.


- Recreate the CLDF data:
  ```shell
  cldfbench makecldf cldfbench_uratyp.py --glottolog PATH/TO/glottolog/glottolog --glottolog-version v4.4
  ```
- Validate it:
  ```shell
  pytest
  ```
- Recreate the human-readable dataset description:
  ```shell
  cldfbench cldfreadme cldfbench_uratyp.py
  ```


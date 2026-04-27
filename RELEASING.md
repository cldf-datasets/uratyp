# Releasing UraTyp

The dataset should be "installed", i.e. you should have run
```shell
pip install -e .[test]
```
ideally in a separate virtual environment.


- Recreate the CLDF data:
  ```shell
  cldfbench makecldf cldfbench_uratyp.py --with-zenodo --with-cldfreadme --glottolog ../../glottolog/glottolog --glottolog-version v5.3
  ```
- Validate it:
  ```shell
  pytest
  cldf validate cldf --with-cldf-markdown
  ```


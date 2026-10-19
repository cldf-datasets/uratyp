# Releasing UraTyp

```shell
git clone https://github.com/cldf-datasets/uratyp
cd uratyp
```


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

```shell
pip install cldfviz[cartopy]
cldfbench cldfviz.map cldf --format svg --height 50 --output map.svg --markersize 70 --padding-left 8 --padding-right 8 --padding-top 3 --padding-bottom 3 --with-ocean --language-properties Subfamily --language-labels
```


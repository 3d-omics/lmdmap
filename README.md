# lmdmap

## Installation

```{sh}
pip install git+https://github.com/3d-omics/lmdmap.git
```

## Update

```{sh}
pip uninstall lmdmap
pip install git+https://github.com/3d-omics/lmdmap.git

```


## Usage

```{sh}
lmdmap G007bI105A input/241113G007bI105post.jpg
lmdmap -n G007bI105A -i input/241113G007bI105post.jpg -t 241113G007bI105.csv -o 241113G007bI105.jpg -m 241113G007bI105_marked.jpg
lmdmap --name G007bI105A --image input/241113G007bI105post.jpg --draw-microsamples
```

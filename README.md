# lmdmap

**lmdmap** is a small python module to crop slide overview images into cryosection-specific overviews and to calculate and print the pixel coordinates of the microsamples. It is a tool used to display the spatial location of laser-microdissected samples in cryosection overviews, designed to generate the data displayed in the 3D'omics visualisation platform.

![Overview of input and output data](overview.png "Overview of input and output data")

## Installation

The latest version of **lmdmap** and its dependencies can be easily installed in any unix environment using the following code.

```{sh}
pip install git+https://github.com/3d-omics/lmdmap.git
```

To install a specific version use the following

```{sh}
pip install git+https://github.com/3d-omics/lmdmap.git@v1.0.0
```

## Update

If a new **lmdmap** version is released, you can upgrade the module using the following code.

```{sh}
pip uninstall lmdmap -y
pip install git+https://github.com/3d-omics/lmdmap.git
```

## Add Airtable API KEY

**lmdmap** retrieves the information of the microsamples directly from the 3D'omics Airtable database. In order for Airtable to enable your computer to fetch data from the database you need to declare an AIRTABLE_API_KEY, which can be created for you by the database administrator.

Then, you can declare the variable for a one-time usage:
```{sh}
export AIRTABLE_API_KEY="THISISWHERETHEAPIKEYSHOULDBEPASTED"
lmdmap -n G007bI105A -i 241113G007bI105post.jpg
```

Or you can save it in your shell configuration file `~/.bashrc, ~/.zshrc` to keep it forever:
```{sh}
nano ~/.bashrc
export AIRTABLE_API_KEY="THISISWHERETHEAPIKEYSHOULDBEPASTED"
source ~/.bashrc
```

## Usage

The minimum arguments needed to use **lmdmap** are the cryosection name (***-n***), which is used to fetch the relevant information from the 3D'omics Airtable database as well as to name the default output files, and the slide overview image (***-i***) from which the cropped image is generated.

By default, **lmdmap** creates to documents in the working directory: a csv file containing the pixel coordinates, and jpg file of the cropped image.

The following optional arguments can be also used for defining outputs:

- ***-t*** enables defining the path and name of the csv table.
- ***-o*** enables defining the path and name of the regular cropped image.
- ***-m*** enables defining the path and name of the cropped image with the positions of microsamples marked.

```{sh}
lmdmap -n G007bI105A -i 241113G007bI105post.jpg
lmdmap -n G007bI105A -i 241113G007bI105post.jpg -t mycustomoutput.csv -o mycustomoutput.jpg -m mycustomoutput_marked.jpg
lmdmap --name G007bI105A --image input/241113G007bI105post.jpg --draw-microsamples
```

The following optional arguments can be used to manually correct the offset of the cutting points and the stretch of the image:

- ***-x*** pixel offset in the x axis.
- ***-y*** pixel offset in the y axis.
- ***-w*** percentage image stretch in the x axis.
- ***-l*** percentage image stretch in the y axis.
- ***-s*** size of the cropping square in pixels (default: 1000).
- ***-c*** display microsample ID codes on image.
- ***-d*** comma-separated list of undesired microsamples to be manually discarded.

```{sh}
G103bO202A_marked.jpg lmdmap -n G103bO202A -i G103bO202_post.jpg -x -92 -l 4 -t G103bO202A.csv -o G103bO202A.jpg -m G103bO202A_marked.jpg
lmdmap -n G121eO302A -i G121eO302_pre.jpg -x -100 -t G121eO302A.csv -o G121eO302A.jpg -m G121eO302A_marked.jpg
```

The following optional arguments can be used to bypass errors and update records in Airtable:

- ***-e*** ignore errors for the pixel coordinate calculations.
- ***-a*** log errors and pixel coordinates in Airtable.

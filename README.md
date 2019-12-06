![License](https://img.shields.io/badge/license-BSD-green.svg)

# SVD utility

This toolbox can be used to compute Region of Interest (ROI) time course by mean of singular value decomposition (SVD). Results are exported to
[cartool](https://sites.google.com/site/cartoolcommunity/)'s result of inverse solution (.ris) file format.

![svd_utility](./img/screenshot.jpg "svd")

# Installation

To install the toolbox, clone this repository:
```
git clone https://github.com/Functional-Brain-Mapping-Laboratory/SVD_utility.git
```
Then go to the repository main folder and install dependencies:

```
cd SVD_utility
pip install -r requirements.txt
```

# Run

To run the toolbox, go to the repository main folder and type:

```
python -m svd
```

For each single ROI, the toolbox computes 1 unique SVD.

When opening several file, the toolbox concatenates time points of all files before fitting SVD. Then fitted SVD is applied to each individual file. That is to say, for each ROI the **same SVD** is applied to each individual file.

A csv file containing the explained variance score of each fitted SVD (Fit), and the explained variance score of each individual file for each ROI is save along results.


Setting scaling option to 'None' returns the first components of the SVD decomposition.
Setting scaling option to 'Eigenvalue' returns the first components of the SVD decomposition multiplied by its first singular value.

# References

Estimating Eeg Source Dipole Orientation Based on Singular-value Decomposition For Connectivity Analysis
M. Rubega-M. Carboni-M. Seeber-D. Pascucci-S. Tourbier-G. Toscano-P. Mierlo-P. Hagmann-G. Plomp-S. Vulliemoz-C. Michel - https://link.springer.com/article/10.1007/s10548-018-0691-2

# directory containing the datasets
DATA_PATH = "/data/matrix/mtx2"

# datasets in the format: (file_name, matrix_size)
# in a .mtx matrix file the first line not starting with % contains the triplet
#   rows columns nonzeros
# pagerank is defined for square matrices so rows and columns must be equal and 
# matrix_size coincides with the number of rows and columns  
datasets = [
    ('eu-2005', 862664),
    ('hollywood-2009', 1139905),
    ('in-2004', 1382908),
]


# some datasets from https://sparse.tamu.edu/LAW
"""
    ('cnr-2000', 325557),
    ('dblp-2010', 326186),
    ('amazon-2008', 735323),
    ('eu-2005', 862664),
    ('hollywood-2009', 1139905),
    ('in-2004', 1382908),
    ('ljournal-2008', 5363260),
    ('indochina-2004', 7414866),
    ('uk-2002', 18520486),
    ('arabic-2005', 22744080),
    ('uk-2005', 39459925),
    ('it-2004', 41291594),
"""

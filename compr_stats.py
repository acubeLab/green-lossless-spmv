import os
import pandas as pd
from datetime import datetime

DATA_PATH = "/data/matrix/mtx"

datasets = [
    ('enron', 69244),
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
]

def get_graph_dim(mtxpath) :
    infile = open(mtxpath, 'r')
    line = infile.readline()
    while line.lstrip().startswith('%') :
        line = infile.readline()
    tokens = line.split()
    assert(len(tokens) == 3)
    rows,cols,edges = [int(x) for x in tokens]
    infile.close()
    assert(rows==cols)
    return rows, edges

def get_sizes(basedir, dataset, pardegree=1) :
    if (pardegree == 1) :
        #k²-tree
        kt_size = os.path.getsize(f'{basedir}/{dataset}.t.kt')

        #zuckerli
        zkr_size = os.path.getsize(f'{basedir}/{dataset}.t.zkr')

        #mm-repair
        vc_size = os.path.getsize(f'{basedir}/{dataset}.mtx.rowm.vc')
        vc_C_size = os.path.getsize(f'{basedir}/{dataset}.mtx.rowm.vc.C')
        vc_C_ans_size = os.path.getsize(f'{basedir}/{dataset}.mtx.rowm.vc.C.ansf.1')
        vc_C_iv_size = os.path.getsize(f'{basedir}/{dataset}.mtx.rowm.vc.C.iv')
        vc_R_size = os.path.getsize(f'{basedir}/{dataset}.mtx.rowm.vc.R')
        vc_R_iv_size = os.path.getsize(f'{basedir}/{dataset}.mtx.rowm.vc.R.iv')
    else :
        kt_size, zkr_size, vc_size, vc_C_size, vc_C_ans_size, vc_C_iv_size, vc_R_size, vc_R_iv_size = 0
        for tid in range(pardegree) :
            #k²-tree
            kt_size += os.path.getsize(f'{basedir}/{dataset}.t.{pardegree}.{tid}.kt')

            #zuckerli
            zkr_size += os.path.getsize(f'{basedir}/{dataset}.t.{pardegree}.{tid}.zkr')

            #mm-repair
            vc_size += os.path.getsize(f'{basedir}/{dataset}.mtx.rowm.{pardegree}.{tid}.vc')
            vc_C_size += os.path.getsize(f'{basedir}/{dataset}.mtx.rowm.{pardegree}.{tid}.vc.C')
            vc_C_ans_size += os.path.getsize(f'{basedir}/{dataset}.mtx.rowm.{pardegree}.{tid}.vc.C.ansf.1')
            vc_C_iv_size += os.path.getsize(f'{basedir}/{dataset}.mtx.rowm.{pardegree}.{tid}.vc.C.iv')
            vc_R_size += os.path.getsize(f'{basedir}/{dataset}.mtx.rowm.{pardegree}.{tid}.vc.R')
            vc_R_iv_size += os.path.getsize(f'{basedir}/{dataset}.mtx.rowm.{pardegree}.{tid}.vc.R.iv')

    val_size = os.path.getsize(f'{basedir}/{dataset}.mtx.rowm.val')

    csrv_size = val_size + vc_size
    re32_size = val_size + vc_C_size + vc_R_size
    reiv_size = val_size + vc_C_iv_size + vc_R_iv_size
    re_size   = val_size + vc_C_ans_size + vc_R_iv_size

    return kt_size, zkr_size, csrv_size, re32_size, reiv_size, re_size

def print_table(basedir, pardegree=1) :
    SIZE_LABELS = ['KT_SIZE', 'ZKR_SIZE', 'CSRV_SIZE', 'RE32_SIZE', 'REIV_SIZE', 'RE_SIZE'] 
    SIZE_PER_EDGE_LABELS = ['KT_BPE', 'ZKR_BPE', 'CSRV_BPE', 'RE32_BPE', 'REIV_BPE', 'RE_BPE'] 

    columns = ['DATASET','NNODES','NEDGES']
    columns.extend(SIZE_LABELS)
    columns.extend(SIZE_PER_EDGE_LABELS)

    rows = []
    for dataset,dim in datasets :
        nnodes,nedges = get_graph_dim(f'{basedir}/{dataset}.mtx')
        assert(nnodes == dim)
        sizes = get_sizes(basedir, dataset, pardegree)

        data = [dataset, nnodes, nedges]
        data.extend(sizes)
        data.extend([x*8/nedges for x in sizes])

        rows.append(data)
    
    df = pd.DataFrame(rows, columns = columns) 

    print(df)
    csvfilepath = 'stats.csv'
    df.to_csv(csvfilepath, index=False)

def main() :
    print_table(DATA_PATH)

if __name__ == '__main__' :
    main()

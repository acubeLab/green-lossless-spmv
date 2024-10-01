import os, sys

BUILD_DIR = "build"
DATA_PATH = "example"

# zkr
ZKR_DIR = "zuckerli"
ZKR_BUILD_DIR = f"{BUILD_DIR}/zuckerli"
ZKR_ENC = f"{ZKR_BUILD_DIR}/encoder"

# kt
KT_DIR = 'k2tree_basic_v0.1'
KT_BUILD_DIR = f'{BUILD_DIR}/k2tree_basic_v0.1'
KT_ENC = f'{KT_BUILD_DIR}/build_tree'
KTRD_ENC = f'{KT_BUILD_DIR}/build_tree_rd'

# mr
MMR_DIR = 'mm-repair'
MMR_ENC = f'{MMR_DIR}/matrepair'
MMR_COUNT = f'{MMR_DIR}/pagerank/mtx2rowm'

datasets = [
    ('enron', 69244),
]
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
]
"""

# possibly overrides DATA_PATH and datasets
if os.path.exists("datasets.py"):
    exec(open("datasets.py").read())


    
def check_exist(infilepath, abort=True):
    if not os.path.exists(infilepath):
        print('File', infilepath, 'does not exist')
        if abort :
            exit(1)
        else :
            return False
    return True

def main(pardegrees) :
    ext = 'mtx'
    for data,nnodes in datasets:
        
        print(f"Transposing {data} (0-based, for mm-repair)")
        check_exist(f'{DATA_PATH}/{data}.{ext}')
        os.system(f"{MMR_COUNT} {DATA_PATH}/{data}.{ext}")
        check_exist(f'{DATA_PATH}/{data}.{ext}.rowm')
        check_exist(f'{DATA_PATH}/{data}.{ext}.ccount')

        print(f"Transposing {data} (1-based)")
        check_exist(f'{DATA_PATH}/{data}.{ext}')
        os.system(f"python3 utils/transpose_mtx.py {DATA_PATH}/{data}.{ext}")
        check_exist(f'{DATA_PATH}/{data}.t.{ext}')

        print(f"Converting {data}.t.{ext} → {data}.t.graph-txt")
        check_exist(f'{DATA_PATH}/{data}.t.{ext}')
        os.system(f"python3 utils/edges2graph-txt.py {DATA_PATH}/{data}.t.{ext} {DATA_PATH}/{data}.t.graph-txt")
        check_exist(f'{DATA_PATH}/{data}.t.graph-txt')
        

        for pardegree in pardegrees :

            if pardegree == 1 :
                
                print(f"Preparing mm-reapir format for {data}")
                check_exist(f'{DATA_PATH}/{data}.mtx.rowm')
                os.system(f"{MMR_ENC} --bool -r {DATA_PATH}/{data}.mtx.rowm {nnodes} {nnodes}")
            
                print(f"Converting {data}.t.graph-txt → {data}.t.zkr-plain")
                check_exist(f'{DATA_PATH}/{data}.t.graph-txt')
                os.system(f"python3 {ZKR_DIR}/gen_graphs/graph-txt2zkr-plain.py {DATA_PATH}/{data}.t.graph-txt {DATA_PATH}/{data}.t.zkr-plain")
                check_exist(f'{DATA_PATH}/{data}.t.zkr-plain')

                print(f"Converting {data}.t.zkr-plain → {data}.t.zkr")
                check_exist(f'{DATA_PATH}/{data}.t.zkr-plain')
                os.system(f"{ZKR_ENC} --input_path {DATA_PATH}/{data}.t.zkr-plain --output_path {DATA_PATH}/{data}.t.zkr")
                check_exist(f'{DATA_PATH}/{data}.t.zkr')

                print(f"Converting {data}.t.graph-txt → {data}.t.kt-plain")
                check_exist(f'{DATA_PATH}/{data}.t.graph-txt')
                os.system(f"python3 {KT_DIR}/gen_graphs/graph-txt2kt-plain.py {DATA_PATH}/{data}.t.graph-txt {DATA_PATH}/{data}.t.kt-plain")
                check_exist(f'{DATA_PATH}/{data}.t.kt-plain')

                print(f"Converting {data}.t.kt-plain → {data}.t.ktrd")
                check_exist(f'{DATA_PATH}/{data}.t.kt-plain')
                os.system(f"{KTRD_ENC} {DATA_PATH}/{data}.t")
                check_exist(f'{DATA_PATH}/{data}.t.ktrd')

            else : # pardegree > 1
                
                print(f"Splitting {data}.t.graph-txt in {pardegree} parts")
                check_exist(f'{DATA_PATH}/{data}.t.graph-txt')
                os.system(f"python3 utils/split_graph-txt.py {DATA_PATH}/{data}.t.graph-txt {pardegree}")
                for tid in range(pardegree) :
                    check_exist(f'{DATA_PATH}/{data}.t.{pardegree}.{tid}.graph-txt')

                print(f"Preparing mm-repair format for {data}")
                check_exist(f'{DATA_PATH}/{data}.mtx.rowm')
                os.system(f"{MMR_ENC} -p {pardegree} -b {pardegree} --bool -r {DATA_PATH}/{data}.mtx.rowm {nnodes} {nnodes}")
                
                for tid in range(pardegree) :
                    
                    print(f"Converting {data}.t.{pardegree}.{tid}.graph-txt → {data}.{pardegree}.{tid}.t.zkr-plain")
                    check_exist(f'{DATA_PATH}/{data}.t.{pardegree}.{tid}.graph-txt')
                    os.system(f"python3 {ZKR_DIR}/gen_graphs/graph-txt2zkr-plain.py {DATA_PATH}/{data}.t.{pardegree}.{tid}.graph-txt {DATA_PATH}/{data}.t.{pardegree}.{tid}.zkr-plain")
                    check_exist(f'{DATA_PATH}/{data}.t.{pardegree}.{tid}.zkr-plain')

                    print(f"Converting {data}.t.{pardegree}.{tid}.zkr-plain → {data}.t.{pardegree}.{tid}.zkr")
                    check_exist(f'{DATA_PATH}/{data}.t.{pardegree}.{tid}.zkr-plain')
                    os.system(f"{ZKR_ENC} --input_path {DATA_PATH}/{data}.t.{pardegree}.{tid}.zkr-plain --output_path {DATA_PATH}/{data}.t.{pardegree}.{tid}.zkr")
                    check_exist(f'{DATA_PATH}/{data}.t.{pardegree}.{tid}.zkr')

                    print(f"Converting {data}.t.{pardegree}.{tid}.graph-txt → {data}.t.{pardegree}.{tid}.kt-plain")
                    check_exist(f'{DATA_PATH}/{data}.t.{pardegree}.{tid}.graph-txt')
                    os.system(f"python3 {KT_DIR}/gen_graphs/graph-txt2kt-plain.py {DATA_PATH}/{data}.t.{pardegree}.{tid}.graph-txt {DATA_PATH}/{data}.t.{pardegree}.{tid}.kt-plain")
                    check_exist(f'{DATA_PATH}/{data}.t.{pardegree}.{tid}.kt-plain')

                    print(f"Converting {data}.t.{pardegree}.{tid}.kt-plain → {data}.t.{pardegree}.{tid}.ktrd")
                    check_exist(f'{DATA_PATH}/{data}.t.{pardegree}.{tid}.kt-plain')
                    os.system(f"{KTRD_ENC} {DATA_PATH}/{data}.t.{pardegree}.{tid}")
                    check_exist(f'{DATA_PATH}/{data}.t.{pardegree}.{tid}.ktrd')


        print(f"Done {data}")
        
if __name__ == '__main__' :
    if len(sys.argv) == 1 :
        print('Usage is:', sys.argv[0], '<par. degree1> ... <par. degreeN>')
        exit(-1)
    pardegrees = [int(sys.argv[i]) for i in range(1, len(sys.argv))]
    main(pardegrees)

import os, sys
from datetime import datetime

BUILD_DIR = "cmake-build-debug"
DATA_PATH = "/data/matrix/mtx"

# plain
PLAIN_PR = f"{BUILD_DIR}/rmult_plain"

# zkr
ZKR_DIR = "zuckerli"
ZKR_BUILD_DIR = f"{BUILD_DIR}/zuckerli"
ZKR_PR = f"{ZKR_BUILD_DIR}/pageranker"
ZKR_PR_PT = f"{ZKR_BUILD_DIR}/pageranker_pthread"

# kt
KT_DIR = 'k2tree_basic_v0.1'
KT_BUILD_DIR = f'{BUILD_DIR}/k2tree_basic_v0.1'
KT_PR = f"{KT_BUILD_DIR}/pagerank"
KT_PR_PT = f"{KT_BUILD_DIR}/pagerank_pthread"
KTRD_PR = f"{KT_BUILD_DIR}/pagerank_rd"
KTRD_PR_PT = f"{KT_BUILD_DIR}/pagerank_pthread_rd"

# ktgn
KTGN_DIR = 'matrix_gn'
KTGN_BUILD_DIR = f'{BUILD_DIR}/{KTGN_DIR}'
KTGN_PR = f'{KTGN_BUILD_DIR}/pagerank_gn'
KTGN_PR_PT = f'{KTGN_BUILD_DIR}/pagerank_gn_pthread'

# mmr
MMR_DIR = 'mm-repair/pagerank'
MMR_PR = 'mm-repair/pagerank/repagerank'

#ls /sys/bus/event_source/devices/power/events
PREAMBLE = "/usr/bin/time -f%e:%M perf stat -a -e L1-dcache-loads,L1-dcache-load-misses,L1-dcache-stores,LLC-loads,LLC-load-misses,LLC-stores,cycles,instructions,power/energy-pkg/,power/energy-ram/ "

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

def check_exist(infilepath):
    if not os.path.exists(infilepath):
        print('File', infilepath, 'does not exist')
        exit(1)
    return

def start_exp(pause=1) :
    os.system(f'sleep {pause}')
    print('\nstart', datetime.now().timestamp(), file=sys.stderr)
    return

verbose = 1
maxiter = 100
dampf = 0.85
topk = 5

def main(pardegrees) :
    t = 't'

    for enc in [ZKR_PR, ZKR_PR_PT, MMR_PR, KT_PR, KT_PR_PT, KTGN_PR, KTGN_PR_PT, KTRD_PR, KTRD_PR_PT] :
        check_exist(enc)
    for data,nnodes in datasets:
        check_exist(f'{DATA_PATH}/{data}.mtx.ccount')
        check_exist(f'{DATA_PATH}/{data}.mtx.rowm')
        for pardegree in pardegrees :
            if pardegree == 1 :
                check_exist(f'{DATA_PATH}/{data}.{t}.zkr')
                check_exist(f'{DATA_PATH}/{data}.{t}.ktrd')
                check_exist(f'{DATA_PATH}/{data}.mtx.rowm.vc')
                check_exist(f'{DATA_PATH}/{data}.mtx.rowm.vc.C')
                check_exist(f'{DATA_PATH}/{data}.mtx.rowm.vc.C.ansf.1')
                check_exist(f'{DATA_PATH}/{data}.mtx.rowm.vc.C.iv')
                check_exist(f'{DATA_PATH}/{data}.mtx.rowm.vc.R')
                check_exist(f'{DATA_PATH}/{data}.mtx.rowm.vc.R.iv')
            else :
                for tid in range(pardegree) :
                    check_exist(f'{DATA_PATH}/{data}.{t}.{pardegree}.{tid}.zkr')
                    check_exist(f'{DATA_PATH}/{data}.{t}.{pardegree}.{tid}.ktrd')
                    check_exist(f'{DATA_PATH}/{data}.mtx.rowm.{pardegree}.{tid}.vc')
                    check_exist(f'{DATA_PATH}/{data}.mtx.rowm.{pardegree}.{tid}.vc.C')
                    check_exist(f'{DATA_PATH}/{data}.mtx.rowm.{pardegree}.{tid}.vc.C.ansf.1')
                    check_exist(f'{DATA_PATH}/{data}.mtx.rowm.{pardegree}.{tid}.vc.C.iv')
                    check_exist(f'{DATA_PATH}/{data}.mtx.rowm.{pardegree}.{tid}.vc.R')
                    check_exist(f'{DATA_PATH}/{data}.mtx.rowm.{pardegree}.{tid}.vc.R.iv')


    for pardegree in pardegrees :
        for data,nnodes in datasets:

            #zuckerli
            start_exp()
            if pardegree==1 :
                os.system(f'{PREAMBLE} {ZKR_PR}    --verbose={verbose} --maxiter={maxiter} --dampf={dampf} --topk={topk} --input_path={DATA_PATH}/{data}.{t}.zkr --ccount_path={DATA_PATH}/{data}.mtx.ccount ')
            else :
                os.system(f'{PREAMBLE} {ZKR_PR_PT} --verbose={verbose} --maxiter={maxiter} --dampf={dampf} --topk={topk} --input_path={DATA_PATH}/{data}.{t}     --ccount_path={DATA_PATH}/{data}.mtx.ccount --pardegree={pardegree} ')

            #k²-tree (UDC) - rank: disabled
            start_exp()
            check_exist(f'{DATA_PATH}/{data}.{t}.ktrd')
            vopt = '-v' if verbose else ''
            if pardegree==1 :
                os.system(f'{PREAMBLE} {KTRD_PR}    {vopt}                -m {maxiter} -d {dampf} -k {topk} {DATA_PATH}/{data}.{t} {DATA_PATH}/{data}.mtx.ccount')
            else :
                os.system(f'{PREAMBLE} {KTRD_PR_PT} {vopt} -b {pardegree} -m {maxiter} -d {dampf} -k {topk} {DATA_PATH}/{data}.{t} {DATA_PATH}/{data}.mtx.ccount')

            """
            #k²-tree (UChile)
            start_exp()
            check_exist(f'{DATA_PATH}/{data}.mtx.1.0.ktgn')
            vopt = '-v' if verbose else ''
            if pardegree==1 :
                os.system(f'{PREAMBLE} {KTGN_PR}    {vopt}                -m {maxiter} -d {dampf} -k {topk} {DATA_PATH}/{data}.mtx ')
            else :
                os.system(f'{PREAMBLE} {KTGN_PR_PT} {vopt} -b {pardegree} -m {maxiter} -d {dampf} -k {topk} {DATA_PATH}/{data}.mtx ')"""

            #mm-repair
            for algo in ['csrv', 're32', 'reiv', 're'] :
                start_exp()
                os.system(f'{PREAMBLE} {MMR_DIR}/{algo}pagerank {vopt} -b {pardegree} -m {maxiter} -d {dampf} -k {topk} {DATA_PATH}/{data}.mtx.rowm {DATA_PATH}/{data}.mtx.ccount')
                
            print('\n\n\n')

    print(f"\nDone {data}")

if __name__ == '__main__' :
    if len(sys.argv) < 2 :
        print('Usage is:', sys.argv[0], '<par. degree1> ... <par. degreeN>')
        exit(-1)
    pardegrees = [int(x) for x in sys.argv[1:]]
    main(pardegrees)

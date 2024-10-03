import os, re, sys

datadir = 'example'  # Path to the current data directory 
logdir = 'example'  # Path to the data directory used when the tests were launched (often the same as data_dir)

builddir = 'build'

re_start = 'start\s+([0-9]+.[0-9]+)'

re_title = '==== Command line:'

re_zkr = f'\s*{builddir}\/zuckerli\/pageranker(_pthread)? --verbose=1 --maxiter=([0-9]+) --dampf=([0-9]+.[0-9]+) --topk=([0-9]+) --input_path={logdir}\/(.+).t(.zkr)? --ccount_path={logdir}\/(.+).mtx.ccount(\s*--pardegree=([0-9]+))?'
re_k2t = f'\s*{builddir}\/k2tree_basic_v0.1\/pagerank(_pthread)? -v( -b ([0-9]+))? -m ([0-9]+) -d ([0-9]+.[0-9]+) -k ([0-9]+) {logdir}\/(.+).t {logdir}\/(.+).mtx.ccount'
re_k2trd = f'\s*{builddir}\/k2tree_basic_v0.1\/pagerank(_pthread)?_rd -v( -b ([0-9]+))? -m ([0-9]+) -d ([0-9]+.[0-9]+) -k ([0-9]+) {logdir}\/(.+).t {logdir}\/(.+).mtx.ccount'
re_k2tgn = f'\s*{builddir}\/matrix_gn\/pagerank_gn(_pthread)? -v( -b ([0-9]+))? -m ([0-9]+) -d ([0-9]+.[0-9]+) -k ([0-9]+) {logdir}\/(.+).mtx'
re_csrv = f'\s*mm-repair\/pagerank\/csrvpagerank -v -b ([0-9]+) -m ([0-9]+) -d ([0-9]+.[0-9]+) -k ([0-9]+) {logdir}\/(.+).mtx.rowm {logdir}\/(.+).mtx.ccount'
re_re32 = f'\s*mm-repair\/pagerank\/re32pagerank -v -b ([0-9]+) -m ([0-9]+) -d ([0-9]+.[0-9]+) -k ([0-9]+) {logdir}\/(.+).mtx.rowm {logdir}\/(.+).mtx.ccount'
re_reiv = f'\s*mm-repair\/pagerank\/reivpagerank -v -b ([0-9]+) -m ([0-9]+) -d ([0-9]+.[0-9]+) -k ([0-9]+) {logdir}\/(.+).mtx.rowm {logdir}\/(.+).mtx.ccount'
re_re = f'\s*mm-repair\/pagerank\/repagerank -v -b ([0-9]+) -m ([0-9]+) -d ([0-9]+.[0-9]+) -k ([0-9]+) {logdir}\/(.+).mtx.rowm {logdir}\/(.+).mtx.ccount'

re_nnodes = 'Number of nodes: ([0-9]+)'
re_ndangling = 'Number of dandling nodes: ([0-9]+)'
re_nedges = 'Number of arcs: ([0-9]+)'
#re_niter = 'Stopped after ([0-9]+) iterations'
re_sum = 'Sum of ranks: ([0-9]+.[0-9]+)'
re_topk = 'Top ([0-9]+) ranks:'

re_numformat = '(\d{1,3}(?:[,\.]?\d{3})*([,\.]?\d+))'
re_l1dcl = f'{re_numformat}\s+L1-dcache-loads'
re_l1dclm = f'{re_numformat}\s+L1-dcache-load-misses'                                       
re_l1dcs = f'{re_numformat}\s+L1-dcache-stores' 
re_llcl = f'{re_numformat}\s+LLC-loads'
re_llclm = f'{re_numformat}\s+LLC-load-misses'                                       
re_llcs = f'{re_numformat}\s+LLC-stores' 
re_cycles = f'{re_numformat}\s+cycles' 
re_instr = f'{re_numformat}\s+instructions' 
re_energy_pkg = f'{re_numformat}\s+Joules power\/energy\-pkg\/'                                           
re_energy_ram = f'{re_numformat}\s+Joules power\/energy\-ram\/'                                           
re_energy_cores = f'{re_numformat}\s+Joules power\/energy\-cores\/'   

re_time = '([0-9]+.[0-9]+):([0-9]+)'

numformatcode = 'usa' #eu or usa

def numformat(n) :
    if numformatcode == 'usa' :
        n = n.replace(',', '')
    elif numformatcode == 'eu' :
        n = n.replace('.', '')
        n = n.replace(',', '.')
    else :
        assert(False)
    return n

def gen_lines(infilepath) :
    infile = open(infilepath, 'r', encoding='latin-1')
    line = infile.readline()
    while line :
        yield line 
        line = infile.readline()
    infile.close()
    return 

def file_size(datadir, filename) :
    return os.path.getsize(f'{datadir}/{filename}')

def main(sep=',') :
    if (len(sys.argv) != 1+1) :
        print('Usage is:', sys.argv[0], '<log file path>')
        exit(-1)

    infilepath = sys.argv[1]
    outfilepath = infilepath[:-4]+'.csv'
    outfile = open(outfilepath, 'w')

    dataset, start, algo, pardegree, maxiter, dampf, topk, nnodes, ndangling, nedges, sum, l1dcl, l1dclm, l1dcs, llcl, llclm, llcs, cycles, instr, energy_pkg, energy_cores, energy_ram, elapsed, pmu, disk = [None for _ in range(25)]

    header = 'DATASET,START,ALGO,PARDEGREE,MAXITER,DAMPF,TOPK,NNODES,NDANGLING,NEDGES,SUM,L1DCL,L1DCLM,L1DCS,LLCL,LLCLM,LLCS,CYCLES,INSTR,ENERGY_PKG,ENERGY_CORES,ENERGY_RAM,ELAPSED,PMU,DISK'

    outfile.write(header)
    outfile.write('\n')

    for line in gen_lines(infilepath) :

        #start
        res = re.search(re_start, line)
        if res :
            print('debug', dataset, pardegree, algo)
            if dataset is not None :
                outfile.write(sep.join([str(x) for x in [dataset, start, algo, pardegree, maxiter, dampf, topk, nnodes, ndangling, nedges, sum, l1dcl, l1dclm, l1dcs, llcl, llclm, llcs, cycles, instr, energy_pkg, energy_cores, energy_ram, elapsed, pmu, disk]]))
                outfile.write('\n')
            dataset, start, algo, pardegree, maxiter, dampf, topk, nnodes, ndangling, nedges, sum, l1dcl, l1dclm, l1dcs, llcl, llclm, llcs, cycles, instr, energy_pkg, energy_cores, energy_ram, elapsed, pmu, disk = [None for _ in range(25)]

            start = res.group(1)

        #title
        res = re.search(re_title, line)
        if res :
            pass
        
        #zuckerli
        res = re.search(re_zkr, line)
        if res :
            algo = 'zkr'
            assert(res.group(1) in ['_pthread', None])
            maxiter = res.group(2)
            dampf = res.group(3)
            topk = res.group(4)
            dataset = res.group(5)
            assert(res.group(6) in ['.zkr', None])
            assert(dataset == res.group(7))
            pardegree = int(res.group(9)) if res.group(8) else 1

            disk = 0
            if pardegree == 1 :
                disk += file_size(datadir, f'{dataset}.t.zkr')
            else :
                for tid in range(pardegree) :
                    disk += file_size(datadir, f'{dataset}.t.{pardegree}.{tid}.zkr')

        #k²-tree (UDC) -- rank: disabled
        res = re.search(re_k2trd, line)
        if res :
            algo = 'k2trd'
            pardegree = int(res.group(3)) if res.group(3) else 1
            maxiter = res.group(4)
            dampf = res.group(5)
            topk = res.group(6)
            dataset = res.group(7)
            assert(dataset == res.group(8))

            disk = 0
            if pardegree == 1 :
                disk += file_size(datadir, f'{dataset}.t.ktrd')
            else :
                for tid in range(pardegree) :
                    disk += file_size(datadir, f'{dataset}.t.{pardegree}.{tid}.ktrd')

        #csrv
        res = re.search(re_csrv, line)
        if res :
            algo = 'csrv'
            pardegree = int(res.group(1))
            maxiter = res.group(2)
            dampf = res.group(3)
            topk = res.group(4)
            dataset = res.group(5)
            assert(dataset == res.group(6))

            disk = 0
            if pardegree == 1 :
                disk += file_size(datadir, f'{dataset}.mtx.rowm.vc')
            else :
                for tid in range(pardegree) :
                    disk += file_size(datadir, f'{dataset}.mtx.rowm.{pardegree}.{tid}.vc')

        #re32
        res = re.search(re_re32, line)
        if res :
            algo = 're32'
            pardegree = int(res.group(1))
            maxiter = res.group(2)
            dampf = res.group(3)
            topk = res.group(4)
            dataset = res.group(5)
            assert(dataset == res.group(6))

            disk = 0
            if pardegree == 1 :
                disk += file_size(datadir, f'{dataset}.mtx.rowm.vc.C')
                disk += file_size(datadir, f'{dataset}.mtx.rowm.vc.R')
            else :
                for tid in range(pardegree) :
                    disk += file_size(datadir, f'{dataset}.mtx.rowm.{pardegree}.{tid}.vc.C')
                    disk += file_size(datadir, f'{dataset}.mtx.rowm.{pardegree}.{tid}.vc.R')

        #reiv
        res = re.search(re_reiv, line)
        if res :
            algo = 'reiv'
            pardegree = int(res.group(1))
            maxiter = res.group(2)
            dampf = res.group(3)
            topk = res.group(4)
            dataset = res.group(5)
            assert(dataset == res.group(6))

            disk = 0
            if pardegree == 1 :
                disk += file_size(datadir, f'{dataset}.mtx.rowm.vc.C.iv')
                disk += file_size(datadir, f'{dataset}.mtx.rowm.vc.R')
            else :
                for tid in range(pardegree) :
                    disk += file_size(datadir, f'{dataset}.mtx.rowm.{pardegree}.{tid}.vc.C.iv')
                    disk += file_size(datadir, f'{dataset}.mtx.rowm.{pardegree}.{tid}.vc.R')

        #re
        res = re.search(re_re, line)
        if res :
            algo = 're'
            pardegree = int(res.group(1))
            maxiter = res.group(2)
            dampf = res.group(3)
            topk = res.group(4)
            dataset = res.group(5)
            assert(dataset == res.group(6))

            disk = 0
            if pardegree == 1 :
                disk += file_size(datadir, f'{dataset}.mtx.rowm.vc.C.ansf.1')
                disk += file_size(datadir, f'{dataset}.mtx.rowm.vc.R')
            else :
                for tid in range(pardegree) :
                    disk += file_size(datadir, f'{dataset}.mtx.rowm.{pardegree}.{tid}.vc.C.ansf.1')
                    disk += file_size(datadir, f'{dataset}.mtx.rowm.{pardegree}.{tid}.vc.R')

        res = re.search(re_nnodes, line)
        if res :
            nnodes = res.group(1)
            
        res = re.search(re_ndangling, line)
        if res :
            ndangling = res.group(1)

        res = re.search(re_nedges, line)
        if res :
            nedges = res.group(1)

        res = re.search(re_sum, line)
        if res :
            sum = res.group(1)

        res = re.search(re_topk, line)
        if res :
            topk = res.group(1)

        res = re.search(re_l1dcl, line)
        if res :
            l1dcl = res.group(1)
            l1dcl = numformat(l1dcl)

        res = re.search(re_l1dclm, line)
        if res :
            l1dclm = res.group(1)
            l1dclm = numformat(l1dclm)

        res = re.search(re_l1dcs, line)
        if res :
            l1dcs = res.group(1)
            l1dcs = numformat(l1dcs)

        res = re.search(re_llcl, line)
        if res :
            llcl = res.group(1)
            llcl = numformat(llcl)

        res = re.search(re_llclm, line)
        if res :
            llclm = res.group(1)
            llclm = numformat(llclm)

        res = re.search(re_llcs, line)
        if res :
            llcs = res.group(1)
            llcs = numformat(llcs)

        res = re.search(re_cycles, line)
        if res :
            cycles = res.group(1)
            cycles = numformat(cycles)

        res = re.search(re_instr, line)
        if res :
            instr = res.group(1)
            instr = numformat(instr)

        res = re.search(re_energy_pkg, line)
        if res :
            energy_pkg = res.group(1)
            energy_pkg = numformat(energy_pkg)

        res = re.search(re_energy_cores, line)
        if res :
            energy_cores = res.group(1)
            energy_cores = numformat(energy_cores)

        res = re.search(re_energy_ram, line)
        if res :
            energy_ram = res.group(1)
            energy_ram  = numformat(energy_ram)

        res = re.search(re_time, line)
        if res :
            elapsed = res.group(1)
            pmu = res.group(2)
            
    #end
    if dataset is not None :
        outfile.write(sep.join([str(x) for x in [dataset, start, algo, pardegree, maxiter, dampf, topk, nnodes, ndangling, nedges, sum, l1dcl, l1dclm, l1dcs, llcl, llclm, llcs, cycles, instr, energy_pkg, energy_cores, energy_ram, elapsed, pmu, disk]]))
        outfile.write('\n')
    return

if __name__ == '__main__' :
    main()

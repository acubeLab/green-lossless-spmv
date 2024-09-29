import sys
from operator import itemgetter
from itertools import groupby

def gen_lines(infilepath) :
    mtx_header = (infilepath.split('.')[-1] == 'mtx')

    infile = open(infilepath, 'r')
    line = infile.readline()
    while line :
        if line.startswith('%'):
            line = infile.readline()
            continue
        if mtx_header :
            mtx_header = False #skip mtx header
            line = infile.readline()
            continue
        assert(line[-1] == '\n')
        yield line[:-1]
        line = infile.readline()
    infile.close()

def max_value(mtxfilepath) :
    infile = open(mtxfilepath, 'r')
    line = infile.readline()
    while line.startswith('%') :
        line = infile.readline()
        assert(line)
    infile.close()

    tokens = line[:-1].split()
    assert(len(tokens) == 3)
    rows,cols,edges = [int(x) for x in tokens]
    assert(rows == cols)
    assert(edges >= 0)
    return rows

def convert_edges_to_graph_text(infilepath, outfilepath):
    nnodes = max_value(infilepath)
    print('#nodes:', nnodes)
        
    adjm = [[] for _ in range(nnodes)]
    for line in gen_lines(infilepath) :
        u, v = map(int, line.strip().split()[:2])
        assert(u>0) #1-based
        assert(v>0) #1-based
        adjm[u-1].append(v-1) #0-based
        #adjm[v-1].append(u-1) #0-based
    #sort
    for adjl in adjm :
        adjl.sort()
    #remove duplicates
    for i,_ in enumerate(adjm) :
    	adjm[i] = list(map(itemgetter(0), groupby(adjm[i])))
     

    with open(outfilepath, 'w') as outfile :
        outfile.write(f'{nnodes}')
        outfile.write('\n')

        for adjl in adjm:
            outfile.write(' '.join(map(str, adjl)))
            outfile.write('\n')
    return

def main() :
    if len(sys.argv) != 2+1 :
        print('Usage is:', sys.argv[0], '<path/to/mat.edges> <path/to/mat.graph-text>')
        exit(-1)
    #args
    infilepath = sys.argv[1]
    suffixes = ['edges', 'mtx']
    if infilepath.split('.')[-1] not in suffixes :
        print('Supported input formats are', ','.join(suffixes))
    outfilepath = sys.argv[2]
    #logic
    convert_edges_to_graph_text(infilepath, outfilepath)

    print('Done.')
    return

if __name__ == '__main__' :
    main()

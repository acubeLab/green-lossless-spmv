import sys 

def fetch_header(infilepath) :
    infile = open(infilepath, 'r')
    line = infile.readline().lstrip()
    while (line.startswith('%')) :
        line = infile.readline().lstrip()
    rows,cols,edges = [int(x) for x in line.split()]
    assert(rows == cols)
    infile.close()
    return rows,cols,edges

def fetch_data(infilepath) :
    infile = open(infilepath, 'r')
    line = infile.readline()
    is_header_found = False
    count = 0
    while line :
        line = line.lstrip()
        if line.startswith('%') :
            pass
        else :
            tokens =  line.split()
            assert(len(tokens) in [2,3])
            if not is_header_found :
                rs, cs, es = [int(x) for x in tokens]
                is_header_found = True 
                assert(rs == cs)
            else :
                r = int(tokens[0])
                c = int(tokens[1])
                yield r,c
                count += 1
        line = infile.readline()
    assert(es == count)
    infile.close()
    return

def main() :
    if len(sys.argv) != 1+1 :
        print('Usage is:', sys.argv[0], '<mtx filepath>')
        exit(0)
    
    #args
    infilepath = sys.argv[1]

    ext = '.mtx'
    assert(infilepath[-len(ext):] == ext)

    #el_filepath = infilepath[:-len(ext)] + '.t'
    t_filepath = infilepath[:-len(ext)] + '.t.mtx'
    #el_file = open(el_filepath, 'w')
    t_file = open(t_filepath, 'w')
    rows,cols,edges = fetch_header(infilepath)
    t_file.write(f'{cols} {rows} {edges}\n')
    edges = [(c,r) for r,c in fetch_data(infilepath)]
    edges.sort()
    for e1,e2 in edges :
        assert(e1)
        assert(e2)
        #el_file.write(f'{e1-1} {e2-1}\n') #0-based
        t_file.write(f'{e1} {e2}\n') #1-based with header
    #el_file.close()
    t_file.close()

if __name__ == '__main__' :
    main()
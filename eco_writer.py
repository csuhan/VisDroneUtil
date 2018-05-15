from optparse import OptionParser
import extractor

### Write SOT annotation for ECO input

def main():
    parser = OptionParser()
    parser.add_option('-i', '--from', action='store', type='string', help='File to read from', dest='from', default='')
    parser.add_option('-o', '--to', action='store', type='string', help='File to write to', dest='to', default='../groundtruth_rect.txt')
    (options, args) = parser.parse_args()
    data = extractor.loadFile(options.from)
    outfile = open(options.to, 'r+')
    for item in data:
        outfile.write(str.join(str(n) for n in item[:4]) + '\n')
    return
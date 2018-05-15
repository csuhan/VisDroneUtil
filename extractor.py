### Read a single annotation file as list

def loadFile(path):
    data = []
    f = open(path, 'r')
    lines = f.readlines
    for line in lines:
        data.append(int(s) for s in line.split(','))
    return data
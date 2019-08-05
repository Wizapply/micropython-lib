import json

boot_count = None

def new_boot(filename='boot_count.dat'):
    global boot_count  #pylint: disable=global-statement

    try:
        with open(filename, 'r') as fread:
            data_j = fread.read()
    except OSError:
        data_j = None

    if data_j is not None:
        try:
            data_d = json.loads(data_j)
        except ValueError:
            data_d = None
    else:
        data_d = None

    if data_d is not None:
        try:
            boot_count = data_d['boot_count']
        except KeyError:
            boot_count = 0
    else:
        boot_count = 0

    try:
        boot_count += 1
    except TypeError:
        boot_count = 1

    data_d = {}
    data_d['boot_count'] = boot_count
    data_j = json.dumps(data_d)
    try:
        with open(filename, 'w') as fwrite:
            fwrite.write(data_j)
    except OSError:
        pass

if __name__ == '__main__':
    new_boot()


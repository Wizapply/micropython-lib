import os

import boot_count

filename = 'test/junk/boot_count_test.dat'
try:
    os.mkdir('test/junk')
except FileExistsError:
    pass


def rm_f(filename):
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass


def test_boot_count_no_file():
    rm_f(filename)
    boot_count.new_boot(filename)
    
    assert(boot_count.boot_count == 1)


def test_boot_count_big_number():
    rm_f(filename)
    with open(filename, 'w') as fw:
        fw.write('{"boot_count": 5000 }')

    boot_count.new_boot(filename)
    assert(boot_count.boot_count == 5001)


def test_boot_count_json_parse_error():
    rm_f(filename)
    with open(filename, 'w') as fw:
        fw.write('["key": value]')

    boot_count.new_boot(filename)
    assert(boot_count.boot_count == 1)


def test_boot_count_key_error():
    rm_f(filename)
    with open(filename, 'w') as fw:
        fw.write('{"unexpected_key": 23}')

    boot_count.new_boot(filename)
    assert(boot_count.boot_count == 1)


def test_boot_count_value_error():
    rm_f(filename)
    with open(filename, 'w') as fw:
        fw.write('{"boot_count": "string_value"}')

    boot_count.new_boot(filename)
    assert(boot_count.boot_count == 1)



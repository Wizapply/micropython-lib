import ulogging
import gc
import micropython
import uos

_logger = ulogging.getLogger('eng.sw.mem')
_logger.setLevel(ulogging.DEBUG)

_mem_used = None
_stack_used = None
_fs_used = None
_counter = 0
def log_mem_usage(_ticks_now):
    #pylint: disable=global-statement
    global _mem_used
    global _stack_used
    global _fs_used
    global _counter

    mem_used = gc.mem_alloc()
    mem_free = gc.mem_free()
    stack_used = micropython.stack_use()
    fs_data = uos.statvfs('/')
    fs_size = fs_data[1] * fs_data[2]   # f_frsize * f_blocks
    fs_avail = fs_data[0] * fs_data[4]  # f_bsize * f_bavail
    fs_used = fs_size - fs_avail

    if mem_used == _mem_used and stack_used == _stack_used and fs_used == _fs_used:
        _counter += 1
        if _counter >= 60:
            _counter = 0
    else:
        _counter = 0

    if _counter == 0:
        _mem_used = mem_used
        _stack_used = stack_used
        _fs_used = fs_used
        _logger.debug("{},{},{},{},{}", mem_used, mem_free, stack_used, fs_used, fs_avail)


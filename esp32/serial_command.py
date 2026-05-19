
import sys
import select
import door_module
_poller = None
_buf    = ""
def init():
    """Đăng ký poll trên sys.stdin (non-blocking)."""
    global _poller
    _poller = select.poll()
    _poller.register(sys.stdin, select.POLLIN)
    print("RESP:READY")
def poll():
    """Gọi định kỳ trong main loop. Không block nếu không có lệnh."""
    global _buf
    if _poller is None:
        return
    while _poller.poll(0):
        try:
            ch = sys.stdin.read(1)
        except Exception:
            return
        if not ch:
            return
        if ch in ("\n", "\r"):
            if _buf:
                _process(_buf.strip())
                _buf = ""
        else:
            _buf += ch
            if len(_buf) > 64:
                _buf = ""
def _process(cmd):
    if cmd == "PING":
        print("RESP:PONG")
    elif cmd == "DOOR_OPEN":
        door_module.door.open()
        print("RESP:OK:open")
    elif cmd == "DOOR_CLOSE":
        door_module.door.close()
        print("RESP:OK:closed")
    elif cmd == "DOOR_STATUS":
        state = "open" if door_module.door.is_open else "closed"
        print("RESP:STATUS:" + state)
    else:
        print("RESP:ERR:unknown")

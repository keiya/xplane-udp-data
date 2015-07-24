import socket
import struct
from contextlib import closing

def main():
    host = '0.0.0.0'
    port = 49003
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM);
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1);
    with closing(sock):
        sock.bind((host,port))
        fixed = struct.Struct('< 5s')
        dataid = struct.Struct('< i')
        data = struct.Struct('< 4x f 4x f 4x f 4x f')
        align = struct.Struct('4x')
        while True:
            sbuf = sock.recv(4096)
            bbuf = bytearray(sbuf)
            read_len = 0

            fields = fixed.unpack_from(bbuf[:5])
            read_len += 5

            if fields[0] != b'DATA@':
                continue

            idx = 0
            while len(bbuf) - read_len > 0:
                if idx > 0:
                    fields = align.unpack_from(bbuf[read_len:])
                idx += 1
                did = dataid.unpack_from(bbuf[read_len:])
                read_len += 4
                print(did)
                fields = data.unpack_from(bbuf[read_len:])
                read_len += 32
                print(fields)
    return

if __name__ == '__main__':
    main()

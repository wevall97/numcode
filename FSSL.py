import asyncio as sa
import os
import struct
import zipfile

SAVE_DIR   = r"C:\FS-All Files"
CHUNK_SIZE = 65536

os.makedirs(SAVE_DIR, exist_ok=True)

async def read_exact(reader: sa.StreamReader, n: int) -> bytes:
    buf = bytearray()
    while len(buf) < n:
        chunk = await reader.read(n - len(buf))
        if not chunk:
            raise ConnectionError("Connection closed before full data received")
        buf.extend(chunk)
    return bytes(buf)

async def h(reader: sa.StreamReader, writer: sa.StreamWriter):
    addr = writer.get_extra_info('peername')
    print(f"[+] Connection from {addr}")

    try:
        writer.write(b'1')
        await writer.drain()

        name_len = struct.unpack('>I', await read_exact(reader, 4))[0]
        if not (1 <= name_len <= 4096):
            raise ValueError(f"Bad filename length: {name_len}")

        filename = (await read_exact(reader, name_len)).decode('utf-8')
        filename = os.path.basename(filename)
        if not filename:
            raise ValueError("Empty filename after sanitization")

        file_size = struct.unpack('>Q', await read_exact(reader, 8))[0]
        print(f"[*] Receiving '{filename}' ({file_size:,} bytes) from {addr}")

        # ── Receive and save ZIP ──────────────────────────────────────────────
        save_path = os.path.join(SAVE_DIR, filename)
        received  = 0

        with open(save_path, 'wb') as f:
            while received < file_size:
                chunk = await reader.read(min(CHUNK_SIZE, file_size - received))
                if not chunk:
                    raise ConnectionError("Connection dropped during transfer")
                f.write(chunk)
                received += len(chunk)

        print(f"[+] Saved '{filename}' ({received:,} bytes)")

        # ── Extract ZIP → folder, then delete ZIP ─────────────────────────────
        if filename.endswith('.zip'):
            folder_name  = filename[:-4]                         # strip .zip
            extract_path = os.path.join(SAVE_DIR, folder_name)
            os.makedirs(extract_path, exist_ok=True)

            with zipfile.ZipFile(save_path, 'r') as zf:
                zf.extractall(extract_path)

            os.remove(save_path)
            print(f"[+] Extracted → '{extract_path}'")

        writer.write(b'OK')
        await writer.drain()

    except Exception as e:
        print(f"[-] Error from {addr}: {e}")
        try:
            writer.write(b'ERR')
            await writer.drain()
        except Exception:
            pass

    finally:
        writer.close()
        await writer.wait_closed()

async def m():
    server = await sa.start_server(h, '0.0.0.0', 9992)
    print("[*] FS File Server listening on 0.0.0.0:9992")
    async with server:
        await server.serve_forever()

sa.run(m())
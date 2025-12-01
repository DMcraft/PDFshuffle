#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import time


class BWESCLHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def do_GET(self):
        print(f"GET {self.path}")

        if self.path == '/eSCL/ScannerCapabilities':
            # Указываем только BlackWhite1
            xml = '''<?xml version="1.0" encoding="UTF-8"?>
<scan:ScannerCapabilities xmlns:scan="http://schemas.hp.com/imaging/escl/2011/05/03" xmlns:pwg="http://www.pwg.org/schemas/2010/12/sm">
<scan:Platen>
<scan:PlatenInputCaps>
<pwg:MaxScanRegions>1</pwg:MaxScanRegions>
<pwg:MaxWidth>2550</pwg:MaxWidth>
<pwg:MaxHeight>3500</pwg:MaxHeight>
<pwg:MinWidth>10</pwg:MinWidth>
<pwg:MinHeight>10</pwg:MinHeight>
<pwg:MaxOpticalXResolution>300</pwg:MaxOpticalXResolution>
<pwg:MaxOpticalYResolution>300</pwg:MaxOpticalYResolution>
<pwg:SettingProfiles>
<pwg:SettingProfile>
<pwg:ColorModes>BlackWhite1</pwg:ColorModes>
<pwg:SupportedResolutions>150</pwg:SupportedResolutions>
<pwg:DocumentFormats>image/x-portable-bitmap</pwg:DocumentFormats>
</pwg:SettingProfile>
</pwg:SettingProfiles>
</scan:PlatenInputCaps>
</scan:Platen>
</scan:ScannerCapabilities>'''

            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/xml\r\n"
                f"Content-Length: {len(xml)}\r\n"
                "Connection: keep-alive\r\n"
                "\r\n"
                f"{xml}"
            )

            print(f"✓ Sending ScannerCapabilities with BlackWhite1 only")
            self.wfile.write(response.encode())
            self.wfile.flush()

        elif self.path == '/eSCL/ScannerStatus':
            xml = '''<?xml version="1.0" encoding="UTF-8"?>
<scan:ScannerStatus xmlns:scan="http://schemas.hp.com/imaging/escl/2011/05/03">
<scan:State>Idle</scan:State>
</scan:ScannerStatus>'''

            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/xml\r\n"
                f"Content-Length: {len(xml)}\r\n"
                "Connection: keep-alive\r\n"
                "\r\n"
                f"{xml}"
            )

            self.wfile.write(response.encode())
            self.wfile.flush()
            print("✓ Sent ScannerStatus")

        elif self.path.startswith('/eSCL/ScanJobs/'):
            # Создаем простое PBM изображение (BlackWhite1)
            width, height = 100, 100
            pbm_header = f"P4\n{width} {height}\n".encode()

            # Создаем изображение: каждый бит представляет пиксель (0 - черный, 1 - белый)
            # Мы создадим шаблон шахматной доски
            pbm_data = bytearray()
            for y in range(height):
                for x in range(0, width, 8):
                    byte = 0
                    for bit in range(8):
                        if (x + bit < width) and ((x + bit + y) % 16 < 8):
                            byte |= (1 << (7 - bit))
                    pbm_data.append(byte)

            pbm_image = pbm_header + pbm_data

            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: image/x-portable-bitmap\r\n"
                f"Content-Length: {len(pbm_image)}\r\n"
                "Connection: keep-alive\r\n"
                "\r\n"
            )

            self.wfile.write(response.encode())
            self.wfile.write(pbm_image)
            self.wfile.flush()
            print(f"✓ Sent PBM image: {width}x{height}, {len(pbm_image)} bytes")

        else:
            self.send_error(404)

    def do_POST(self):
        print(f"POST {self.path}")

        if self.path == '/eSCL/ScanJobs':
            response_json = '{"JobId":"test123"}'

            response = (
                "HTTP/1.1 201 Created\r\n"
                "Location: http://127.0.0.1:8080/eSCL/ScanJobs/test123\r\n"
                "Content-Type: application/json\r\n"
                f"Content-Length: {len(response_json)}\r\n"
                "Connection: keep-alive\r\n"
                "\r\n"
                f"{response_json}"
            )

            self.wfile.write(response.encode())
            self.wfile.flush()
            print("✓ Created scan job")
        else:
            self.send_error(404)


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080

    print("🚀 Запуск BlackWhite eSCL эмулятора")
    print(f"📡 Адрес: http://{host}:{port}")
    print("🎯 Только BlackWhite1 и PBM формат")

    server = HTTPServer((host, port), BWESCLHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️ Сервер остановлен")

import os
import sys
import ssl
import cgi
import html
import socket
import pathlib
import http.client
import urllib.parse
from io import BytesIO
from http import HTTPStatus
from threading import Thread

__version__ = "0.0.1"

__all__ = ["http_server", "https_server"]

HTTP_STATUSES = list(HTTPStatus)
ALLOWED_CONTENT_METHODS = ["POST", "PUT", "DELETE"]
ALLOWED_REQUEST_METHODS = ["GET", "HEAD", "POST", "PUT",
                           "DELETE", "CONNECT", "OPTIONS"]
# defaults
DEFAULT_ERROR_MESSAGE = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n<html>\n\t<head>\n\t\t<title>Error {}</title>\n\t</head>\n\t<body>\n\t\t<center>\n\t\t\t<h1>{}</h1>\n\t\t</center>\n\t\t<hr>\n\t\t<center>\n\t\t\t{}\n\t\t</center>\n\t</body>\n</html>"""
DEFAULT_CONTENT_TYPE = "text/html;charset=utf-8"
DEFAULT_REQUEST_PROTOCOL = "HTTP/1.1"

MIME_TYPES = {".3dm": "x-world/x-3dmf", ".3dmf": "x-world/x-3dmf", ".a": "application/octet-stream", ".aab": "application/x-authorware-bin", ".aam": "application/x-authorware-map", ".aas": "application/x-authorware-seg", ".abc": "text/vnd.abc", ".acgi": "text/html", ".afl": "video/animaflex", ".ai": "application/postscript", ".aif": "audio/x-aiff", ".aifc": "audio/x-aiff", ".aiff": "audio/x-aiff", ".aim": "application/x-aim", ".aip": "text/x-audiosoft-intra", ".ani": "application/x-navi-animation", ".aos": "application/x-nokia-9000-communicator-add-on-software", ".aps": "application/mime", ".arc": "application/octet-stream", ".arj": "application/octet-stream", ".art": "image/x-jg", ".asf": "video/x-ms-asf", ".asm": "text/x-asm", ".asp": "text/asp", ".asx": "video/x-ms-asf-plugin", ".au": "audio/x-au", ".avi": "video/x-msvideo", ".avs": "video/avs-video", ".bcpio": "application/x-bcpio", ".bin": "application/x-macbinary", ".bm": "image/bmp", ".bmp": "image/x-windows-bmp", ".boo": "application/book", ".book": "application/book", ".boz": "application/x-bzip2", ".bsh": "application/x-bsh", ".bz": "application/x-bzip", ".bz2": "application/x-bzip2", ".c": "text/x-c", ".c++": "text/plain", ".cat": "application/vnd.ms-pki.seccat", ".cc": "text/x-c", ".ccad": "application/clariscad", ".cco": "application/x-cocoa", ".cdf": "application/x-netcdf", ".cer": "application/x-x509-ca-cert", ".cha": "application/x-chat", ".chat": "application/x-chat", ".class": "application/x-java-class", ".com": "text/plain", ".conf": "text/plain", ".cpio": "application/x-cpio", ".cpp": "text/x-c", ".cpt": "application/x-cpt", ".crl": "application/pkix-crl", ".crt": "application/x-x509-user-cert", ".csh": "text/x-script.csh", ".css": "text/css", ".cxx": "text/plain", ".dcr": "application/x-director", ".deepv": "application/x-deepv", ".def": "text/plain", ".der": "application/x-x509-ca-cert", ".dif": "video/x-dv", ".dir": "application/x-director", ".dl": "video/x-dl", ".doc": "application/msword", ".dot": "application/msword", ".dp": "application/commonground", ".drw": "application/drafting", ".dump": "application/octet-stream", ".dv": "video/x-dv", ".dvi": "application/x-dvi", ".dwf": "model/vnd.dwf", ".dwg": "image/x-dwg", ".dxf": "image/x-dwg", ".dxr": "application/x-director", ".el": "text/x-script.elisp", ".elc": "application/x-elc", ".env": "application/x-envoy", ".eps": "application/postscript", ".es": "application/x-esrehber", ".etx": "text/x-setext", ".evy": "application/x-envoy", ".exe": "application/octet-stream", ".f": "text/x-fortran", ".f77": "text/x-fortran", ".f90": "text/x-fortran", ".fdf": "application/vnd.fdf", ".fif": "image/fif", ".fli": "video/x-fli", ".flo": "image/florian", ".flx": "text/vnd.fmi.flexstor", ".fmf": "video/x-atomic3d-feature", ".for": "text/x-fortran", ".fpx": "image/vnd.net-fpx", ".frl": "application/freeloader", ".funk": "audio/make", ".g": "text/plain", ".g3": "image/g3fax", ".gif": "image/gif", ".gl": "video/x-gl", ".gsd": "audio/x-gsm", ".gsm": "audio/x-gsm", ".gsp": "application/x-gsp", ".gss": "application/x-gss", ".gtar": "application/x-gtar", ".gz": "application/x-gzip", ".gzip": "multipart/x-gzip", ".h": "text/x-h", ".hdf": "application/x-hdf", ".help": "application/x-helpfile", ".hgl": "application/vnd.hp-hpgl", ".hh": "text/x-h", ".hlb": "text/x-script", ".hlp": "application/x-winhelp", ".hpg": "application/vnd.hp-hpgl", ".hpgl": "application/vnd.hp-hpgl", ".hqx": "application/x-mac-binhex40", ".hta": "application/hta", ".htc": "text/x-component", ".htm": "text/html", ".html": "text/html", ".htmls": "text/html", ".htt": "text/webviewhtml", ".htx": "text/html", ".ice": "x-conference/x-cooltalk", ".ico": "image/x-icon", ".idc": "text/plain", ".ief": "image/ief", ".iefs": "image/ief", ".iges": "model/iges", ".igs": "model/iges", ".ima": "application/x-ima", ".imap": "application/x-httpd-imap", ".inf": "application/inf", ".ins": "application/x-internett-signup", ".ip": "application/x-ip2", ".isu": "video/x-isvideo", ".it": "audio/it", ".iv": "application/x-inventor", ".ivr": "i-world/i-vrml", ".ivy": "application/x-livescreen", ".jam": "audio/x-jam", ".jav": "text/x-java-source", ".java": "text/x-java-source", ".jcm": "application/x-java-commerce", ".jfif": "image/pjpeg", ".jfif-tbnl": "image/jpeg", ".jpe": "image/pjpeg", ".jpeg": "image/pjpeg", ".jpg": "image/pjpeg", ".jps": "image/x-jps", ".js": "application/x-javascript", ".jut": "image/jutvision", ".kar": "music/x-karaoke", ".ksh": "text/x-script.ksh", ".la": "audio/x-nspaudio", ".lam": "audio/x-liveaudio", ".latex": "application/x-latex", ".lha": "application/x-lha", ".lhx": "application/octet-stream", ".list": "text/plain", ".lma": "audio/x-nspaudio", ".log": "text/plain", ".lsp": "text/x-script.lisp", ".lst": "text/plain", ".lsx": "text/x-la-asf", ".ltx": "application/x-latex", ".lzh": "application/x-lzh", ".lzx": "application/x-lzx", ".m": "text/x-m", ".m1v": "video/mpeg", ".m2a": "audio/mpeg", ".m2v": "video/mpeg", ".m3u": "audio/x-mpequrl", ".man": "application/x-troff-man", ".map": "application/x-navimap", ".mar": "text/plain", ".mbd": "application/mbedlet", ".mc$": "application/x-magic-cap-package-1.0", ".mcd": "application/x-mathcad", ".mcf": "text/mcf", ".mcp": "application/netmc", ".me": "application/x-troff-me", ".mht": "message/rfc822", ".mhtml": "message/rfc822", ".mid": "x-music/x-midi", ".midi": "x-music/x-midi", ".mif": "application/x-mif", ".mime": "www/mime", ".mjf": "audio/x-vnd.audioexplosion.mjuicemediafile", ".mjpg": "video/x-motion-jpeg", ".mm": "application/x-meme", ".mme": "application/base64", ".mod": "audio/x-mod", ".moov": "video/quicktime", ".mov": "video/quicktime", ".movie": "video/x-sgi-movie", ".mp2": "video/x-mpeq2a", ".mp3": "video/x-mpeg", ".mpa": "video/mpeg", ".mpc": "application/x-project", ".mpe": "video/mpeg", ".mpeg": "video/mpeg", ".mpg": "video/mpeg", ".mpga": "audio/mpeg", ".mpp": "application/vnd.ms-project", ".mpt": "application/x-project", ".mpv": "application/x-project", ".mpx": "application/x-project", ".mrc": "application/marc", ".ms": "application/x-troff-ms", ".mv": "video/x-sgi-movie", ".my": "audio/make", ".mzz": "application/x-vnd.audioexplosion.mzz", ".nap": "image/naplps", ".naplps": "image/naplps", ".nc": "application/x-netcdf", ".ncm": "application/vnd.nokia.configuration-message", ".nif": "image/x-niff", ".niff": "image/x-niff", ".nix": "application/x-mix-transfer", ".nsc": "application/x-conference", ".nvd": "application/x-navidoc", ".o": "application/octet-stream", ".oda": "application/oda", ".omc": "application/x-omc", ".omcd": "application/x-omcdatamaker", ".omcr": "application/x-omcregerator",
              ".p": "text/x-pascal", ".p10": "application/x-pkcs10", ".p12": "application/x-pkcs12", ".p7a": "application/x-pkcs7-signature", ".p7c": "application/x-pkcs7-mime", ".p7m": "application/x-pkcs7-mime", ".p7r": "application/x-pkcs7-certreqresp", ".p7s": "application/pkcs7-signature", ".part": "application/pro_eng", ".pas": "text/pascal", ".pbm": "image/x-portable-bitmap", ".pcl": "application/x-pcl", ".pct": "image/x-pict", ".pcx": "image/x-pcx", ".pdb": "chemical/x-pdb", ".pdf": "application/pdf", ".pfunk": "audio/make.my.funk", ".pgm": "image/x-portable-greymap", ".pic": "image/pict", ".pict": "image/pict", ".pkg": "application/x-newton-compatible-pkg", ".pko": "application/vnd.ms-pki.pko", ".pl": "text/x-script.perl", ".plx": "application/x-pixclscript", ".pm": "text/x-script.perl-module", ".pm4": "application/x-pagemaker", ".pm5": "application/x-pagemaker", ".png": "image/png", ".pnm": "image/x-portable-anymap", ".pot": "application/vnd.ms-powerpoint", ".pov": "model/x-pov", ".ppa": "application/vnd.ms-powerpoint", ".ppm": "image/x-portable-pixmap", ".pps": "application/vnd.ms-powerpoint", ".ppt": "application/x-mspowerpoint", ".ppz": "application/mspowerpoint", ".pre": "application/x-freelance", ".prt": "application/pro_eng", ".ps": "application/postscript", ".psd": "application/octet-stream", ".pvu": "paleovu/x-pv", ".pwz": "application/vnd.ms-powerpoint", ".py": "text/x-script.phyton", ".pyc": "applicaiton/x-bytecode.python", ".qcp": "audio/vnd.qcelp", ".qd3": "x-world/x-3dmf", ".qd3d": "x-world/x-3dmf", ".qif": "image/x-quicktime", ".qt": "video/quicktime", ".qtc": "video/x-qtc", ".qti": "image/x-quicktime", ".qtif": "image/x-quicktime", ".ra": "audio/x-realaudio", ".ram": "audio/x-pn-realaudio", ".ras": "image/x-cmu-raster", ".rast": "image/cmu-raster", ".rexx": "text/x-script.rexx", ".rf": "image/vnd.rn-realflash", ".rgb": "image/x-rgb", ".rm": "audio/x-pn-realaudio", ".rmi": "audio/mid", ".rmm": "audio/x-pn-realaudio", ".rmp": "audio/x-pn-realaudio-plugin", ".rng": "application/vnd.nokia.ringing-tone", ".rnx": "application/vnd.rn-realplayer", ".roff": "application/x-troff", ".rp": "image/vnd.rn-realpix", ".rpm": "audio/x-pn-realaudio-plugin", ".rt": "text/vnd.rn-realtext", ".rtf": "text/richtext", ".rtx": "text/richtext", ".rv": "video/vnd.rn-realvideo", ".s": "text/x-asm", ".s3m": "audio/s3m", ".saveme": "application/octet-stream", ".sbk": "application/x-tbook", ".scm": "video/x-scm", ".sdml": "text/plain", ".sdp": "application/x-sdp", ".sdr": "application/sounder", ".sea": "application/x-sea", ".set": "application/set", ".sgm": "text/x-sgml", ".sgml": "text/x-sgml", ".sh": "text/x-script.sh", ".shar": "application/x-shar", ".shtml": "text/x-server-parsed-html", ".sid": "audio/x-psid", ".sit": "application/x-stuffit", ".skd": "application/x-koan", ".skm": "application/x-koan", ".skp": "application/x-koan", ".skt": "application/x-koan", ".sl": "application/x-seelogo", ".smi": "application/smil", ".smil": "application/smil", ".snd": "audio/x-adpcm", ".sol": "application/solids", ".spc": "text/x-speech", ".spl": "application/futuresplash", ".spr": "application/x-sprite", ".sprite": "application/x-sprite", ".src": "application/x-wais-source", ".ssi": "text/x-server-parsed-html", ".ssm": "application/streamingmedia", ".sst": "application/vnd.ms-pki.certstore", ".step": "application/step", ".stl": "application/x-navistyle", ".stp": "application/step", ".sv4cpio": "application/x-sv4cpio", ".sv4crc": "application/x-sv4crc", ".svf": "image/x-dwg", ".svr": "x-world/x-svr", ".swf": "application/x-shockwave-flash", ".t": "application/x-troff", ".talk": "text/x-speech", ".tar": "application/x-tar", ".tbk": "application/x-tbook", ".tcl": "text/x-script.tcl", ".tcsh": "text/x-script.tcsh", ".tex": "application/x-tex", ".texi": "application/x-texinfo", ".texinfo": "application/x-texinfo", ".text": "text/plain", ".tgz": "application/x-compressed", ".tif": "image/x-tiff", ".tiff": "image/x-tiff", ".tr": "application/x-troff", ".tsi": "audio/tsp-audio", ".tsp": "audio/tsplayer", ".tsv": "text/tab-separated-values", ".turbot": "image/florian", ".txt": "text/plain", ".uil": "text/x-uil", ".uni": "text/uri-list", ".unis": "text/uri-list", ".unv": "application/i-deas", ".uri": "text/uri-list", ".uris": "text/uri-list", ".ustar": "multipart/x-ustar", ".uu": "text/x-uuencode", ".uue": "text/x-uuencode", ".vcd": "application/x-cdlink", ".vcs": "text/x-vcalendar", ".vda": "application/vda", ".vdo": "video/vdo", ".vew": "application/groupwise", ".viv": "video/vnd.vivo", ".vivo": "video/vnd.vivo", ".vmd": "application/vocaltec-media-desc", ".vmf": "application/vocaltec-media-file", ".voc": "audio/x-voc", ".vos": "video/vosaic", ".vox": "audio/voxware", ".vqe": "audio/x-twinvq-plugin", ".vqf": "audio/x-twinvq", ".vql": "audio/x-twinvq-plugin", ".vrml": "x-world/x-vrml", ".vrt": "x-world/x-vrt", ".vsd": "application/x-visio", ".vst": "application/x-visio", ".vsw": "application/x-visio", ".w60": "application/wordperfect6.0", ".w61": "application/wordperfect6.1", ".w6w": "application/msword", ".wav": "audio/x-wav", ".wb1": "application/x-qpro", ".wbmp": "image/vnd.wap.wbmp", ".web": "application/vnd.xara", ".wiz": "application/msword", ".wk1": "application/x-123", ".wmf": "windows/metafile", ".wml": "text/vnd.wap.wml", ".wmlc": "application/vnd.wap.wmlc", ".wmls": "text/vnd.wap.wmlscript", ".wmlsc": "application/vnd.wap.wmlscriptc", ".word": "application/msword", ".wp": "application/wordperfect", ".wp5": "application/wordperfect6.0", ".wp6": "application/wordperfect", ".wpd": "application/x-wpwin", ".wq1": "application/x-lotus", ".wri": "application/x-wri", ".wrl": "x-world/x-vrml", ".wrz": "x-world/x-vrml", ".wsc": "text/scriplet", ".wsrc": "application/x-wais-source", ".wtk": "application/x-wintalk", ".xbm": "image/xbm", ".xdr": "video/x-amt-demorun", ".xgz": "xgl/drawing", ".xif": "image/vnd.xiff", ".xl": "application/excel", ".xla": "application/x-msexcel", ".xlb": "application/x-excel", ".xlc": "application/x-excel", ".xld": "application/x-excel", ".xlk": "application/x-excel", ".xll": "application/x-excel", ".xlm": "application/x-excel", ".xls": "application/x-msexcel", ".xlt": "application/x-excel", ".xlv": "application/x-excel", ".xlw": "application/x-msexcel", ".xm": "audio/xm", ".xml": "text/xml", ".xmz": "xgl/movie", ".xpix": "application/x-vnd.ls-xpix", ".xpm": "image/xpm", ".x-png": "image/png", ".xsr": "video/x-amt-showrun", ".xwd": "image/x-xwindowdump", ".xyz": "chemical/x-pdb", ".z": "application/x-compressed", ".zip": "multipart/x-zip", ".zoo": "application/octet-stream", ".zsh": "text/x-script.zsh"}


class _request:
    def __init__(self, client_connection) -> None:
        self.request = BytesIO(client_connection.recv(1024))
        self.parsed = False

    def parse(self):
        if self.parsed:
            return None
        try:
            raw_requestline = self.request.readline(65537)
            if len(raw_requestline) > 65536:
                return HTTPStatus.REQUEST_URI_TOO_LONG
            if not raw_requestline:
                return HTTPStatus.BAD_REQUEST
        except TimeoutError:
            return HTTPStatus.REQUEST_TIMEOUT

        # parse and validate the start line of request
        requestline = str(raw_requestline, 'iso-8859-1')
        words = requestline.rstrip('\r\n').split()
        if len(words) >= 3:
            # needed * method, path, http version
            method = words[0]
            parsed = urllib.parse.urlparse(words[1])
            path = parsed.path
            query = urllib.parse.parse_qs(parsed.query)
            incoming_version = words[-1]  # eg, HTTP/1.1
            content = None  # form content
            try:
                if not incoming_version.startswith('HTTP/'):
                    raise ValueError
                if method not in ALLOWED_REQUEST_METHODS:
                    raise ValueError
                if not path.startswith("/"):
                    raise ValueError
                version_number = incoming_version.split("/")[1].split(".")
                if len(version_number) != 2:
                    raise ValueError
                version_number = int(version_number[0]), int(version_number[1])
            except (ValueError, IndexError):
                # quick error
                return HTTPStatus.BAD_REQUEST

            # default error true if no error it will be changed to false
            http_version_error = True
            # check http version type
            if version_number >= (1, 1) and incoming_version >= "HTTP/1.1":
                http_version_error = False
            if version_number >= (2, 0):
                http_version_error = True
            if http_version_error:
                return HTTPStatus.HTTP_VERSION_NOT_SUPPORTED

        # starting line does not include method, path, http version
        if not len(words) >= 3:
            return HTTPStatus.BAD_REQUEST

        # parse the headers of the request
        try:
            headers = dict(http.client.parse_headers(
                self.request, _class=http.client.HTTPMessage).items())
        except http.client.HTTPException:
            return HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE
        except http.client.LineTooLong:
            return HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE

        # parse formdata and other content bodies from request
        try:
            if "Content-Length" and "Content-Type" in headers and method in ALLOWED_CONTENT_METHODS:
                datatype, boundary = cgi.parse_header(headers["Content-Type"])
                content_length = int(headers["Content-Length"])

                # max length is 2gb
                if content_length > 2147483647:
                    return HTTPStatus.REQUEST_ENTITY_TOO_LARGE

                for i in boundary:
                    boundary[i] = boundary[i].encode()

                if datatype == "multipart/form-data":
                    content = cgi.parse_multipart(self.request, boundary)
                elif datatype == "application/x-www-form-urlencoded":
                    content = urllib.parse.parse_qs(
                        self.request.read(content_length), keep_blank_values=1)
                    content = {key.decode(): val[0].decode()
                               for key, val in content.items()}
                else:
                    return HTTPStatus.UNSUPPORTED_MEDIA_TYPE

        except Exception as e:
            print(e)
            return HTTPStatus.UNSUPPORTED_MEDIA_TYPE

        # basic parsing (successful)
        self.headers = headers
        self.body = content
        self.path = path
        self.query = query
        self.http_version = version_number
        self.method = method
        self.host = self.get_header("Host").split(":")[0]
        self.parsed = True
        return True

    def get_header(self, headername, err=None):
        if not headername in self.headers:
            return err
        return self.headers[headername]


class _response:
    def __init__(self, client_connection) -> None:
        self.client_connection = client_connection
        self.headers = {
            'Content-type': DEFAULT_CONTENT_TYPE,
            'cache-control': 'no-cache, no-store, max-age=0'
        }
        self.protocol = DEFAULT_REQUEST_PROTOCOL
        self.status = 200
        self.content = []

    def set_header(self, headername, value):
        self.headers.update({headername: value})

    def write_head(self, x, y=None) -> None:
        headers = x if type(x) == dict else y
        status = x if type(x) == int else y
        if headers:
            self.headers.update(headers)
        if status:
            self.status = status

    def write(self, content) -> None:
        if not type(content) == bytes:
            content = content.encode()
        self.content.append(content)

    def serve_file(self, filename) -> None:
        suffix = pathlib.Path(filename).suffix
        mime = MIME_TYPES[suffix] if suffix in MIME_TYPES else "text/plain"

        with open(filename, "rb") as r:
            self.content.append(r.read())

    def raw_response(self):
        # get status
        statusphrase = HTTP_STATUSES[HTTP_STATUSES.index(self.status)].phrase
        # get content
        content = b''.join(self.content)
        self.set_header("Content-Length", str(len(content)))
        # get headers
        raw_headers = []
        for i in self.headers.keys():
            raw_headers.append(f"{i}: {self.headers[i]}".encode())
        raw_response = [
            f"{self.protocol} {self.status} {statusphrase}\r\n".encode(),
            b'\n'.join(raw_headers),
            b'\r\n\r\n',
            content]
        return raw_response

    def end(self):
        raw_response = self.raw_response()
        self.client_connection.sendall(b''.join(raw_response))
        self.client_connection.close()

    def send_error(self, error: int) -> None:
        if not isinstance(error, int):
            raise TypeError(f"error required int, not {type(error)}")
        error = HTTP_STATUSES[HTTP_STATUSES.index(error)]
        self.write(DEFAULT_ERROR_MESSAGE.format(error.value, html.escape(
            error.phrase), html.escape(error.description)))
        self.write_head({"Content-type": DEFAULT_CONTENT_TYPE}, error.value)
        self.end()
        return None


class http_server:
    def __init__(self, keyfile="", certfile="") -> None:
        self.__routers = {}

        try:
            self.is_https
        except:
            self.server_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            server_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)

            self.server_socket = ssl.wrap_socket(
                server_socket, keyfile=keyfile, certfile=certfile, server_side=True, ssl_version=ssl.PROTOCOL_TLSv1_2, ca_certs=None, do_handshake_on_connect=True, suppress_ragged_eofs=True, ciphers='ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!3DES:!MD5:!PSK')

    def add(self, handlerfunc, host="*", path="*") -> None:
        d = {path: handlerfunc}
        if host in self.__routers:
            self.__routers[host].update(d)
        else:
            self.__routers[host] = d

    def serve_static(self, foldername):
        if not os.path.exists(foldername):
            raise FileNotFoundError

        def static_servers(request, response):
            url = request.path[1:]
            contentlocation = os.path.join(foldername, url)
            if os.path.exists(contentlocation) and os.path.isfile(contentlocation):
                response.serve_file(contentlocation)
                response.end()
            elif os.path.exists(contentlocation) and os.path.isdir(contentlocation):
                filenames = next(os.walk(contentlocation), (None, None, []))[2]
                for i in filenames:
                    if "index" in i:
                        response.serve_file(os.path.join(contentlocation, i))
                        response.end()
                        break
            else:
                response.send_error(HTTPStatus.NOT_FOUND.value)

        return static_servers

    def __pick_router(self, host, path):
        if host in self.__routers:
            pathfound = None
            for i in self.__routers[host]:
                if path.startswith(i):
                    pathfound = i
                    break

            if pathfound:
                return self.__routers[host][pathfound]
            elif "*" in self.__routers[host]:
                return self.__routers[host]["*"]

    def __callback(self, client_connection, client_address) -> None:
        request = _request(client_connection)
        response = _response(client_connection)
        parse_result = request.parse()
        # !error parsing!, send error and return
        if parse_result != True:
            return response.send_error(parse_result)

        host = request.host
        path = request.path
        # direct request to proper router

        specific = self.__pick_router(host, path)
        all = self.__pick_router("*", path)

        if specific:
            return specific(request, response)
        elif all:
            return all(request, response)

        return response.send_error(HTTPStatus.NOT_FOUND.value)

    def listen(self, port=8000, ip='127.0.0.1', wait=False) -> None:
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((ip, port))

        try:
            # create the server socket
            self.server_socket.listen(1)
            # on each client connection
            while True:
                try:
                    client_connection, client_address = self.server_socket.accept()
                    Thread(target=self.__callback, args=[
                        client_connection, client_address], daemon=True).start()
                except ssl.SSLError:
                    pass
        except KeyboardInterrupt:
            self.server_socket.close()


class https_server(http_server):
    is_https = True

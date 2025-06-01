#!/usr/bin/env python
# /// script
# dependencies = [
#   "cryptography",
# ]
# ///

import os
import argparse
import datetime
import socket
import ssl
import logging
import tempfile
import io
import mimetypes
import urllib.parse
import email.utils  # For parsing If-Modified-Since

from http import HTTPStatus, server
from pathlib import Path
from typing import Any, Callable, Optional, Tuple, BinaryIO, Dict, Union

from cryptography import x509
from cryptography.x509 import SubjectKeyIdentifier, AuthorityKeyIdentifier
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

ServerAddress = Tuple[str, int]

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def generate_self_signed_certificate(hostname: str) -> Dict[str, str]:
    """Generates a self-signed certificate and private key for the given hostname."""
    logger.info(f"Generating self-signed certificate for: {hostname}")

    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    public_key = private_key.public_key()

    subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, hostname)])

    builder = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(public_key)
        .serial_number(x509.random_serial_number())
        .not_valid_before(
            datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
        )
        .not_valid_after(
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
        )
        .add_extension(x509.SubjectAlternativeName([x509.DNSName(hostname)]), critical=False)
        .add_extension(SubjectKeyIdentifier.from_public_key(public_key), critical=False)
        .add_extension(
            AuthorityKeyIdentifier.from_issuer_public_key(public_key), critical=False
        )
        .add_extension(
            x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]),
            critical=True,
        )
    )
    certificate = builder.sign(private_key, hashes.SHA256(), default_backend())

    return {
        "key": private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode("utf-8"),
        "cert": certificate.public_bytes(serialization.Encoding.PEM).decode("utf-8"),
    }


class CustomHTTPRequestHandler(server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"  # Explicitly set HTTP/1.1

    # Ensure .wasm and .js MIME types are correctly registered
    if ".wasm" not in mimetypes.types_map:
        mimetypes.add_type("application/wasm", ".wasm")
    # Ensure .js is application/javascript
    mimetypes.add_type("application/javascript", ".js", strict=True)

    def __init__(
        self,
        request: socket.socket,
        client_address: ServerAddress,
        srv: server.ThreadingHTTPServer,
        *,
        directory: Optional[Union[str, Path]] = None,
    ) -> None:
        super().__init__(
            request, client_address, srv, directory=str(directory) if directory else None
        )

    def end_headers(self) -> None:
        """Send additional headers for WASM compatibility and security."""
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        super().end_headers()

    def send_head(self) -> Optional[BinaryIO]:
        """
        Common header sending logic.
        This version handles COOP/COEP and correct MIME types. No Gzip.
        Returns a file-like object (BytesIO or original file) or None.
        """
        translated_path_str = self.translate_path(self.path)
        if translated_path_str is None:
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Path translation failed")
            return None
        current_path: Path = Path(translated_path_str)

        f: Optional[BinaryIO] = None

        if current_path.is_dir():
            parts = urllib.parse.urlsplit(self.path)
            if not parts.path.endswith("/"):
                self.send_response(HTTPStatus.MOVED_PERMANENTLY)
                new_parts = parts._replace(path=parts.path + "/")
                new_url = urllib.parse.urlunsplit(new_parts)
                self.send_header("Location", new_url)
                self.send_header("Content-Length", "0")
                self.end_headers()  # Adds COOP/COEP
                return None

            for index_name in "index.html", "index.htm":
                index_file: Path = current_path / index_name
                if index_file.exists():
                    current_path = index_file
                    break
            else:
                return self.list_directory(str(current_path))

        content_type: str = self.guess_type(str(current_path)) or "application/octet-stream"

        original_file: Optional[BinaryIO] = None
        try:
            original_file = current_path.open("rb")
            fs = os.fstat(original_file.fileno())

            if "If-Modified-Since" in self.headers and "If-None-Match" not in self.headers:
                try:
                    ims_dt = email.utils.parsedate_to_datetime(
                        self.headers["If-Modified-Since"]
                    )
                    if ims_dt.tzinfo is None:
                        ims_dt = ims_dt.replace(tzinfo=datetime.timezone.utc)

                    last_modified_dt = datetime.datetime.fromtimestamp(
                        fs.st_mtime, datetime.timezone.utc
                    )
                    last_modified_dt = last_modified_dt.replace(microsecond=0)

                    if last_modified_dt <= ims_dt:
                        self.send_response(HTTPStatus.NOT_MODIFIED)
                        self.end_headers()  # Adds COOP/COEP
                        return None
                except (TypeError, IndexError, OverflowError, ValueError) as e:
                    logger.debug(f"Invalid If-Modified-Since header: {e}")
                    pass

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", content_type)
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            file_content: bytes = original_file.read()
            self.send_header("Content-Length", str(len(file_content)))
            f = io.BytesIO(file_content)
            self.end_headers()  # Adds COOP/COEP
            return f

        except FileNotFoundError:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None
        except IsADirectoryError:
            self.send_error(HTTPStatus.NOT_FOUND, "Path is a directory")
            return None
        except PermissionError:
            self.send_error(HTTPStatus.FORBIDDEN, "Permission denied")
            return None
        except Exception as e:
            logger.error(f"Error processing request for {current_path}: {e}", exc_info=True)
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Server error")
            return None
        finally:
            if original_file:
                original_file.close()


class SSLThreadingHTTPServer(server.ThreadingHTTPServer):
    """A threading HTTP server that uses SSL and can serve from a specified directory."""

    def __init__(
        self,
        server_address: ServerAddress,
        HandlerClass: Callable[..., server.BaseHTTPRequestHandler],
        ssl_context: ssl.SSLContext,
        directory: Path,
    ) -> None:
        super().__init__(server_address, HandlerClass)
        self.ssl_context: ssl.SSLContext = ssl_context
        self.directory: Path = directory

    def get_request(self) -> Tuple[ssl.SSLSocket, ServerAddress]:
        """Gets the request and wraps the socket with SSL."""
        conn, addr = self.socket.accept()
        return self.ssl_context.wrap_socket(conn, server_side=True), addr

    def finish_request(self, request: ssl.SSLSocket, client_address: ServerAddress) -> None:
        """Finish one request by creating an instance of the RequestHandlerClass."""
        self.RequestHandlerClass(request, client_address, self, directory=self.directory)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="A simple self-signed development (NON-PRODUCTION) HTTPS server (HTTP/1.1) for serving static files with WASM support."
    )
    parser.add_argument(
        "-H",
        "--hostname",
        default=socket.getfqdn(),
        help="Hostname for the certificate (default: %(default)s)",
    )
    parser.add_argument(
        "-b",
        "--bind",
        metavar="ADDRESS",
        default="0.0.0.0",
        help="Bind to this address (default: %(default)s)",
    )
    parser.add_argument(
        "-d",
        "--directory",
        type=Path,
        default=Path.cwd(),
        help="Serve this directory (default: current directory)",
    )
    parser.add_argument(
        "port",
        default=8443,
        type=int,
        nargs="?",
        help="Bind to this port (default: %(default)s)",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug logging for request handler."
    )
    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)

    serving_directory: Path = args.directory.resolve()
    if not serving_directory.is_dir():
        logger.error(
            f"Error: Directory '{serving_directory}' not existing or not a directory."
        )
        exit(1)

    logger.info(f"Serving files from: {serving_directory}")
    logger.info(f"HTTP Protocol Version: {CustomHTTPRequestHandler.protocol_version}")
    logger.info(f"MIME type for .wasm: {mimetypes.guess_type('file.wasm')[0]}")
    logger.info(f"MIME type for .js: {mimetypes.guess_type('file.js')[0]}")
    logger.info(
        "Will send Cross-Origin-Opener-Policy and Cross-Origin-Embedder-Policy headers."
    )

    cert_data = generate_self_signed_certificate(args.hostname)
    httpd: Optional[SSLThreadingHTTPServer] = None

    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir_path = Path(tmpdir_name)
        key_path: Path = tmpdir_path / "key.pem"
        cert_path: Path = tmpdir_path / "cert.pem"

        key_path.write_text(cert_data["key"])
        cert_path.write_text(cert_data["cert"])

        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(certfile=str(cert_path), keyfile=str(key_path))

        server_address: ServerAddress = (args.bind, args.port)
        try:
            httpd = SSLThreadingHTTPServer(
                server_address, CustomHTTPRequestHandler, ssl_context, serving_directory
            )
            logger.info(f"Serving on https://{args.hostname}:{args.port}/ (Ctrl+C to quit)")
            httpd.serve_forever()
        except OSError as e:
            logger.error(f"Error starting server: {e}")
            if e.errno == socket.errno.EADDRINUSE:
                logger.error(f"Port {args.port} is already in use on {args.bind}.")
            elif e.errno == socket.errno.EACCES:
                logger.error(
                    "Permission denied. Insufficient privileges to bind to port or address."
                )
            exit(1)
        except KeyboardInterrupt:
            logger.info("Server stopped by user (Ctrl+C)")
        finally:
            if httpd:
                logger.info("Shutting down server...")
                httpd.shutdown()
                httpd.server_close()
                logger.info("Server resources released.")


if __name__ == "__main__":
    main()

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

from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

from cryptography import x509
from cryptography.x509 import SubjectKeyIdentifier, AuthorityKeyIdentifier
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def generate_self_signed_certificate(hostname: str) -> dict[str, str]:
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


class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Custom HTTP request handler to set the HTTP protocol version."""

    protocol_version = "HTTP/1.1"

    def __init__(self, request, client_address, server, *, directory=None):
        # The 'directory' argument is passed from SSLThreadingHTTPServer
        #   and is a keyword-only argument for SimpleHTTPRequestHandler's __init__
        super().__init__(request, client_address, server, directory=directory)


class SSLThreadingHTTPServer(ThreadingHTTPServer):
    """A threading HTTP server that uses SSL and can serve from a specified directory."""

    def __init__(self, server_address, HandlerClass, ssl_context, directory):
        super().__init__(server_address, HandlerClass)
        self.ssl_context = ssl_context
        # Directory to serve files from
        self.directory = directory

    def get_request(self):
        """Gets the request and wraps the socket with SSL."""
        conn, addr = self.socket.accept()
        return self.ssl_context.wrap_socket(conn, server_side=True), addr

    def finish_request(self, request, client_address):
        """Finish one request by creating an instance of the RequestHandlerClass,
        passing the serving directory to it."""
        self.RequestHandlerClass(request, client_address, self, directory=self.directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A simple self-signed HTTPS server for serving static files."
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
        default=os.getcwd(),
        help="Serve this directory (default: %(default)s)",
    )
    parser.add_argument(
        "port",
        default=8443,
        type=int,
        nargs="?",
        help="Bind to this port (default: %(default)s)",
    )
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        logger.error(f"Error: Directory '{args.directory}' not existing or not a directory.")
        exit(1)

    logger.info(f"Preparing to serve files from: {os.path.abspath(args.directory)}")

    cert_data = generate_self_signed_certificate(args.hostname)
    httpd = None

    with tempfile.TemporaryDirectory() as tmpdir:
        key_path = os.path.join(tmpdir, "key.pem")
        cert_path = os.path.join(tmpdir, "cert.pem")

        with open(key_path, "w") as f:
            f.write(cert_data["key"])
        with open(cert_path, "w") as f:
            f.write(cert_data["cert"])

        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(certfile=cert_path, keyfile=key_path)

        try:
            httpd = SSLThreadingHTTPServer(
                (args.bind, args.port), CustomHTTPRequestHandler, ssl_context, args.directory
            )
            logger.info(f"Serving on https://{args.hostname}:{args.port}/ (Ctrl+C to quit)")
            httpd.serve_forever()
        except OSError as e:
            logger.error(f"Error starting server: {e}")
            if e.errno == 98:
                # EADDRINUSE
                logger.error(f"Port {args.port} is already in use.")
            elif e.errno == 13:
                # EACCES
                logger.error(
                    "Permission denied. Insufficient privileges to bind to port or address"
                )
            exit(1)
        except KeyboardInterrupt:
            logger.info("Server stopped by user (Ctrl+C)")
        finally:
            if httpd:
                httpd.shutdown()
                httpd.server_close()
                logger.info("Server resources released.")

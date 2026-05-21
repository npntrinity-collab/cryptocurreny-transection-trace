import os
import re
import socket
import ssl
import certifi
from urllib.parse import urlparse
from dotenv import load_dotenv

try:
    from pymongo import MongoClient
    from pymongo.uri_parser import parse_uri
except ImportError:
    MongoClient = None
    parse_uri = None

try:
    import dns.resolver
    import dns.exception
except ImportError:
    dns = None

# Load project .env so MONGO_URI and related vars are available
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'config', '.env'))

DEFAULT_PORT = 27017


def get_mongo_uri():
    uri = os.getenv('MONGO_URI')
    if not uri:
        raise RuntimeError('MONGO_URI environment variable is not set')
    return uri


def parse_hosts_from_uri(uri):
    if uri.startswith('mongodb+srv://') and dns is not None:
        parsed = urlparse(uri)
        hostname = parsed.hostname
        if not hostname:
            return []
        try:
            answers = dns.resolver.resolve(f'_mongodb._tcp.{hostname}', 'SRV')
            return [str(r.target).rstrip('.') + ':' + str(r.port) for r in answers]
        except dns.exception.DNSException as exc:
            print('SRV lookup failed:', exc)
            return [hostname + ':27017']
    if uri.startswith('mongodb://'):
        without_prefix = uri[len('mongodb://'):]
        if '@' in without_prefix:
            without_prefix = without_prefix.split('@', 1)[1]
        host_port = without_prefix.split('/')[0]
        return [item for item in host_port.split(',') if item]
    return []


def get_hosts(uri):
    hosts = parse_hosts_from_uri(uri)
    if not hosts:
        print('Unable to parse hosts from URI. Falling back to the base hostname.')
        parsed = urlparse(uri)
        hostname = parsed.hostname
        if hostname:
            hosts = [f'{hostname}:{DEFAULT_PORT}']
    return hosts


def test_connectivity(host, port):
    errors = []
    try:
        addr_info = socket.getaddrinfo(host, port, proto=socket.IPPROTO_TCP)
        print(f'  DNS resolved {host} to {addr_info[0][4]}')
    except Exception as exc:
        errors.append(f'DNS failed: {exc}')
        print(f'  DNS failed for {host}: {exc}')
        return False

    for family, socktype, proto, canonname, sockaddr in addr_info:
        try:
            with socket.socket(family, socktype, proto) as sock:
                sock.settimeout(10)
                sock.connect(sockaddr)
                print(f'  TCP connect succeeded to {sockaddr}')
                context = ssl.create_default_context(cafile=certifi.where())
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    print(f'  TLS handshake succeeded with {host}: {ssock.version()}')
                    return True
        except Exception as exc:
            errors.append(str(exc))
            print(f'  TLS connect failed to {sockaddr}: {exc}')
    print('  All connection attempts failed for', host)
    return False


def test_mongo_ping(uri):
    if MongoClient is None:
        print('pymongo not available; skipping MongoDB ping test.')
        return
    try:
        client = MongoClient(uri, tls=True, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000, connectTimeoutMS=5000)
        print('Attempting MongoDB ping...')
        client.admin.command('ping')
        print('MongoDB ping succeeded.')
    except Exception as exc:
        print('MongoDB ping failed:', exc)
    finally:
        try:
            client.close()
        except Exception:
            pass


def main():
    uri = get_mongo_uri()
    print('Mongo URI:', re.sub(r'//.*?:.*?@', '//<user>:<pass>@', uri))
    hosts = get_hosts(uri)
    if not hosts:
        print('No hosts found in the URI.')
        return

    for host_entry in hosts:
        if ':' in host_entry:
            host, port = host_entry.split(':', 1)
            port = int(port)
        else:
            host, port = host_entry, DEFAULT_PORT
        print(f'Testing host: {host}:{port}')
        test_connectivity(host, port)
        print('')

    test_mongo_ping(uri)


if __name__ == '__main__':
    main()

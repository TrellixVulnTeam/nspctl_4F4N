import logging
import sys
import socket
import base64
import os

_all_errors = [NotImplementedError, ValueError, socket.error]

try:
    from http.client import HTTPConnection as http_client_HTTPConnection
    from http.client import BadStatusLine as http_client_BadStatusLine
    from http.client import ResponseNotReady as http_client_ResponseNotReady
    from http.client import error as http_client_error
except ImportError as exc:
    sys.stderr.write("!!! CANNOT IMPORT HTTP.CLIENT: " + str(exc) + "\n")
else:
    _all_errors.append(http_client_error)

_all_errors = tuple(_all_errors)

logger = logging.getLogger(__name__)


def create_conn(baseurl, conn=None):
    """Create connections"""

    parts = baseurl.split("://", 1)
    if len(parts) != 2:
        raise ValueError(
            "Provided URI does not " "contain protocol identifier. '%s'" % baseurl
        )
    protocol, url_parts = parts
    del parts

    url_parts = url_parts.split("/")
    host = url_parts[0]
    if len(url_parts) < 2:
        address = "/"
    else:
        address = "/" + "/".join(url_parts[1:])
    del url_parts

    userpass_host = host.split("@", 1)
    if len(userpass_host) == 1:
        host = userpass_host[0]
        userpass = ["anonymous"]
    else:
        host = userpass_host[1]
        userpass = userpass_host[0].split(":")
    del userpass_host

    if len(userpass) > 2:
        raise ValueError("Unable to interpret username/password provided.")
    elif len(userpass) == 2:
        username = userpass[0]
        password = userpass[1]
    elif len(userpass) == 1:
        username = userpass[0]
        password = None
    del userpass

    http_headers = {}
    http_params = {}
    if username and password:
        try:
            encodebytes = base64.encodebytes
        except AttributeError:
            # Python 2
            encodebytes = base64.encodestring
        auth_string = "%s:%s" % (username, password)
        base64string = encodebytes(auth_string.encode()).decode()
        http_headers = {'Authorization': 'Basic %s' % base64string}

    if not conn:
        if protocol == "https":
            # check python ssl support
            try:
                from http.client import HTTPSConnection as http_client_HTTPSConnection
            except ImportError:
                raise NotImplementedError(
                    "python must have ssl enabled for https support"
                )
            conn = http_client_HTTPSConnection(host)
        elif protocol == "http":
            conn = http_client_HTTPConnection(host)
        else:
            raise NotImplementedError("%s is not a supported protocol." % protocol)

    return conn, protocol, address, http_params, http_headers


def make_http_request(conn, address, _params={}, headers={}, dest=None):
    """Uses the |conn| object to request the data"""

    rc = 0
    response = None
    while (rc == 0) or (rc == 301) or (rc == 302):
        try:
            if rc != 0:
                conn = create_conn(address)[0]
            conn.request("GET", address, body=None, headers=headers)
        except SystemExit as exc:
            raise Exception("{}".format(exc))
        except Exception as exc:
            return None, None, "Server request failed: {}".format(exc)
        response = conn.getresponse()
        rc = response.status

        # 301 means that the page address is wrong.
        if (rc == 301) or (rc == 302):
            ignored_data = response.read()
            del ignored_data
            for x in str(response.msg).split("\n"):
                parts = x.split(": ", 1)
                if parts[0] == "Location":
                    if rc == 301:
                        sys.stderr.write(
                            "Location has moved: "
                            + str(parts[1])
                            + "\n"
                        )
                    if rc == 302:
                        sys.stderr.write(
                            "Location has temporarily moved: "
                            + str(parts[1])
                            + "\n"
                        )
                    address = parts[1]
                    break

    if (rc != 200) and (rc != 206):
        return (
            None,
            rc,
            "Server did not respond successfully (%s: %s)"
            % (str(response.status), str(response.reason)),
        )

    if dest:
        dest.write(response.read())
        return "", 0, ""

    return response.read(), 0, ""


def file_get(baseurl=None, dest=None, conn=None, filename=None):
    """Takes a base url to connect to and read from.
    URL should be in the form <proto>://<site>[:port]<path>"""

    if not os.path.isdir(dest):
        os.mkdir(dest)

    filename = str(os.path.basename(baseurl))
    file_path = os.path.join(dest, filename)
    dest = open(file_path, 'wb')

    fetch = file_get_lib(baseurl, dest, conn)

    if fetch != os.EX_OK:
        sys.stderr.write("Fetcher exited with a failure condition.\n")
        return 1
    else:
        sys.stderr.write("Download completed!\n")
        return 0
    return 1


def file_get_lib(baseurl, dest, conn=None):
    """Takes a base url to connect to and read from.
    URL should be in the form <proto>://<site>[:port]<path>"""

    if not conn:
        keepconnection = 0
    else:
        keepconnection = 1

    conn, protocol, address, params, headers = create_conn(baseurl, conn)

    sys.stderr.write("Fetching '" + str(os.path.basename(address)) + "'\n")
    if protocol in ["http", "https"]:
        data, rc, _msg = make_http_request(conn, address, params, headers, dest=dest)
    else:
        raise TypeError("Unknown protocol. '%s'" % protocol)

    if not keepconnection:
        conn.close()

    return rc

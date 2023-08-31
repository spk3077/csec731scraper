"""
File: client.py
Assignment: Web Scraper Assignment
Lanuguage: python3
Author: Sean Kells <spk3077@rit.edu>
Purpose: HTTP Client that parses specified web server response for external references
"""
import sys
import socket
import ssl
import certifi

import re

CRLF = "\r\n"
# URI_ATTRIBUTES no longer necessary with regex
URI_ATTRIBUTES: set = {
    'action=',
    'archive=',
    'background=',
    'cite=',
    'classid=',
    'codebase=',
    'data=',
    'formaction=',
    'href=',
    'icon=',
    'itemtype=',
    'longdesc=',
    'manifest=',
    'poster=',
    'profile=',
    'src=',
    'srcset=',
    'usemap=',
    'xmlns='
}

def generate_request(url: str, host: str) -> str:
    """
    generate_request generates and returns the HTTP request string.

    :param url: Full URL excluding protocol
    :param host: the host domain
    :return: HTTP request string
    """ 
    page: str = url[len(host):]
    if page == "":
        page = "/"
    req = "GET " + page + " HTTP/1.1" + CRLF
    req += "Host: " + host + CRLF
    req += "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.111 Safari/537.36" + CRLF
    req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7" + CRLF
    req += "Accept-Encoding: identity" + CRLF
    req += "Accept-Language: en-US,en;q=0.9" + CRLF
    req += "Connection: close" + CRLF + CRLF
    return req


def send_receive(req: str, host: str) -> tuple[str, str]:
    """
    send_receive communicates with the specified URI and returns the response content

    :param req: HTTP request string
    :param host: the host domain
    :return: response data headers and response data body
    """
    response: str = ""
    conn_type: str = sys.argv[1].split("://")[0]
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    if conn_type == "http":
        conn.connect((host, 80))
        conn.send(req.encode())

        # Retrieve all additional response content
        temp_resp = conn.recv(8192).decode("UTF-8", errors = "ignore")
        while temp_resp != "":
            response += temp_resp
            temp_resp = conn.recv(8192).decode("UTF-8", errors = "ignore")
        print("SOCKET CLOSING...")
        conn.close()
        
    elif conn_type == "https":
        context = ssl.create_default_context(cafile=certifi.where())
        s_conn = context.wrap_socket(conn, server_hostname=host)
        s_conn.connect((host, 443))
        s_conn.send(req.encode())

        # Retrieve all additional response content
        temp_resp = s_conn.recv(8192).decode("UTF-8", errors = "ignore")
        while temp_resp != "":
            response += temp_resp
            temp_resp = s_conn.recv(8192).decode("UTF-8", errors = "ignore")
        print("SOCKET CLOSING...")
        conn.close()
    
    resp_headers = response.split(CRLF + CRLF)[0].strip()
    resp_body = response.split(CRLF + CRLF)[1].strip()
    return resp_headers, resp_body


def parse_references(resp_body: str, host: str):
    """
    parse_references dissects the response_body for unique external references and returns the list of them

    :param resp_body: HTTP response body to dissect
    :param host: the host domain
    :return: set containing external references
    """
    refs: set = set()
    for tag in resp_body.split('<'):
        # Three capturing groups using quantifiers to support domains of varying length and extending parameters/fragments/port specifications
        for uri in re.findall(r'(http|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?', tag):
            refs.add(uri[1])
    
    refs.discard(host)
    return refs


def print_output(refs: set):
    """
    print_output formats the unique references into output acceptable for assignment

    :param refs: set of references located
    :return: Nothing
    """
    print()
    print("UNIQUE EXTERNAL REFERENCE DOMAINS:")
    print("==========================================")
    if len(refs) <= 0:
        print("NONE FOUND")
        
    for ref in sorted(refs):
        print(ref)
    
    print()
    print("TOTAL OF " + str(len(refs)) + " UNIQUE EXTERNAL REFERENCES")

def main():
    """
    main function is called upon execution

    :return: Nothing
    """
    # Check argument variables 
    if len(sys.argv) != 2:
        print("Requires one URI parameter")
        print("EX: python3 client.py https://www.rit.edu/")
        exit(1)
    elif len(sys.argv[1]) < 5 and "http://" != sys.argv[1][0:7] and "https://" != sys.argv[1][0:8]:
        print("Must be a http/https URI input")
        print("EX: python3 client.py https://www.rit.edu/")
        exit(1)

    url = sys.argv[1].split("//")[1]
    host = url.split("/")[0]

    
    req: str = generate_request(url, host)
    resp_headers, resp_body = send_receive(req, host)
    
    refs: set = parse_references(resp_body, host)
    print_output(refs)


main()

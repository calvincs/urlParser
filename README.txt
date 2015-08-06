urlParser
===================
Command line script to parse url into its individual components, returns results as JSON


Requirements
===================
python3
netaddr==0.7.15
pytest==2.7.2


Setup and Run
===================
pip3 install netaddr
pip3 install pytest    
python3 urlParser.py 'https://www.exampledomain.com/'


Some URL Examples
===================

Named URL Versions:
scheme://user:pass@domain.com:8080/path1/path2/path3/page?arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage
scheme://user:pass@subdomains.domain.com:8080/path1/path2/path3/page?arg1=one+two&arg2=2;arg3=three;arg4#Anchor

IPv4 URL Versions:
scheme://user:pass@127.0.0.1:8080/path1/path2/path3/page?arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage
scheme://user:pass@3221226219:8080/path1/path2/path3/page?arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage
scheme://user:pass@0xC0.0x00.0x02.0xEB:8080/path1/path2/path3/page?arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage
scheme://user:pass@0300.0000.0002.0353:8080/path1/path2/path3/page?arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage
scheme://user:pass@0xC00002EB:8080/path1/path2/path3/page?arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage

IPv6 URL Versions:
scheme://user:pass@[::1]:8080/path1/path2/path3/pagearg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage
scheme://user:pass@338288524927261089654170743795120240736:8080/path1/path2/path3/page?arg1=one#AnchorOnPage


Output Examples
===================
Command Line:
	python3 urlParser.py 'scheme://user:pass@domain.com:8080/path1/path2/path3/page?arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage'

JSON Output:
{
    "cgi": {
        "anchor": "AnchorOnPage",
        "arg1": "one+two",
        "arg2": "2",
        "arg3": "three",
        "arg4": ""
    },
    "credential": {
        "password": "pass",
        "username": "user"
    },
    "domain": {
        "fqdn": "domain.com",
        "port": "8080",
        "sld": "domain",
        "tld": "com"
    },
    "input_url": "scheme://user:pass@domain.com:8080/path1/path2/path3/page?arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage",
    "path": "path1/path2/path3/page",
    "scheme": "scheme://"
}

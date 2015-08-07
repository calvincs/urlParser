#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    UrlDeconstruction PyTest
    ------------------------
    Tests UrlDeconstruction Class parsing functions
    :copyright: (c) 2015 by Calvin Schultz.
    :license: BSD, see LICENSE for more details.

    Usage:
    	python3 -m pytest test.py

    Requires:
    	pytest-2.7.2

    Notes:
    	Output of key-value pairs should be ordered
"""

import pytest
from urlParser import UrlDeconstruction

def test_parseScheme():
	"""
		Test parsing Application Scheme from url string
	"""
	urld 		= UrlDeconstruction()
	resSCHEMENorm		= urld.parseScheme("http://user:pass@google.com")
	resSCHEME3Chr 	= urld.parseScheme("ftp://user@google.com")
	resSCHEMENone 	= urld.parseScheme("user@google.com")
	resSCHEMECred 	= urld.parseScheme("user:pass@google.com")

	#Testing Results
	assert	resSCHEMENorm		== ({'scheme': 'http://'}, 'user:pass@google.com')
	assert	resSCHEME3Chr 	== ({'scheme': 'ftp://'}, 'user@google.com')
	assert	resSCHEMENone 	== (None, '')
	assert	resSCHEMECred 	== (None, '')


def test_parseCredentials():
	"""
		Test parsing User Credentials from url string
	"""
	urld 			= UrlDeconstruction()
	resCREDUserPass = urld.parseCredentials("user:pass@google.com")
	resCREDUser 	= urld.parseCredentials("user@google.com")

	#Testing Results
	assert resCREDUserPass 	== ({'credential': {'password': 'pass', 'username': 'user'}}, 'google.com')
	assert resCREDUser 		== ({'credential': {'username': 'user'}}, 'google.com')


def test_parseIpv4():
	"""
		Test parsing IPv4 from url string
	"""
	urld 		= UrlDeconstruction()
	resIPV4DotNot	= urld.parseIpv4("127.0.0.1:8080/p1/p2.do")
	resIPV4DotHex 	= urld.parseIpv4("0xC0.0x00.0x02.0xEB:8080/p1/p2.do")
	resIPV4DotOct	= urld.parseIpv4("0300.0000.0002.0353:8080/p1/p2.do")
	resIPV4HexDec 	= urld.parseIpv4("0xC00002EB:8080/p1/p2.do")
	resIPV4Oct 		= urld.parseIpv4("3221226219:8080/p1/p2.do")

	#Testing Results
	assert	resIPV4DotNot	== ({'ipv4': {'port': '8080', 'address': '127.0.0.1', 'type': 'dotnot'}}, 'p1/p2.do')
	assert 	resIPV4DotHex 	== ({'ipv4': {'port': '8080', 'address': '0xC0.0x00.0x02.0xEB', 'notation': '192.0.2.235', 'type': 'dothex'}}, 'p1/p2.do')
	assert 	resIPV4DotOct	== ({'ipv4': {'type': 'dotoct', 'notation': '192.0.2.235', 'address': '0300.0000.0002.0353', 'port': '8080'}}, 'p1/p2.do')
	assert 	resIPV4HexDec 	== ({'ipv4': {'address': '0xC00002EB', 'type': 'hexdec', 'notation': '192.0.2.235', 'port': '8080'}}, 'p1/p2.do')
	assert 	resIPV4Oct 		== ({'ipv4': {'address': '3221226219', 'port': '8080', 'type': 'dec', 'notation': '192.0.2.235'}}, 'p1/p2.do')


def test_parseIpv6():
	"""
		Test parsing IPv6 from url string
	"""
	urld 		= UrlDeconstruction()
	resIPV6Local	= urld.parseIpv6("[::1]:8080/p1/p2.do")
	resIPV6V4Com	= urld.parseIpv6("[::ffff:10.0.0.1/96]:8080/p1/p2.do")	
	resIPV6Full		= urld.parseIpv6("[FEDC:BA98:7654:3210:FEDC:BA98:7654:3210]:8080/p1/p2.do")
	resIPV6Oct		= urld.parseIpv6("338288524927261089654170743795120240736:8080/p1/p2.do")

	#Testing Results
	assert	resIPV6Local	== ({'ipv6': {'address': '::1', 'port': '8080', 'type': 'std'}}, 'p1/p2.do')
	assert 	resIPV6V4Com 	== ({'ipv6': {'type': 'std', 'address': '::ffff:10.0.0.1/96', 'port': '8080'}}, 'p1/p2.do')
	assert 	resIPV6Full		== ({'ipv6': {'port': '8080', 'address': 'fedc:ba98:7654:3210:fedc:ba98:7654:3210', 'type': 'std'}}, 'p1/p2.do')
	assert 	resIPV6Oct		== ({'ipv6': {'type': 'oct', 'port': '8080', 'standard': 'fe80::21b:77ff:fbd6:7860', 'address': '338288524927261089654170743795120240736'}}, 'p1/p2.do')


def test_parseAnchor():
	"""
		Test parsing Anchor from url string
	"""
	urld 		= UrlDeconstruction()
	resANCR1 	= urld.parseAnchor("/path1/path2/page.do?arg1=(one+two);t=2;out#PageAnchor")
	resANCR2 	= urld.parseAnchor("")

	#Testing Results
	assert resANCR1 	== ({'#': 'PageAnchor'}, '/path1/path2/page.do?arg1=(one+two);t=2;out')
	assert resANCR2 	== (None, '')


def test_parsePath():
	"""
		Test parsing Url Path from url string
	"""
	urld 		= UrlDeconstruction()
	resPATH1 	= urld.parsePath("/path1/path2/page.do")
	resPATH2 	= urld.parsePath("/path1/path2/page.html")
	resPATH3 	= urld.parsePath("/path1/path2/page/")
	resPATH4 	= urld.parsePath("")
	resPATH5 	= urld.parsePath("/path1/path2/page.do?arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage")
	resPATH6 	= urld.parsePath("/path1/path2/page.html?arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage")
	resPATH7 	= urld.parsePath("/path1/path2/page/?arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage")

	#Testing Results
	assert resPATH1 	== ({'path': '/path1/path2/page.do'}, '')
	assert resPATH2 	== ({'path': '/path1/path2/page.html'}, '')
	assert resPATH3 	== ({'path': '/path1/path2/page/'}, '')
	assert resPATH4 	== (None, '')
	assert resPATH5 	== ({'path': '/path1/path2/page.do'}, 'arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage')
	assert resPATH6 	== ({'path': '/path1/path2/page.html'}, 'arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage')
	assert resPATH7 	== ({'path': '/path1/path2/page/'}, 'arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage')


def test_parseCGI():
	"""
		Test parsing CGI from url string
	"""
	urld 		= UrlDeconstruction()
	resCGI1 	= urld.parseCGI("arg1=one+two&arg2=2&arg3=three3")
	resCGI2 	= urld.parseCGI("arg1=one+two&arg2=2;arg3=three;arg4")
	resCGI3 	= urld.parseCGI("arg1=one+two&arg2=2;arg3=three;arg4#PageAnchor")
	resCGI4 	= urld.parseCGI("arg1#PageAnchor")
	resCGI5 	= urld.parseCGI("#PageAnchor")
	resCGI6 	= urld.parseCGI("")

	#Testing Results
	assert resCGI1 	== ({'cgi': {'arg1': 'one+two', 'arg3': 'three3', 'arg2': '2'}}, '')
	assert resCGI2 	== ({'cgi': {'arg4': '', 'arg1': 'one+two', 'arg2': '2', 'arg3': 'three'}}, '')
	assert resCGI3 	== ({'cgi': {'arg3': 'three', 'arg2': '2', 'arg1': 'one+two'}}, '')
	assert resCGI4 	== ({'cgi': {'arg1': ''}}, '')
	assert resCGI5 	== (None, '')
	assert resCGI6 	== (None, '')


def test_urlParseEngine():
	"""
		Test urlParseEngine full examples
	"""
	urld 		= UrlDeconstruction()
	resENGTest1 	= urld.urlParseEngine("scheme://user:pass@www.domain.com:8080/p1/p2/p3/page.do?arg1=one+two&arg2=2&arg3=three3;arg4#AnchorOnPage")
	urld.flush()
	resENGTest2 	= urld.urlParseEngine("scheme://user:pass@127.0.0.1:8080/p1/p2/p3/page.do?arg1=one+two&arg2=2&arg3=three3;arg4#AnchorOnPage")
	urld.flush()
	resENGTest3 	= urld.urlParseEngine("scheme://user:pass@localhost:8080/p1/p2/p3/page.do?arg1=one+two&arg2=2&arg3=three3;arg4#AnchorOnPage")
	urld.flush()
	resENGTest4 	= urld.urlParseEngine("scheme://user:pass@[::1]:8080/p1/p2/p3/page.do?arg1=one+two&arg2=2&arg3=three3;arg4#AnchorOnPage")

	#Testing Results - This needs to be cleaned up / order keys
	assert resENGTest1 	== {'input_url': 'scheme://user:pass@www.domain.com:8080/p1/p2/p3/page.do?arg1=one+two&arg2=2&arg3=three3;arg4#AnchorOnPage', 
							'#': 'AnchorOnPage', 
							'credential': {'password': 'pass', 'username': 'user'}, 
							'cgi': {'arg3': 'three3', 'arg2': '2', 'arg4': '', 'arg1': 'one+two'}, 
							'domain': {'sld': 'domain', 'tld': 'com', 'host': 'www', 'port': '8080', 'fqdn': 'www.domain.com'}, 
							'path': 'p1/p2/p3/page.do', 
							'scheme': 'scheme://'
							}


	assert resENGTest2 	== {'ipv4': {'type': 'dotnot', 'address': '127.0.0.1', 'port': '8080'}, 
							'path': 'p1/p2/p3/page.do', 
							'input_url': 'scheme://user:pass@127.0.0.1:8080/p1/p2/p3/page.do?arg1=one+two&arg2=2&arg3=three3;arg4#AnchorOnPage', 
							'#': 'AnchorOnPage', 
							'credential': {'username': 'user', 'password': 'pass'}, 
							'cgi': {'arg4': '', 'arg1': 'one+two', 'arg3': 'three3', 'arg2': '2'}, 
							'scheme': 'scheme://'
							}


	assert resENGTest3 	== {'input_url': 'scheme://user:pass@localhost:8080/p1/p2/p3/page.do?arg1=one+two&arg2=2&arg3=three3;arg4#AnchorOnPage', 
							'scheme': 'scheme://', 
							'cgi': {'arg3': 'three3', 'arg4': '', 'arg2': '2', 'arg1': 'one+two'}, 
							'credential': {'username': 'user', 'password': 'pass'}, 
							'path': 'p1/p2/p3/page.do', 
							'domain': {'port': '8080', 'fqdn': 'localhost'}, 
							'#': 'AnchorOnPage'
							}

	assert resENGTest4 	== {'scheme': 'scheme://', 
							'cgi': {'arg1': 'one+two', 'arg2': '2', 'arg3': 'three3', 'arg4': ''}, 
							'ipv6': {'port': '8080', 'address': '::1', 'type': 'std'}, 
							'credential': {'username': 'user', 'password': 'pass'}, 
							'path': 'p1/p2/p3/page.do', 
							'input_url': 'scheme://user:pass@[::1]:8080/p1/p2/p3/page.do?arg1=one+two&arg2=2&arg3=three3;arg4#AnchorOnPage', 
							'#': 'AnchorOnPage'
							}


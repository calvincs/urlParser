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
	resNorm		= urld.parseScheme("http://user:pass@google.com")
	res3Chr 	= urld.parseScheme("ftp://user@google.com")
	resNone 	= urld.parseScheme("user@google.com")
	resCred 	= urld.parseScheme("user:pass@google.com")

	#Testing Results
	assert	resNorm		== ({'scheme': 'http://'}, 'user:pass@google.com')
	assert	res3Chr 	== ({'scheme': 'ftp://'}, 'user@google.com')
	assert	resNone 	== (None, '')
	assert	resCred 	== (None, '')

def test_parseCredentials():
	"""
		Test parsing User Credentials from url string
	"""
	urld 		= UrlDeconstruction()
	resUserPass = urld.parseCredentials("user:pass@google.com")
	resUser 	= urld.parseCredentials("user@google.com")

	#Testing Results
	assert resUserPass 	== ({'credential': {'password': 'pass', 'username': 'user'}}, 'google.com')
	assert resUser 		== ({'credential': {'username': 'user'}}, 'google.com')

def test_parseIpv4():
	"""
		Test parsing IPv4 from url string
	"""
	urld 		= UrlDeconstruction()
	resDotNot	= urld.parseIpv4("127.0.0.1:8080/p1/p2.do")
	resDotHex 	= urld.parseIpv4("0xC0.0x00.0x02.0xEB:8080/p1/p2.do")
	resDotOct	= urld.parseIpv4("0300.0000.0002.0353:8080/p1/p2.do")
	resHexDec 	= urld.parseIpv4("0xC00002EB:8080/p1/p2.do")
	resOct 		= urld.parseIpv4("3221226219:8080/p1/p2.do")

	#Testing Results
	assert	resDotNot	== ({'ipv4': {'port': '8080', 'address': '127.0.0.1', 'type': 'dotnot'}}, 'p1/p2.do')
	assert 	resDotHex 	== ({'ipv4': {'port': '8080', 'address': '0xC0.0x00.0x02.0xEB', 'notation': '192.0.2.235', 'type': 'dothex'}}, 'p1/p2.do')
	assert 	resDotOct	== ({'ipv4': {'type': 'dotoct', 'notation': '192.0.2.235', 'address': '0300.0000.0002.0353', 'port': '8080'}}, 'p1/p2.do')
	assert 	resHexDec 	== ({'ipv4': {'address': '0xC00002EB', 'type': 'hexdec', 'notation': '192.0.2.235', 'port': '8080'}}, 'p1/p2.do')
	assert 	resOct 		== ({'ipv4': {'address': '3221226219', 'port': '8080', 'type': 'dec', 'notation': '192.0.2.235'}}, 'p1/p2.do')

def test_parseIpv6():
	"""
		Test parsing IPv6 from url string
	"""
	urld 		= UrlDeconstruction()
	resLocal	= urld.parseIpv6("[::1]:8080/p1/p2.do")
	resV4Com	= urld.parseIpv6("[::ffff:10.0.0.1/96]:8080/p1/p2.do")	
	resFull		= urld.parseIpv6("[FEDC:BA98:7654:3210:FEDC:BA98:7654:3210]:8080/p1/p2.do")
	resOct		= urld.parseIpv6("338288524927261089654170743795120240736:8080/p1/p2.do")

	#Testing Results
	assert	resLocal	== ({'ipv6': {'address': '::1', 'port': '8080', 'type': 'std'}}, 'p1/p2.do')
	assert 	resV4Com 	== ({'ipv6': {'type': 'std', 'address': '::ffff:10.0.0.1/96', 'port': '8080'}}, 'p1/p2.do')
	assert 	resFull		== ({'ipv6': {'port': '8080', 'address': 'fedc:ba98:7654:3210:fedc:ba98:7654:3210', 'type': 'std'}}, 'p1/p2.do')
	assert 	resOct		== ({'ipv6': {'type': 'oct', 'port': '8080', 'standard': 'fe80::21b:77ff:fbd6:7860', 'address': '338288524927261089654170743795120240736'}}, 'p1/p2.do')

def test_parsePath():
	"""
		Test parsing Url Path from url string
	"""
	urld 		= UrlDeconstruction()
	resSimple1 	= urld.parsePath("/path1/path2/page.do")
	resSimple2 	= urld.parsePath("/path1/path2/page.html")
	resSimple3 	= urld.parsePath("/path1/path2/page/")
	resSimple4 	= urld.parsePath("")
	resCompx1 	= urld.parsePath("/path1/path2/page.do?arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage")
	resCompx2 	= urld.parsePath("/path1/path2/page.html?arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage")
	resCompx3 	= urld.parsePath("/path1/path2/page/?arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage")

	#Testing Results
	print(resSimple1)
	assert resSimple1 	== ({'path': '/path1/path2/page.do'}, '')
	assert resSimple2 	== ({'path': '/path1/path2/page.html'}, '')
	assert resSimple3 	== ({'path': '/path1/path2/page/'}, '')
	assert resSimple4 	== (None, '')

	assert resCompx1 	== ({'path': '/path1/path2/page.do'}, 'arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage')
	assert resCompx2 	== ({'path': '/path1/path2/page.html'}, 'arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage')
	assert resCompx3 	== ({'path': '/path1/path2/page/'}, 'arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage')

def test_parseCGI():
	"""
		Test parsing CGI from url string
	"""
	urld 		= UrlDeconstruction()
	resCGI1 	= urld.parseCGI("arg1=one+two&arg2=2&arg3=three3")
	resCGI2 	= urld.parseCGI("arg1=one+two&arg2=2;arg3=three;arg4")
	resCGI3 	= urld.parseCGI("arg1=one+two&arg2=2;arg3=three;arg4#PageAnchor")
	resCGI4 	= urld.parseCGI("")

	#Testing Results
	assert resCGI1 	== ({'cgi': {'arg1': 'one+two', 'arg3': 'three3', 'arg2': '2'}}, '')
	assert resCGI2 	== ({'cgi': {'arg3': 'three', 'arg1': 'one+two', 'arg2': '2', 'arg4': ''}}, '')
	assert resCGI3 	== ({'cgi': {'anchor': 'PageAnchor', 'arg3': 'three', 'arg4': '', 'arg1': 'one+two', 'arg2': '2'}}, '')
	assert resCGI4 	== (None, '')

def test_urlParseEngine():
	"""
		Test urlParseEngine full examples
	"""
	urld 		= UrlDeconstruction()
	resTest1 	= urld.urlParseEngine("scheme://user:pass@www.domain.com:8080/p1/p2/p3/page.do?arg1=one+two&arg2=2&arg3=three3;arg4#AnchorOnPage")
	urld.flush()
	resTest2 	= urld.urlParseEngine("scheme://user:pass@127.0.0.1:8080/p1/p2/p3/page.do?arg1=one+two&arg2=2&arg3=three3;arg4#AnchorOnPage")
	urld.flush()
	resTest3 	= urld.urlParseEngine("scheme://user:pass@localhost:8080/p1/p2/p3/page.do?arg1=one+two&arg2=2&arg3=three3;arg4#AnchorOnPage")
	urld.flush()
	resTest4 	= urld.urlParseEngine("scheme://user:pass@[::1]:8080/p1/p2/p3/page.do?arg1=one+two&arg2=2&arg3=three3;arg4#AnchorOnPage")

	#Testing Results - This needs to be cleaned up / order keys
	assert resTest1 	== {'input_url': 'scheme://user:pass@www.domain.com:8080/p1/p2/p3/page.do?arg1=one+two&arg2=2&arg3=three3;arg4#AnchorOnPage', 
							'domain': {'tld': 'com', 'port': '8080', 'host': 'www', 'sld': 'domain', 'fqdn': 'www.domain.com'}, 
							'credential': {'password': 'pass', 'username': 'user'}, 
							'scheme': 'scheme://', 
							'path': 'p1/p2/p3/page.do', 
							'cgi': {'arg2': '2', 'arg3': 'three3', 'arg4': '', 'arg1': 'one+two', 'anchor': 'AnchorOnPage'}
							}
	
	assert resTest2 	== {'path': 'p1/p2/p3/page.do', 
							'input_url': 'scheme://user:pass@127.0.0.1:8080/p1/p2/p3/page.do?arg1=one+two&arg2=2&arg3=three3;arg4#AnchorOnPage', 
							'credential': {'username': 'user', 'password': 'pass'}, 
							'scheme': 'scheme://', 
							'ipv4': {'type': 'dotnot', 'address': '127.0.0.1', 'port': '8080'}, 
							'cgi': {'arg2': '2', 'arg3': 'three3', 'arg1': 'one+two', 'anchor': 'AnchorOnPage', 'arg4': ''}
							}

	assert resTest3 	== {'cgi': {'arg1': 'one+two', 'arg4': '', 'anchor': 'AnchorOnPage', 'arg2': '2', 'arg3': 'three3'}, 
							'scheme': 'scheme://', 
							'input_url': 'scheme://user:pass@localhost:8080/p1/p2/p3/page.do?arg1=one+two&arg2=2&arg3=three3;arg4#AnchorOnPage', 
							'path': 'p1/p2/p3/page.do', 
							'domain': {'port': '8080', 'fqdn': 'localhost'}, 
							'credential': {'password': 'pass', 'username': 'user'}
							}
	assert resTest4 	== {'ipv6': {'port': '8080', 'type': 'std', 'address': '::1'}, 
							'scheme': 'scheme://', 
							'cgi': {'arg4': '', 'arg2': '2', 'arg3': 'three3', 'anchor': 'AnchorOnPage', 'arg1': 'one+two'}, 
							'credential': {'username': 'user', 'password': 'pass'}, 
							'path': 'p1/p2/p3/page.do', 
							'input_url': 'scheme://user:pass@[::1]:8080/p1/p2/p3/page.do?arg1=one+two&arg2=2&arg3=three3;arg4#AnchorOnPage'
							}


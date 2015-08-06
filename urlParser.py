#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import urllib.parse
import netaddr
import re
import json
import traceback

class UrlDeconstruction:
	"""
		UrlDeconstruction Class
			
		Requirements:
			Python3
			urllib3==1.7.1
			netaddr==0.7.15

		Notes:
			Update updateStates function to order the dict by keys
	"""

	def __init__(self):
		#Initialize Variables
		self._urlComponents 	= {}
		self._urlString 		= ''

	def flush(self):
		"""
			Re-Initialize Variables
		"""
		self._urlComponents 	= {}
		self._urlString 		= ''

	def findPattern(self, patternList, testString):
		"""
			Takes a dict of patterns, finds match against testString
			First one to match wins
			
			Returns dict key or None if unable to find match
		"""
		try:
			for regExpKey in patternList.keys():
				regExpPattern = patternList[regExpKey]
				pattern = regExpPattern.match(testString)
				if pattern:
					return regExpKey
			else:
				return False
		except Exception:
			traceback.print_exc()

	def updateStates(self, data):
		"""
			Update the current urlString State as well as the urlComponents Dict
			#Takes tupil (urlComponents, urlString)
		"""
		try:
			(components, urlString) = data
			self._urlString 		= urlString
			self._urlComponents.update(components)
		except Exception:
			traceback.print_exc()

	def returnJson(self):
		"""
			Returns urlComponents out as JSON friendly string
		"""
		return json.dumps(self._urlComponents, sort_keys=True, indent=4, separators=(',', ': '))

	def parseIpv4(self, urlString):
		"""
			Attempt to get IPv4 w/ Port from the url string input
		"""
		try:
			#Standard Dotted Notation
			regDotNot	=	re.compile('^((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(:([\d]{1,5})(/|$)|/|$)')
			#Dotted Hexadecimal
			regDotHex	=	re.compile('^(0x[A-F0-9]{2}\.0x[A-F0-9]{2}\.0x[A-F0-9]{2}\.0x[A-F0-9]{2})(:([\d]{1,5})(/|$)|/|$)', re.IGNORECASE)
			#Dotted Octal
			regDotOct	=	re.compile('^([\d]{4}\.[\d]{4}\.[\d]{4}\.[\d]{4})(:([\d]{1,5})(/|$)|/|$)')
			#Hexadecimal
			regHexDec	=	re.compile('^(0x[\dA-F]{8})(:([\d]{1,5})(/|$)|/|$)', re.IGNORECASE)
			#Octal
			regOct		=	re.compile('^([\d]{12})(:([\d]{1,5})(/|$)|/|$)')
			#Decimal
			regDec 		=	re.compile('^([\d]{10})(:([\d]{1,5})(/|$)|/|$)')

			#Collection of patterns
			ipv4RegPatterns	=	 {	'DotNot' : regDotNot,
								  	'DotHex' : regDotHex,
								  	'DotOct' : regDotOct,
								  	'HexDec' : regHexDec,
								  	'Oct'	 : regOct,
								  	'Dec'	 : regDec}

			#Create Dict & vars for results
			results 		= {}
			results['ipv4'] = {}
			newUrlString	= ''

			#Find Pattern to use
			regExpKey	= self.findPattern(ipv4RegPatterns, urlString)

			#Parse urlString
			if regExpKey:
				regPattern 	= ipv4RegPatterns[regExpKey]
				out 		= [m for m in regPattern.findall(urlString)]
				ipv4Data	= [(w,y, len(w+x)) for w,x,y,z in out][0]
				ipAddress	= ipv4Data[0]
				ipPort		= ipv4Data[1]
				splitPos	= ipv4Data[2]
				if ipPort:					results['ipv4']['port'] = ipPort
				if regExpKey != 'DotNot':	results['ipv4']['notation'] = str(netaddr.IPAddress(ipAddress))
				results['ipv4']['address'] 			= ipAddress
				results['ipv4']['type'] 			= regExpKey.lower()

				newUrlString = urlString[splitPos:]

			else:
				results =  None

		except Exception:
			traceback.print_exc()

		finally:
			#Return results
			return (results, newUrlString)

	def parseIpv6(self, urlString):
		"""
			Attempt to get IPv6 w/ Port from the url string input
		"""
		try:
			#Standard and Abbv Version
			regStd	=	re.compile('^\[([0-9a-f:%\./]*)\](:([\d]{1,5})(/|$)|/|$)', re.IGNORECASE)
			#Oct
			regOct	=	re.compile('^([\d]{39})(:([\d]{1,5})(/|$)|/|$)', re.IGNORECASE)

			#Collection of patterns
			ipv6RegPatterns	=	 {	'Std' : regStd,
								  	'Oct' : regOct}

			#Create Dict & vars for results
			results 		= {}
			results['ipv6'] = {}
			newUrlString 	= ''

			#Find Pattern to use
			regExpKey	= self.findPattern(ipv6RegPatterns, urlString)

			#Parse urlString
			if regExpKey:
				regPattern 	= ipv6RegPatterns[regExpKey]
				out 		= [m for m in regPattern.findall(urlString)]
				ipv6Data	= [(w,y, len(w+x)) for w,x,y,z in out][0]
				ipAddress	= ipv6Data[0]
				ipPort		= ipv6Data[1]
				if ipPort:	results['ipv6']['port'] = ipPort
				if regExpKey != 'Std': 
					results['ipv6']['standard'] = str(netaddr.IPAddress(int(ipAddress)))
					splitPos = ipv6Data[2]
				elif regExpKey == 'Std':
					splitPos = ipv6Data[2] + 2 #We need to account for the space taken by the brackets
				else:
					pass
				results['ipv6']['address'] 			= ipAddress.lower()
				results['ipv6']['type'] 			= regExpKey.lower()
				
				newUrlString = urlString[splitPos:]
			
			else:
				results = None

		except Exception:
			traceback.print_exc()

		finally:
			#Return results
			return (results, newUrlString)

	def parseDomain(self, urlString):
		"""
			Attempt to get Domain details from url string
		"""
		try:
			#Domain Regex
			regDom		=	re.compile('^([\w\-\.]*\.[\w]*)(:([\d]{1,5})(/|$)|/|$)', re.IGNORECASE)
			regLoc		=	re.compile('^(localhost)(:([\d]{1,5})(/|$)|/|$)', re.IGNORECASE)

			#Collection of patterns
			domRegPatterns	=	 {	'Dom' : regDom,
								  	'Loc' : regLoc}

			#Create Dict & vars for results
			results 			= {}
			results['domain'] 	= {}
			newUrlString		= ''

			#Find Pattern to use
			regExpKey	= self.findPattern(domRegPatterns, urlString)

			#Parse urlString
			if regExpKey:
				regPattern 	= domRegPatterns[regExpKey]
				out 		= [m for m in regPattern.findall(urlString)]
				fqdnData 	= [(w,y, len(w+x)) for w,x,y,z in out][0]
				fqdn 		= fqdnData[0]
				port 		= fqdnData[1]
				splitPos	= fqdnData[2]
				tldPos 		= fqdn.rfind('.') + 1 if fqdn.find('.') != -1 else None
				tld 		= fqdn[tldPos:]
				if port: 	results['domain']['port']	= port
				if fqdn: 	results['domain']['fqdn']	= fqdn
				if tldPos:	results['domain']['tld']	= tld

				#Extract SLD Information
				subData = [(x.start(), x.end()) for x in re.finditer('\.', fqdn)] # Get tuples of all '.' positions
				if len(subData) == 1:	# Domain contains only SLD
					results['domain']['sld'] 	= fqdn[:subData[0][0]]
				elif len(subData) > 1:	# Domain has more then one sub domain
					posSLD 		= (subData[len(subData)-2][1], subData[len(subData)-1][0])
					results['domain']['sld'] 	= fqdn[posSLD[0]:posSLD[1]]
					posHostSLD	= posSLD[0] -1
					results['domain']['host'] 	= fqdn[:posHostSLD]
				else:
					pass
				
				newUrlString = urlString[splitPos:]

			else:
				results =  None

		except Exception:
			traceback.print_exc()

		finally:
			#Return results
			return (results, newUrlString)

	def parseScheme(self, urlString):
		"""
			Attempt to get Application Scheme from url string
		"""
		try:
			#Scheme Regex
			regScheme	=	re.compile('^([\w-]*)://')

			#Create Dict & vars for results
			results 			= {}
			results['scheme'] 	= {}
			newUrlString		= ''

			#Parse urlString
			out = [m.end(0) for m in regScheme.finditer(urlString)]
			if out:
				results['scheme'] 	= urlString[:out[0]]
				newUrlString 		= urlString[out[0]:]

			else:
				results = None

		except Exception:
			traceback.print_exc()

		finally:
			#Return results
			return (results, newUrlString)	

	def parseCredentials(self, urlString):
		"""
			Attempt to get Credentials from url string
		"""
		try:
			#Credential Regex
			regCreds	=	re.compile('^([\w]*):([\w]*)@|([a-z0-9]*)@')

			#Create Dict & vars for results
			results 				= {}
			results['credential'] 	= {}
			newUrlString 			= ''

			#Parse urlString
			out = [m.end(0) for m in regCreds.finditer(urlString)]
			if out:
				credString	= urlString[:(out[0]-1)]
				#Seperate User:Pass if present
				if credString.find(':') > 0:
					(credUser, credPass) 				= credString.split(':')
					results['credential']['username'] 	= credUser
					results['credential']['password'] 	= credPass
				else:
					results['credential']['username'] 	= credString

				newUrlString = urlString[out[0]:]
				
			else:
				results =  None

		except Exception:
			traceback.print_exc()

		finally:
			#Return results
			return (results, newUrlString)			

	def parsePath(self, urlString):
		"""
			Attempt to get Path Information from url string
		"""
		try:
			#Path Regex
			regPath		=	re.compile('^([\w\./]*)')

			#Create Dict & vars for results
			results 			= {}
			results['path'] 	= {}
			newUrlString 		= ''

			#Parse urlString
			out = regPath.match(urlString)
			if out:
				#If the path is empty, return None with empty url string
				if out.groups()[0] != '':
					results['path'] = out.groups()[0]
					newUrlString 	= urlString[out.end()+1:]
				else:
					results = None
			else:
				results = None

		except Exception:
			traceback.print_exc()

		finally:
			#Return results
			return (results, newUrlString)

	def parseCGI(self, urlString):
		"""
			Attempt to get CGI values and Anchor from url string
		"""
		try:
			#CGI Regex
			regCGI		=	re.compile('([\w]+)[:=] ?"?([\w\+\(\)]+)"?|(\w+)|(#)')

			#Create Dict for results
			results				= {}
			results['cgi']		= {}

			#Parse urlString
			out = regCGI.findall(urlString)
			if out:
				#Init parsing variables
				cgiValues 		= {}
				anchorValue		= None
				anchorToggle 	= False
				for values in out:
					#Shorten Value Names
					v0 = values[0]
					v1 = values[1]
					v2 = values[2]
					v3 = values[3]

					#Perform Logic to get values
					if values[3]: anchorToggle 		= True	#Pound symbol found, capture the Anchor
					
					#Capture Values
					if v0: 						results['cgi'][v0] = v1
					if v2 and anchorToggle: 	results['cgi']['#'] = v2
					if v2 and not anchorToggle:	results['cgi'][v2] = ''
			else:
				results =  None

		except Exception:
			traceback.print_exc()

		finally:
			#Return results
			return (results, '')

	def urlParseEngine(self, urlInput):
		"""
			Systematicly Deconstruct the url string left -> right
			See comments
		"""
		try:
			#1. 	Clean the URL, as it may be qouted
			cleanUrl 	= urllib.parse.unquote(urlInput)

			#2. 	Recored the results
			self._urlComponents['input_url'] 	= urlInput
			#2a. 	Make note if it was diffrent, set urlInput to new cleaned input
			if cleanUrl != urlInput: 
				self._urlComponents['clean_url'] = cleanUrl
				urlInput = cleanUrl

			#3. 	Set the urlString variable
			self._urlString = urlInput

			#4. 	Begin main parse logic
			# 		--Scheme
			outScheme 	= self.parseScheme(self._urlString)
			if outScheme != (None, ''): self.updateStates(outScheme)

			#		--Credentials
			outCreds	= self.parseCredentials(self._urlString)
			if outCreds != (None, ''):  self.updateStates(outCreds)


			#5. 	IPv4/6 and Domain Parsing, First match wins
			matchToggle = False
			#--IPv6
			outIpv6		= self.parseIpv6(self._urlString)
			if outIpv6 != (None, '') and matchToggle is False:
				self.updateStates(outIpv6)
				matchToggle = True

			#--IPv4
			outIpv4		= self.parseIpv4(self._urlString)
			if outIpv4 != (None, '') and matchToggle is False:
				self.updateStates(outIpv4)
				matchToggle = True

			#--Domain
			outDomain	= self.parseDomain(self._urlString)
			if outDomain != (None, '') and matchToggle is False:
				self.updateStates(outDomain)
				matchToggle = True

			#6. 	Path Parsing
			outPath	= self.parsePath(self._urlString)
			if outPath!= (None, ''):	self.updateStates(outPath)

			#7. 	CGI/Anchor Parsing	
			outCGI	= self.parseCGI(self._urlString)
			if outCGI != (None, ''):	self.updateStates(outCGI)

		except Exception as err:
			traceback.print_exc()

		finally:
			#Return Parsed Data
			return self._urlComponents


def main(urlString):
	urld = UrlDeconstruction()
	urld.urlParseEngine(urlString)
	print(urld.returnJson())


if __name__ == '__main__':
	if len(sys.argv) > 1:
		main(sys.argv[1])
	else:
		doc = """
Input: 	Takes URL input and parses into its individual possible components
Output: JSON Document

Possible URL Structure Examples
----------------------
	#Named URL Versions
	scheme://user:pass@domain.com:8080/path1/path2/path3/page?arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage
	scheme://user:pass@subdomains.domain.com:8080/path1/path2/path3/page?arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage

	#IPv4 Versions
	scheme://user:pass@127.0.0.1:8080/path1/path2/path3/page?arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage
	scheme://user:pass@3221226219:8080/path1/path2/path3/page?arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage
	scheme://user:pass@0xC0.0x00.0x02.0xEB:8080/path1/path2/path3/page?arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage
	scheme://user:pass@0300.0000.0002.0353:8080/path1/path2/path3/page?arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage
	scheme://user:pass@0xC00002EB:8080/path1/path2/path3/page?arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage

	#IPv6 Versions
	scheme://user:pass@[::1]:8080/path1/path2/path3/page?arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage
	scheme://user:pass@338288524927261089654170743795120240736:8080/path1/path2/path3/page?arg1=one+two&arg2=2;arg3=three;arg4#AnchorOnPage

*CGI may use ?/&/;/=
*Single Anchor capture
*URL may lack full possible structure, deconstruct occures left to right

W3C  URL - http://www.w3.org/TR/url
IPv6 URL - https://www.ietf.org/rfc/rfc2732.txt
"""
		print(doc)
		sys.exit(-1)
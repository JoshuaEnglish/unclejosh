# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 17:40:53 2017

@author: jenglish
"""
from lxml import etree
addressbooktext = '''<addressBook>
  <card>
    <name>John Smith</name>
    <email>js@example.com</email>
  </card>
  <card>
    <name>Fred Bloggs</name>
    <email>fb@example.net</email>
  </card>
</addressBook>'''

addressbook = etree.fromstring(addressbooktext)

rngtext = '''
<element name="addressBook" xmlns="http://relaxng.org/ns/structure/1.0">
  <zeroOrMore>
    <element name="card">
      <element name="name">
        <text/>
      </element>
      <element name="email">
        <text/>
      </element>
    </element>
  </zeroOrMore>
</element>'''

rng = etree.fromstring(rngtext)
RNG = etree.RelaxNG(rng)
RNG.assertValid(addressbook)

E = etree.QName(rng.nsmap[None], "element")

stylesheet = '''<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:rng="http://relaxng.org/ns/structure/1.0"
exclude-result-prefixes="rng">

<xsl:output method="html" indent="yes" />

<xsl:template match="/">
  <html>
  <body>
      <h2>RNG2HTML</h2>
      <xsl:apply-templates/>
  </body>
  </html>
</xsl:template>

<xsl:template match="rng:zeroOrMore">
    <div class="zeroOrMore"><xsl:apply-templates/></div>
</xsl:template>

<xsl:template match="rng:element[@name='card']">
    <div class="card"><xsl:apply-templates/></div>
</xsl:template>

<xsl:template match="rng:element[@name='name']">
    <label>Name</label><input type="text" value="your name here"/>
</xsl:template>

<xsl:template match="rng:element[@name='email']">
    <label>Email</label><input type="email" value="me@example.com"/>
</xsl:template>

</xsl:stylesheet>'''

style = etree.fromstring(stylesheet)
xslt = etree.XSLT(style)
res = xslt.apply(rng)
print(res)
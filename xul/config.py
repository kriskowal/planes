#!/usr/bin/env python

app = 'ish'
name = 'ish'
description = 'A Graphical Shell Client'
author = 'Kris Kowal'
authorURL = "http://planes.com"
company = 'Cixar'
uid = "".join(file('@.uid')).strip()

major_version = 0
minor_version = 0
build_version = 1
in_development = True

version = "%d.%d.%d%s" % (
    major_version,
    minor_version,
    build_version,
    in_development and "+" or ""
)

# for Firefox extension deployment
homepageURL = "http://planes.com/%(app)s" % vars()
updateURL = "%(homepageURL)s/update.rdf" % vars()
updateFile = "%(app)s-%(version)s.xpi" % vars()
updateLink = "%(homepageURL)s/%(updateFile)s" % vars()
firefoxUID = 'ec8030f7-c20a-464f-9b0e-13a3a9e97384'
firefoxMinVersion = '1.0.6'
firefoxMaxVersion = '1.5'

# for XULRunner deployment
geckoMinVersion = '1.8'
geckoMaxVersion = '1.8'
startXul = '@.xul'

overlays = (
    # overlay this on that
    ('%(app)s/content/browser.xul' % vars(), 'browser/content/browser.xul' % vars()),
)
stylesheets = (
    # overlay this on that
)

skins = {
    'classic': {
        'skin_version': '1.0',
        'display_name': name,
    },
}

locales = {
    'en-US': {
        'locale_version': '1.0',
        'display_name': 'English (US)',
    },
}


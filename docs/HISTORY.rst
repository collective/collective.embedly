Changelog
=========

2.2 - Aug 29, 2013
------------------

- Don't cache errors in persistent cache
  [kroman0]

- Added persistent cache and cache timeout
  [kroman0]

2.1 - May 13, 2013
------------------

- Updated embed.ly api url
  [kroman0]

- support urls containing non-asci characters such as
  http://maps.google.com/maps?q=%C3%96sterreich
  (fixes #5)
  [fRiSi]

- added 'Use services regexp' bool field to registry.
  (fixes #4)
  [kroman0]

2.0 - Feb 25, 2013
------------------

- change tests structure
  [kroman0]

- added acceptance tests
  [kroman0]

- added TinyMCE plugin
  [kroman0]

- cleanup genericsetup profiles
  [kroman0]

1.7 - Nov 23, 2011
------------------

- added view for updating embedly services manually

- handling of empty api_key added

- local cache of available services updated

1.6 - Sep 14, 2011
------------------

- Only run the uninstall profile when the product is being uninstalled.
  This allows for the api key to survive through a reinstall.
  [claytron]

- Add support for passing the embedly API key
  [claytron]

1.5 - Sep 2, 2011
-----------------

- href distinguishing regular expression improved
- logging added

1.4.1 - Aug 8, 2011
-------------------

- typpos in CSS fixed

1.4 - Apr 26, 2011
------------------

- URL parameters parsing algorithm updated

1.3 - Apr 05, 2011
------------------

- maxwidth, maxheight, callback, wmode params support added

- updated list of embedly services

1.2 - Mar 29, 2011
------------------

- the embedly link now marked with icon and background in TinyMCE

1.1 - Mar 4, 2011
-----------------

- proper registration of embedly transformation done; does not clash with
  safe HTML transform from now on

1.0 - Mar 3, 2011
-----------------

- Initial release

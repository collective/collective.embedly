Introduction
============

This package provides TinyMCE visual editor support for embed.ly service:
videos, images and other rich media can be inserted to Plone from different
services through one API.

The approach here is to use the Transform machinery to replace the URL with
embed code by calling the embed.ly API.

There are more than 200 services that support embed.ly service. These are such
video sharing sites as Youtube, Blip.tv, Vimeo; such audio streaming services 
as Grooveshark, SoundCloud, last.fm; such image/photo stocks as Flickr, and 
many other: GoogleMaps, Facebook, Twitter, etc.

This product was developed by http://quintagroup.com for Plone collective, 
sponsored by Headnet ApS http://headnet.dk.

Usage
-----

To embed media from the embedly-supported external resource to Plone:

* Go to the object's edit form, select some text and click  
  'Insert/Edit Embedly link' button.

* In the panel add link and configure extra parameters in 'Advanced' tab.
  Check http://embed.ly/docs/arguments for params description.

* The text should now look like linked. TinyMCE makes the whole passage linked, 
  so keep in mind that the whole passage will later be substituted with 
  embedded media.
  
* Save this page. Now when rendered, there will be "preview" from embed.ly 
  service inserted instead of the linked text.

More about usage at http://projects.quintagroup.com/products/wiki/collective.embedly

Note
----

* collective.embedly does not fix errors in provided URLs

* you can check if your URL will be transformed calling embed.ly manualy, for example:

   o video URL http://www.youtube.com/watch?v=L1NPLlhFTVk
   o you should call http://api.embed.ly/1/oembed setting 'url' parameter with your value
   o http://api.embed.ly/1/oembed?url=http://www.youtube.com/watch?v=L1NPLlhFTVk
   o http://api.embed.ly/1/oembed?url=http://www.youtube.com/watch?v=L1NPLlhFTVk&fromat=xml format result as xml

* You can set the API key by going to Site Setup -> Configuration Registry and
  setting the api_key value. The default is to not pass along a key, your
  requests to embedly will be anonymous and based solely on IP address.

Supported Plone Version
-----------------------

* Plone 4.x

Contributors
------------

* Volodymyr Cherepanyak
* Roman Kozlovskyi
* Serhiy Valchuk
* Clayton Parker

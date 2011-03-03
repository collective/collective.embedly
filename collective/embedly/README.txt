This package provides TinyMCE visual editor support for embed.ly service: videos, images and other rich media 
can be inserted to Plone from different services through one API.

The approach here is to use the Transform machinery to replace the URL with embed code by calling the embed.ly API.

There are more than 200 services that support embed.ly service. These are such video sharing sites as Youtube, 
Blip.tv, Vimeo; such audio streaming services as Grooveshark, SoundCloud, last.fm; such image/photo stocks as 
Flickr, and many other: GoogleMaps, Facebook, Twitter, etc.

This product was developed by http://quintagroup.com for Plone collective, sponsored by Headnet company http://headnet.dk.

Usage
-----

 To embed media from the embedly-supported external resource to Plone:

 1. Go to your site HTML Filtering panel (/@@filter-controlpanel) and add tags that are used for embedding content from
    that external service into the list of 'Custom Tags' and remove them from the lists of 'Nasty Tags' and 'Stripped Tags'. 
    These are usually such tags as 'embed', 'object', 'iframe' and others.

 2. Go to the object's edit form, select some text and choose 'Embedly link' style for it.

 3. The text should now look like linked. TinyMCE makes the whole passage linked, so keep in mind that the whole passage 
    will later be substituted with embedded media.
   
 4. Select this text again and go to Insert link to insert the URL to the desired object on the external service.
   
 5. Save this page. Now when rendered, there will be "preview" from embed.ly service inserted instead of the linked text. 

More about usage at http://projects.quintagroup.com/products/wiki/collective.embedly

Supported Plone Version
-----------------------

 Plone 4.0

Author
------

 Roman Kozlovskyi 


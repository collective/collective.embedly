Introduction
============

collective.embedly package provides TinyMCE visual editor support for embed.ly service, so that videos 
can be inserted to Plone from different video streaming services.

The approach here is to use the Transform machinery to replace the URL with embed code by calling the embed.ly API.

This product was developed by  http://quintagroup.com for Plone collective, sponsored by Headnet company http://headnet.dk.

Usage
-----

 1. In your site HTML Filtering panel (/@@filter-controlpanel) remove 'embed' and 'object' from the list of Nasty tags 
    and add them to the list of Custom tags. 

 2. Go to the object's edit form, select some text and choose 'Embedly link' style for it. As a result the text should
    look like linked (TinyMCE makes the whole passage linked).
   
 3. Select this text again and go to Insert link to insert the URL to the desired object (e.g. http://youtube.com/..).

 4. Save this page. Now when rendered, there will be "preview" from embed.ly service inserted instead of the linked text. 

More about usege at http://projects.quintagroup.com/products/wiki/collective.embedly

Supported Plone Version
-----------------------

 * Plone 4.0

Author
------

 * Roman Kozlovskyi 


Some of the data has been retrieved from WMS/Geoserver APIs using GetMap GeoRSS calls. 

But unfortunately GeoRSS can't encode polygons with inner rings and this means that for polygons with holes in them. The wholes couldn't be retrieved.

To overcome this for the cadastral cases, where the data is supposed to be a mosaic of non-overlapping polygons, 
I did write a script which punches holes wherever a complete overlap of polygons is seen, this in a way restores the holes in the polygons. 

I have "corrected" most of the data this way. But, unfortunately not all the data is non-overlapping and not all polygons might have a corresponding filling polygon in the data itself.

So some data is likely still missing and in the case of unexpected overlaps some extraneous holes were introduced. 

I found this better than the existing situation of missing holes completely. So, I am going to let it be. 

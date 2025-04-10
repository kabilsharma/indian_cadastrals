#!/bin/bash

f=$1
new_f="converted_$f"

echo "converting $f"

ogr2ogr -f GeoJSONSEQ $new_f -t_srs EPSG:4326 -s_srs EPSG:3857 GeoJSONSEQ:$f

mv $new_f $f

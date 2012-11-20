#! /bin/sh
#
# Planimeter.cgi
# cgi script for measuring the area of geodesic polygons
#
# Copyright (c) Charles Karney (2011) <charles@karney.com> and licensed
# under the MIT/X11 License.  For more information, see
# http://geographiclib.sourceforge.net/

. ./utils.sh
OPTION=`lookupkey "$QUERY_STRING" option`
if test "$OPTION" = Reset; then
    INPUT=
else
    INPUT=`lookupcheckkey "$QUERY_STRING" input`
    NORM=`lookupkey "$QUERY_STRING" norm`
    TYPE=`lookupkey "$QUERY_STRING" type`
fi
env > /tmp/env

INPUTENC=`encodevalue "$INPUT"`
if test "$TYPE" = "polyline"; then
  LINEFLAG=-l
else
  LINEFLAG=
fi
COMMAND=Planimeter
EXECDIR=../bin
STATUS=
NUM=
LEN=
AREA=
if test "$INPUT"; then
    STATUS=`echo "$INPUT" | head -1 | $EXECDIR/GeoConvert`
    if test $? -eq 0; then
	STATUS=OK
	OUTPUT=`echo "$INPUT" | $EXECDIR/$COMMAND $LINEFLAG | head -1`
	NUM="`echo $OUTPUT | cut -f1 -d' '`"
	LEN="`echo $OUTPUT | cut -f2 -d' '`"
	AREA="`echo $OUTPUT | cut -f3 -d' '`"
	if test "$NORM"; then
	    TRANSFORMEDINPUT=`echo "$INPUT" | $EXECDIR/GeoConvert -p 20 |
	    sed '/^ERROR/,$d'`
	    INPUTENC=`encodevalue "$TRANSFORMEDINPUT"`
	fi
    fi
    # echo `date +"%F %T"` "$COMMAND: $INPUT" >> ../persistent/utilities.log
fi

echo Content-type: text/html
echo
cat <<EOF
<html>
  <head>
    <title>
      Online geodesic planimeter
    </title>
    <meta name="description" content="Online geodesic planimeter" />
    <meta name="author" content="Charles F. F. Karney" />
    <meta name="keywords"
	  content="geodesics,
		   geodesic distance,
		   geodesic area,
		   geographic distance,
		   geographic area,
		   geodesic polygon,
		   shortest path,
		   spheroidal triangle,
		   latitude and longitude,
		   online calculator,
		   WGS84 ellipsoid,
		   GeographicLib" />
  </head>
  <body>
    <h3>
      Online geodesic polygon and polyline calculations using the
      <a href="http://geographiclib.sourceforge.net/html/Planimeter.1.html">
	 Planimeter</a> utility
    </h3>
    <form action="/cgi-bin/Planimeter" method="get">
      <p>
	<input type="radio" name="type" value="polygon"
	       `test "$LINEFLAG" || echo CHECKED`> Polygon
	&nbsp;&nbsp;&nbsp;
	<input type="radio" name="type" value="polyline"
	       `test "$LINEFLAG" && echo CHECKED`> Polyline
      </p>
      <p>
        Enter the vertices as latitude longitude pairs, one per line:
	<br>
        &nbsp;&nbsp;&nbsp;
        <textarea cols=40 rows=15 name="input">$INPUTENC</textarea>
      </p>
      <p>
	<input type="checkbox" name="norm" value="decdegrees"
	       `test "$NORM" && echo CHECKED` />
	Convert vertices to decimal degrees
      </p>
      <p>
        Select action:<br>
        &nbsp;&nbsp;&nbsp;
        <input type="submit" name="option" value="Submit">
        <input type="submit" name="option" value="Reset">
      </p>
      <p>
        Results:<br>
        <font size="4"><pre>
    STATUS             = $STATUS
    number of vertices = $NUM
    Perimeter (m)      = $LEN
    area (m^2)         = $AREA</pre></font>
      </p>
    </form>
    <hr>
    <p>
      In polygon mode,
      <a href="http://geographiclib.sourceforge.net/html/Planimeter.1.html">
        Planimeter</a>
      calculates the perimeter and area of a geodesic polygon for the
      WGS84 ellipsoid.  Counter-clockwise traversal of a polygon results
      in a positive area.  Only simple polygons are supported for the
      area computation.  There is no need to close the polygon.
      Polygons may include one or both poles.  In polyline mode,
      <a href="http://geographiclib.sourceforge.net/html/Planimeter.1.html">
        Planimeter</a>
      calculates the length of the geodesic path joining the points.
    </p>
    <p>
      Give the vertices in terms of latitude and longitude, for example
      (these all refer to the position of Timbuktu):
      <pre>
        16.776 -3.009
        16d47' -3d1'
        W3&deg;0'34" N16&deg;46'33"
        3:0:34W 16:46:33N</pre>
      The coordinates can also be given in UTM, UPS, or MGRS coordinates (see
      the documentation on the
      <a href="http://geographiclib.sourceforge.net/html/GeoConvert.1.html">
	GeoConvert</a>
      utility).  A blank line or a coordinate which cannot be understood
      causes the reading of vertices to be stopped.
    </p>
    <p>
      The result for the perimeter is accurate to about 15&nbsp;nm per
      vertex.  The result for the area is accurate to about
      0.1&nbsp;m<sup>2</sup> per vertex.
    </p>
    <p>
      <a href="http://geographiclib.sourceforge.net/html/Planimeter.1.html">
        Planimeter</a>,
      which is a simple wrapper of the
      <a href="http://geographiclib.sourceforge.net/html/classGeographicLib_1_1Geodesic.html">
        GeographicLib::Geodesic</a> class,
      is one of the utilities provided
      with <a href="http://geographiclib.sourceforge.net/">
        GeographicLib</a>.
      Geodesic areas can also be computed using Javascript; see the
      <a href="../scripts/geod-calc.html">Javascript geodesic
	calculator</a>.
      If you wish to use Planimeter directly,
      <a href="http://sourceforge.net/projects/geographiclib/files/distrib">
        download</a>
      and compile GeographicLib.  The algorithms are described
      in C. F. F. Karney,
      <a href="http://dx.doi.org/10.1007/s00190-012-0578-z"><i>Algorithms for
      geodesics</i></a>,
      J. Geodesy, 2012; DOI:
      <a href="http://dx.doi.org/10.1007/s00190-012-0578-z">
	10.1007/s00190-012-0578-z</a>;
      addenda <a href="http://geographiclib.sf.net/geod-addenda.html">
	geod-addenda.html</a>.
    </p>
    <hr>
    <address>Charles Karney
      <a href="mailto:charles@karney.com">&lt;charles@karney.com&gt;</a>
      (2011-08-14)</address>
    <a href="http://geographiclib.sourceforge.net">
      <img
	 src="http://sourceforge.net/sflogo.php?group_id=283628&amp;type=9"
	 border="0" height="15" width="80" alt="SourceForge.net" />
    </a>
  </body>
</html>
EOF

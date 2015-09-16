from appfd.models import *
from csv import reader
from django.contrib.gis.geos import Point
from django.db import connection

def run():
    print "running loadGeoNames"

    # most have user create fdw extension with
    # CREATE EXTENSION file_fdw;

    # deletes all rows from place table`
    #TRUNCATE appfd_place CASCADE;
#    Place.objects.all().delete()
    cursor = connection.cursor()
    c.execute("""
    COPY appfd_geoname
    FROM '/home/usrfd/data/geonames/allCountries.txt'
    WITH (FORMAT 'text', DELIMITER E'\t', NULL 'NULL');
    """)
 
#    cursor.execute("""
"""        CREATE SERVER geoname_server FOREIGN DATA WRAPPER file_fdw;
        CREATE FOREIGN TABLE appfd_geoname (
            geonameid integer,
            name varchar(200),
            asciiname varchar(200),
            alternatenames varchar(10000),
            latitude decimal(8),
            longitude decimal(8),
            feature_class char(1),
            feature_code varchar(10),
            country_code varchar(2),
            cc2 varchar(200),
            admin1_code varchar(20),
            admin2_code varchar(80),
            admin3_code varchar(20),
            admin4_code varchar(20),
            population bigint,
            elevation integer,
            dem integer,
            timezone varchar(40),
            modification_date varchar(40)
        )
        SERVER geoname_server
        OPTIONS ( filename '/home/usrfd/data/geonames/allCountries.txt', format 'text' );

    INSERT INTO appfd_place (geonameid, name, point) SELECT geonameid, name, ST_SetSRID(ST_POINT(longitude, latitude), 4326) FROM appfd_geoname LIMIT 10;


     this command runs it in the background
sudo -u postgres psql -c "INSERT INTO appfd_place (geonameid, name, point) SELECT geonameid, name, ST_SetSRID(ST_POINT(longitude, latitude), 4326) FROM appfd_geoname;" dbfd &

sudo -u postgres psql -c "CREATE INDEX name_idx ON appfd_place (name);" dbfd &

CREATE INDEX name_idx ON appfd_place USING gin(to_tsvector(name));


"""
#""")
#    c.execute("""
#    COPY appfd_place (,,,null,column0,null,null,column1)
#    FROM '/home/usrfd/data/geonames/allCountries.txt'
#    WITH (FORMAT 'text', DELIMITER E'\t', NULL 'NULL');
#    """)
 
#    cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
#    cursor.execute("""
#LOAD DATA INFILE "/home/usrfd/data/geonames/allCountries.txt"
#INTO TABLE appfd_place 
#CHARACTER SET 'utf8'
#FIELDS TERMINATED BY '\t'
#
#    """
    """
    counter = 0
    with open("/home/usrfd/data/geonames/allCountries.txt", "r") as f:
        for line in f:
            #print "line is", line
            line_split = line.strip().split("\t")
            #print "line_split is", line_split
           # #print "geonameid = ", int(line_split[0])
            place = Place.objects.get_or_create(geonameid=int(line_split[0]))[0]
            place.name = line_split[1]
            #print "place.name is", line_split[1]
            place.point = Point(x=float(line_split[5]),y=float(line_split[4])) 
            place.save()

            #print counter, "-"
            counter += 1
            if counter % 1000 == 0:
                print counter
            else:
               counter += 1
  
    """
    #f = open("/home/usrfd/data/geonames/allCountries.txt", "r")
    #Entry.objects.bulk_create([Place(geonameid=line[0],name=line[1],point=Point(x=float(line[5]),y=float(line[4]))) for line in csv.reader(f, delimiter='\t', quotechar='|')])
    #f.close()

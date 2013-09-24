BATYFILE=wider_area_bathymetry.nc
OUTFILE=meshmetric_UTM.nc

module load gmt
gdalwarp -s_srs "EPSG:4326" -t_srs "EPSG:22332" -of netCDF $BATYFILE $OUTFILE
grdmath $OUTFILE 0 EQ 1000 MUL $OUTFILE 200 MUL ADD = $OUTFILE

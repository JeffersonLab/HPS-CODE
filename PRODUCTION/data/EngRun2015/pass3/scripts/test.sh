
java='/apps/scicomp/java/jdk1.7/bin/java -XX:+UseSerialGC'
jar='/u/group/hps/hps_soft/hps-java/hps-distribution-3.4.1-20151005.231744-88-bin.jar'
recon='/org/hps/steering/recon/EngineeringRun2015FullRecon_Pass2.lcsim'
evio='hps_005772.evio.100'
dq='/org/hps/steering/production/DataQuality.lcsim'
dqm='/org/hps/steering/production/DataQualityRecon_Pass2.lcsim'
fee='/org/hps/steering/production/FEEFilter.lcsim'
dstmkr='/u/group/hps/hps_soft/hps-dst/build/bin/dst_maker'


date

#$java \
#    -cp $jar \
#    -x $recon \
#    -r -d HPS-EngRun2015-Nominal-v3-1-fieldmap \
#    -R 5772 \
#    -DoutputFile=out \
#    $evio \
#    >& recon.log

#$java \
#    -jar $jar \
#    -r $dq \
#    -i out.slcio \
#    > dq.txt

#$java \
#    -Xmx2000m 
#    -jar $jar \
#    -r $dqm \
#    -DoutputFile=dqm \
#    -i out.slcio

#$dstmkr out.slcio -o dst.root -g -b 0.24

$java \
    -jar $jar \
    -r $fee \
    -DoutputFile=fee \
    -i out.slcio


date



#!/usr/bin/perl

$list_file = @ARGV[0];

@files = `cat $list_file`;

for $cur_file (@files){
    
    chop($cur_file);

    system("unlink /lustre/expphy/stage/hps/mss/hallb/hps/engrun2015/tweakpass6/skim/dst/pulser/$cur_file");

}

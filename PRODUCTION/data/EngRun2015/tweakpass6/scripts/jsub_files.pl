#!/usr/bin/perl

$js_dir = @ARGV[0];

system("mkdir ReSubmitted");

@files = `ls $js_dir/*.xml | sort`;


foreach $cur_file (@files){
    chop($cur_file);
    $jsub_command = "jsub -xml $cur_file";
    $cp_command = "cp -f $cur_file ReSubmitted/";
    system($jsub_command);
    system($cp_command);
    
}

#!/bin/sh

farm_out=$1

scriptDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pass=`echo $scriptDir | awk -F/ '{print$(NF-1)}'`

runtype=all

for xx in $farm_out/*.out*
do
  run=${xx%%$pass.*}
  run=${run##*$runtype}
  echo -n "$xx $run "
  if [ ${xx: -3} == ".gz" ]
  then
      view='gunzip -c'
  else
      view='cat'
  fi
  #echo $xx
  $view $xx |\
    grep -A1 '^Resource usage summary' |\
    tail -1 |\
    awk -F= '{print$5}' |\
    awk -F: '{print($1*60*60+$2*60+$3*60)/60/60}'
done


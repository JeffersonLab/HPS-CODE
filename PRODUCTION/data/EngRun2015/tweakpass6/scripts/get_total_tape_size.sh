grep "size=" skim/moller/hps_00*.slcio | awk '{split($1, a, "="); print a[2]}'

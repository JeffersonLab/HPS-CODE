#!/bin/csh -f

#set files="`${1}*.xml`"
echo ${1}
foreach f (`ls ${1}*.xml`)
    echo "$f"
    jsub -xml $f
#    break
end

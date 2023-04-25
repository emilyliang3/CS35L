#!/bin/bash
shellpid=$(echo $$)
echo "Current login shell process: "
ps $shellpid
echo "Ancestor processes: "
currppid=$(ps o ppid= $shellpid)
while test "$currppid" -ne 0
do ps $currppid
   currppid=$(ps o ppid= $currppid)
done   
echo "Descendant processes: "
childpids=$(ps --ppid $shellpid o pid=)
childpids=$(echo -n $childpids)
while ! test -z "$childpids"
do currpids="$childpids"
#   echo "currpids:"
#   echo $currpids
   childpids=""
   for pid in $currpids
   do childpids="$childpids $(ps --ppid $pid o pid=)"
      echo "pid:"
      echo $pid
      ps $pid
   done
done




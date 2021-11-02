 #!/bin/bash


compile=false #false
run_pulse=true
run_c4mip=false #false

profile=gfortran

modeldir=.
numerics=(D1I)

if $compile
then
    for numeric in ${numerics[*]}
    do 
        ln -sf "control_${numeric}.inc" ./$modeldir/src/control.inc
        make -C ./$modeldir clean
        make -C ./$modeldir profile=$profile
        mv ./$modeldir/bernSCM ./$modeldir/bernSCM$numeric
    done
fi

if $run_pulse
then
    mkdir -p $modeldir/output
    cd $modeldir
# Pulse example
    
    for files in $(ls $modeldir/runfiles -p |grep -v /|grep "^run_pulse_1yr*")
    do 
        ./bernSCM${numerics[0]}  <runfiles/$files
    done    
    cd -
fi


if $run_c4mip
then
    cd $modeldir
# C4MIP example
    runfiles=(run_c4mip_Conly  run_c4mip_coupled  run_c4mip_Tonly  run_c4mip_uncoupled)
    for i in 0 1 2 3
    do for numeric in ${numerics[*]}
        do
            ./bernSCM${numeric} < runfiles/${runfiles[$i]}
        done
    done
    cd -
fi


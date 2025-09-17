transcript off
onbreak {quit -force}
onerror {quit -force}
transcript on

asim +access +r +m+inter_spartan  -L xil_defaultlib -L unisims_ver -L unimacro_ver -L secureip -O5 xil_defaultlib.inter_spartan xil_defaultlib.glbl

do {inter_spartan.udo}

run 1000ns

endsim

quit -force

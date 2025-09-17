transcript off
onbreak {quit -force}
onerror {quit -force}
transcript on

vlib work
vlib activehdl/xil_defaultlib

vmap xil_defaultlib activehdl/xil_defaultlib

vlog -work xil_defaultlib  -sv2k12 "+incdir+../../../uart_ascon_light_el.gen/sources_1/ip/clk_wiz_1" -l xil_defaultlib \
"../../../uart_ascon_light_el.srcs/sources_1/imports/fsmAscon/ASCON.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/RTL2/ascon_pack.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/Sources_ascon-20250324/ascon_pack.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/Sources_ascon-20250324/Pc.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/Sources_ascon-20250324/Permutation.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/Sources_ascon-20250324/Pl.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/Sources_ascon-20250324/Ps.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/Sources_ascon-20250324/Sbox.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/RTL2/uart_pkg.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/RTL2/ad_reg.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/Sources_ascon-20250324/ascon.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/RTL2/ascon_reg.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/RTL2/baud_generator.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/RTL2/cipher_reg.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/fsmAscon/compteur.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/Sources_ascon-20250324/compteur_double_init.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/fsmAscon/fsm.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/RTL2/fsm_dcounter.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/Sources_ascon-20250324/fsm_moore.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/RTL2/fsm_uart.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/RTL2/key_reg.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/Sources_ascon-20250324/mux_state.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/RTL2/nonce_reg.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/RTL2/receive.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/RTL2/reg_sel.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/Sources_ascon-20250324/register_w_en.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/RTL2/rx_reg.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/RTL2/rxbit_dcounter.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/Sources_ascon-20250324/state_register_w_en.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/RTL2/tag_reg.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/RTL2/trans_receive.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/RTL2/transmit.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/RTL2/tx_reg.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/RTL2/txbit_dcounter.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/RTL2/uart_core.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/RTL2/wave_reg.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/Sources_ascon-20250324/xor_begin_perm.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/Sources_ascon-20250324/xor_end_perm.sv" \
"../../../uart_ascon_light_el.srcs/sources_1/imports/RTL2/inter_spartan.sv" \


vlog -work xil_defaultlib \
"glbl.v"


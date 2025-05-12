v {xschem version=3.4.6RC file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N -130 -60 -130 -30 {lab=#net1}
N 40 -60 40 -30 {lab=#net2}
N -90 -60 40 -60 {lab=#net2}
N 210 -60 210 -30 {lab=#net3}
N 80 -60 210 -60 {lab=#net3}
N 380 -60 380 -30 {lab=#net4}
N 250 -60 380 -60 {lab=#net4}
N 520 120 520 150 {lab=OUT}
N 350 120 350 150 {lab=#net5}
N 350 120 480 120 {lab=#net5}
N 180 120 180 150 {lab=#net6}
N 180 120 310 120 {lab=#net6}
N 10 120 10 150 {lab=#net7}
N 10 120 140 120 {lab=#net7}
N -160 120 -160 150 {lab=#net8}
N -160 120 -30 120 {lab=#net8}
N 570 -60 570 120 {lab=OUT}
N 40 -90 40 -60 {lab=#net2}
N 210 -90 210 -60 {lab=#net3}
N 380 -90 380 -60 {lab=#net4}
N 350 90 350 120 {lab=#net5}
N 180 90 180 120 {lab=#net6}
N 10 90 10 120 {lab=#net7}
N -160 90 -160 120 {lab=#net8}
N 520 90 520 120 {lab=OUT}
N -130 -90 -130 -60 {lab=#net1}
N -280 120 -200 120 {lab=#net1}
N 520 120 570 120 {lab=OUT}
N 420 -60 570 -60 {lab=OUT}
N -280 -60 -130 -60 {lab=#net1}
N -280 -60 -280 120 {lab=#net1}
C {ipin.sym} -450 -90 0 0 {name=p19 lab=VGND}
C {ipin.sym} -450 -70 0 0 {name=p20 lab=VNB}
C {ipin.sym} -450 -50 0 0 {name=p21 lab=VPB}
C {ipin.sym} -450 -30 0 0 {name=p22 lab=VPWR}
C {opin.sym} 570 0 0 0 {name=p2 lab=OUT}
C {sky130_fd_pr/nfet_01v8.sym} -110 -30 0 0 {name=M18
W=420000u
L=150000u
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 60 -30 2 1 {name=M7
W=420000u
L=150000u
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} -110 -30 0 0 {name=M8
W=420000u
L=150000u
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_hvt.sym} -110 -90 0 0 {name=M9
W=640000u
L=150000u
model=pfet_01v8_hvt
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_hvt.sym} 60 -90 2 1 {name=M10
W=640000u
L=150000u
model=pfet_01v8_hvt
spiceprefix=X
}
C {lab_pin.sym} -90 -90 2 0 {name=p1 sig_type=std_logic lab=VPB}
C {lab_pin.sym} -90 -30 2 0 {name=p15 sig_type=std_logic lab=VNB}
C {lab_pin.sym} -90 0 2 0 {name=p16 sig_type=std_logic lab=VGND}
C {lab_pin.sym} -90 -120 2 0 {name=p17 sig_type=std_logic lab=VPWR}
C {lab_pin.sym} 80 -90 2 0 {name=p18 sig_type=std_logic lab=VPB}
C {lab_pin.sym} 80 -30 2 0 {name=p23 sig_type=std_logic lab=VNB}
C {lab_pin.sym} 80 0 2 0 {name=p24 sig_type=std_logic lab=VGND}
C {lab_pin.sym} 80 -120 2 0 {name=p25 sig_type=std_logic lab=VPWR}
C {sky130_fd_pr/nfet_01v8.sym} 230 -30 2 1 {name=M11
W=420000u
L=150000u
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_hvt.sym} 230 -90 2 1 {name=M12
W=640000u
L=150000u
model=pfet_01v8_hvt
spiceprefix=X
}
C {lab_pin.sym} 250 -90 2 0 {name=p34 sig_type=std_logic lab=VPB}
C {lab_pin.sym} 250 -30 2 0 {name=p35 sig_type=std_logic lab=VNB}
C {lab_pin.sym} 250 0 2 0 {name=p36 sig_type=std_logic lab=VGND}
C {lab_pin.sym} 250 -120 2 0 {name=p37 sig_type=std_logic lab=VPWR}
C {sky130_fd_pr/nfet_01v8.sym} 400 -30 2 1 {name=M13
W=420000u
L=150000u
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_hvt.sym} 400 -90 2 1 {name=M14
W=640000u
L=150000u
model=pfet_01v8_hvt
spiceprefix=X
}
C {lab_pin.sym} 420 -90 2 0 {name=p38 sig_type=std_logic lab=VPB}
C {lab_pin.sym} 420 -30 2 0 {name=p39 sig_type=std_logic lab=VNB}
C {lab_pin.sym} 420 0 2 0 {name=p40 sig_type=std_logic lab=VGND}
C {lab_pin.sym} 420 -120 2 0 {name=p41 sig_type=std_logic lab=VPWR}
C {sky130_fd_pr/pfet_01v8_hvt.sym} -180 90 2 0 {name=M30
W=640000u
L=150000u
model=pfet_01v8_hvt
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 330 150 2 0 {name=M31
W=420000u
L=150000u
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 500 150 0 1 {name=M32
W=420000u
L=150000u
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_hvt.sym} 500 90 0 1 {name=M33
W=640000u
L=150000u
model=pfet_01v8_hvt
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_hvt.sym} 330 90 2 0 {name=M34
W=640000u
L=150000u
model=pfet_01v8_hvt
spiceprefix=X
}
C {lab_pin.sym} 480 90 2 1 {name=p66 sig_type=std_logic lab=VPB}
C {lab_pin.sym} 480 150 2 1 {name=p67 sig_type=std_logic lab=VNB}
C {lab_pin.sym} 480 180 2 1 {name=p68 sig_type=std_logic lab=VGND}
C {lab_pin.sym} 480 60 2 1 {name=p69 sig_type=std_logic lab=VPWR}
C {lab_pin.sym} 310 90 2 1 {name=p70 sig_type=std_logic lab=VPB}
C {lab_pin.sym} 310 150 2 1 {name=p71 sig_type=std_logic lab=VNB}
C {lab_pin.sym} 310 180 2 1 {name=p72 sig_type=std_logic lab=VGND}
C {lab_pin.sym} 310 60 2 1 {name=p73 sig_type=std_logic lab=VPWR}
C {sky130_fd_pr/nfet_01v8.sym} 160 150 2 0 {name=M35
W=420000u
L=150000u
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_hvt.sym} 160 90 2 0 {name=M36
W=640000u
L=150000u
model=pfet_01v8_hvt
spiceprefix=X
}
C {lab_pin.sym} 140 90 2 1 {name=p74 sig_type=std_logic lab=VPB}
C {lab_pin.sym} 140 150 2 1 {name=p75 sig_type=std_logic lab=VNB}
C {lab_pin.sym} 140 180 2 1 {name=p76 sig_type=std_logic lab=VGND}
C {lab_pin.sym} 140 60 2 1 {name=p77 sig_type=std_logic lab=VPWR}
C {sky130_fd_pr/nfet_01v8.sym} -10 150 2 0 {name=M37
W=420000u
L=150000u
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_hvt.sym} -10 90 2 0 {name=M38
W=640000u
L=150000u
model=pfet_01v8_hvt
spiceprefix=X
}
C {lab_pin.sym} -30 90 2 1 {name=p78 sig_type=std_logic lab=VPB}
C {lab_pin.sym} -30 150 2 1 {name=p79 sig_type=std_logic lab=VNB}
C {lab_pin.sym} -30 180 2 1 {name=p80 sig_type=std_logic lab=VGND}
C {lab_pin.sym} -30 60 2 1 {name=p81 sig_type=std_logic lab=VPWR}
C {sky130_fd_pr/nfet_01v8.sym} -180 150 2 0 {name=M39
W=420000u
L=150000u
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_hvt.sym} -180 90 2 0 {name=M40
W=640000u
L=150000u
model=pfet_01v8_hvt
spiceprefix=X
}
C {lab_pin.sym} -200 90 2 1 {name=p82 sig_type=std_logic lab=VPB}
C {lab_pin.sym} -200 150 2 1 {name=p83 sig_type=std_logic lab=VNB}
C {lab_pin.sym} -200 180 2 1 {name=p84 sig_type=std_logic lab=VGND}
C {lab_pin.sym} -200 60 2 1 {name=p85 sig_type=std_logic lab=VPWR}
C {ipin.sym} -450 -110 0 0 {name=p11 lab=UNUSED}

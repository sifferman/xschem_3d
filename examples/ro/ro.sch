v {xschem version=3.4.6RC file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N -240 -90 -240 -30 {lab=#net1}
N -70 -90 -70 -30 {lab=#net2}
N -200 -60 -70 -60 {lab=#net2}
N 100 -90 100 -30 {lab=#net3}
N -30 -60 100 -60 {lab=#net3}
N 270 -90 270 -30 {lab=#net4}
N 140 -60 270 -60 {lab=#net4}
N -240 -90 -240 -30 {lab=#net1}
N -70 -90 -70 -30 {lab=#net2}
N -200 -60 -70 -60 {lab=#net2}
N 100 -90 100 -30 {lab=#net3}
N -30 -60 100 -60 {lab=#net3}
N 270 -90 270 -30 {lab=#net4}
N 140 -60 270 -60 {lab=#net4}
N 520 90 520 150 {lab=OUT}
N 350 90 350 150 {lab=#net5}
N 350 120 480 120 {lab=#net5}
N 180 90 180 150 {lab=#net6}
N 180 120 310 120 {lab=#net6}
N 10 90 10 150 {lab=#net7}
N 10 120 140 120 {lab=#net7}
N -160 90 -160 150 {lab=#net8}
N -160 120 -30 120 {lab=#net8}
N 520 90 520 150 {lab=OUT}
N 350 90 350 150 {lab=#net5}
N 350 120 480 120 {lab=#net5}
N 180 90 180 150 {lab=#net6}
N 180 120 310 120 {lab=#net6}
N 10 90 10 150 {lab=#net7}
N 10 120 140 120 {lab=#net7}
N -160 90 -160 150 {lab=#net8}
N -160 120 -30 120 {lab=#net8}
N 520 120 580 120 {lab=OUT}
N 580 -60 580 120 {lab=OUT}
N -300 120 -200 120 {lab=#net1}
N -300 -60 -300 120 {lab=#net1}
N -300 -60 -240 -60 {lab=#net1}
N 310 -60 580 -60 {lab=OUT}
C {ipin.sym} -450 -90 0 0 {name=p19 lab=VGND}
C {ipin.sym} -450 -70 0 0 {name=p20 lab=VNB}
C {ipin.sym} -450 -50 0 0 {name=p21 lab=VPB}
C {ipin.sym} -450 -30 0 0 {name=p22 lab=VPWR}
C {opin.sym} 580 0 0 0 {name=p2 lab=OUT}
C {sky130_fd_pr/nfet_01v8.sym} -50 -30 2 1 {name=M16
W=420000u
L=150000u
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} -220 -30 0 0 {name=M18
W=420000u
L=150000u
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_hvt.sym} -220 -90 0 0 {name=M19
W=640000u
L=150000u
model=pfet_01v8_hvt
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_hvt.sym} -50 -90 2 1 {name=M20
W=640000u
L=150000u
model=pfet_01v8_hvt
spiceprefix=X
}
C {lab_pin.sym} -200 -90 2 0 {name=p26 sig_type=std_logic lab=VPB}
C {lab_pin.sym} -200 -30 2 0 {name=p27 sig_type=std_logic lab=VNB}
C {lab_pin.sym} -200 0 2 0 {name=p28 sig_type=std_logic lab=VGND}
C {lab_pin.sym} -200 -120 2 0 {name=p29 sig_type=std_logic lab=VPWR}
C {lab_pin.sym} -30 -90 2 0 {name=p30 sig_type=std_logic lab=VPB}
C {lab_pin.sym} -30 -30 2 0 {name=p31 sig_type=std_logic lab=VNB}
C {lab_pin.sym} -30 0 2 0 {name=p32 sig_type=std_logic lab=VGND}
C {lab_pin.sym} -30 -120 2 0 {name=p33 sig_type=std_logic lab=VPWR}
C {sky130_fd_pr/nfet_01v8.sym} 120 -30 2 1 {name=M1
W=420000u
L=150000u
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_hvt.sym} 120 -90 2 1 {name=M2
W=640000u
L=150000u
model=pfet_01v8_hvt
spiceprefix=X
}
C {lab_pin.sym} 140 -90 2 0 {name=p3 sig_type=std_logic lab=VPB}
C {lab_pin.sym} 140 -30 2 0 {name=p4 sig_type=std_logic lab=VNB}
C {lab_pin.sym} 140 0 2 0 {name=p5 sig_type=std_logic lab=VGND}
C {lab_pin.sym} 140 -120 2 0 {name=p6 sig_type=std_logic lab=VPWR}
C {sky130_fd_pr/nfet_01v8.sym} 290 -30 2 1 {name=M3
W=420000u
L=150000u
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_hvt.sym} 290 -90 2 1 {name=M4
W=640000u
L=150000u
model=pfet_01v8_hvt
spiceprefix=X
}
C {lab_pin.sym} 310 -90 2 0 {name=p7 sig_type=std_logic lab=VPB}
C {lab_pin.sym} 310 -30 2 0 {name=p8 sig_type=std_logic lab=VNB}
C {lab_pin.sym} 310 0 2 0 {name=p9 sig_type=std_logic lab=VGND}
C {lab_pin.sym} 310 -120 2 0 {name=p10 sig_type=std_logic lab=VPWR}
C {sky130_fd_pr/nfet_01v8.sym} -50 -30 2 1 {name=M7
W=420000u
L=150000u
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} -220 -30 0 0 {name=M8
W=420000u
L=150000u
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_hvt.sym} -220 -90 0 0 {name=M9
W=640000u
L=150000u
model=pfet_01v8_hvt
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_hvt.sym} -50 -90 2 1 {name=M10
W=640000u
L=150000u
model=pfet_01v8_hvt
spiceprefix=X
}
C {lab_pin.sym} -200 -90 2 0 {name=p1 sig_type=std_logic lab=VPB}
C {lab_pin.sym} -200 -30 2 0 {name=p15 sig_type=std_logic lab=VNB}
C {lab_pin.sym} -200 0 2 0 {name=p16 sig_type=std_logic lab=VGND}
C {lab_pin.sym} -200 -120 2 0 {name=p17 sig_type=std_logic lab=VPWR}
C {lab_pin.sym} -30 -90 2 0 {name=p18 sig_type=std_logic lab=VPB}
C {lab_pin.sym} -30 -30 2 0 {name=p23 sig_type=std_logic lab=VNB}
C {lab_pin.sym} -30 0 2 0 {name=p24 sig_type=std_logic lab=VGND}
C {lab_pin.sym} -30 -120 2 0 {name=p25 sig_type=std_logic lab=VPWR}
C {sky130_fd_pr/nfet_01v8.sym} 120 -30 2 1 {name=M11
W=420000u
L=150000u
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_hvt.sym} 120 -90 2 1 {name=M12
W=640000u
L=150000u
model=pfet_01v8_hvt
spiceprefix=X
}
C {lab_pin.sym} 140 -90 2 0 {name=p34 sig_type=std_logic lab=VPB}
C {lab_pin.sym} 140 -30 2 0 {name=p35 sig_type=std_logic lab=VNB}
C {lab_pin.sym} 140 0 2 0 {name=p36 sig_type=std_logic lab=VGND}
C {lab_pin.sym} 140 -120 2 0 {name=p37 sig_type=std_logic lab=VPWR}
C {sky130_fd_pr/nfet_01v8.sym} 290 -30 2 1 {name=M13
W=420000u
L=150000u
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_hvt.sym} 290 -90 2 1 {name=M14
W=640000u
L=150000u
model=pfet_01v8_hvt
spiceprefix=X
}
C {lab_pin.sym} 310 -90 2 0 {name=p38 sig_type=std_logic lab=VPB}
C {lab_pin.sym} 310 -30 2 0 {name=p39 sig_type=std_logic lab=VNB}
C {lab_pin.sym} 310 0 2 0 {name=p40 sig_type=std_logic lab=VGND}
C {lab_pin.sym} 310 -120 2 0 {name=p41 sig_type=std_logic lab=VPWR}
C {sky130_fd_pr/nfet_01v8.sym} 330 150 2 0 {name=M21
W=420000u
L=150000u
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 500 150 0 1 {name=M22
W=420000u
L=150000u
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_hvt.sym} 500 90 0 1 {name=M23
W=640000u
L=150000u
model=pfet_01v8_hvt
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_hvt.sym} 330 90 2 0 {name=M24
W=640000u
L=150000u
model=pfet_01v8_hvt
spiceprefix=X
}
C {lab_pin.sym} 480 90 2 1 {name=p46 sig_type=std_logic lab=VPB}
C {lab_pin.sym} 480 150 2 1 {name=p47 sig_type=std_logic lab=VNB}
C {lab_pin.sym} 480 180 2 1 {name=p48 sig_type=std_logic lab=VGND}
C {lab_pin.sym} 480 60 2 1 {name=p49 sig_type=std_logic lab=VPWR}
C {lab_pin.sym} 310 90 2 1 {name=p50 sig_type=std_logic lab=VPB}
C {lab_pin.sym} 310 150 2 1 {name=p51 sig_type=std_logic lab=VNB}
C {lab_pin.sym} 310 180 2 1 {name=p52 sig_type=std_logic lab=VGND}
C {lab_pin.sym} 310 60 2 1 {name=p53 sig_type=std_logic lab=VPWR}
C {sky130_fd_pr/nfet_01v8.sym} 160 150 2 0 {name=M25
W=420000u
L=150000u
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_hvt.sym} 160 90 2 0 {name=M26
W=640000u
L=150000u
model=pfet_01v8_hvt
spiceprefix=X
}
C {lab_pin.sym} 140 90 2 1 {name=p54 sig_type=std_logic lab=VPB}
C {lab_pin.sym} 140 150 2 1 {name=p55 sig_type=std_logic lab=VNB}
C {lab_pin.sym} 140 180 2 1 {name=p56 sig_type=std_logic lab=VGND}
C {lab_pin.sym} 140 60 2 1 {name=p57 sig_type=std_logic lab=VPWR}
C {sky130_fd_pr/nfet_01v8.sym} -10 150 2 0 {name=M27
W=420000u
L=150000u
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_hvt.sym} -10 90 2 0 {name=M28
W=640000u
L=150000u
model=pfet_01v8_hvt
spiceprefix=X
}
C {lab_pin.sym} -30 90 2 1 {name=p58 sig_type=std_logic lab=VPB}
C {lab_pin.sym} -30 150 2 1 {name=p59 sig_type=std_logic lab=VNB}
C {lab_pin.sym} -30 180 2 1 {name=p60 sig_type=std_logic lab=VGND}
C {lab_pin.sym} -30 60 2 1 {name=p61 sig_type=std_logic lab=VPWR}
C {sky130_fd_pr/nfet_01v8.sym} -180 150 2 0 {name=M29
W=420000u
L=150000u
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_hvt.sym} -180 90 2 0 {name=M30
W=640000u
L=150000u
model=pfet_01v8_hvt
spiceprefix=X
}
C {lab_pin.sym} -200 90 2 1 {name=p62 sig_type=std_logic lab=VPB}
C {lab_pin.sym} -200 150 2 1 {name=p63 sig_type=std_logic lab=VNB}
C {lab_pin.sym} -200 180 2 1 {name=p64 sig_type=std_logic lab=VGND}
C {lab_pin.sym} -200 60 2 1 {name=p65 sig_type=std_logic lab=VPWR}
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

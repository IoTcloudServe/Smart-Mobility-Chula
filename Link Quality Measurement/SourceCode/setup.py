
Pi1 ='10.0.0.1'
Pi2 ='10.0.0.2'
Pi3 ='10.0.0.3'
Pi4 ='10.0.0.4'
Pi5 ='10.0.0.5'
Pi6 ='10.0.0.6'
GW1 ='10.0.0.8'
GW2 ='10.0.0.9'

R1=[GW1,Pi1]
R2=[GW1,Pi4]
R3=[Pi1,Pi4]
R4=[Pi1,Pi2]
R5=[Pi4,Pi5]
R6=[Pi2,Pi5]
R7=[Pi3,Pi2]
R8=[Pi6,Pi5]
R9=[Pi3,Pi6]
R10=[GW2,Pi3]
R11=[GW2,Pi6]

N = 10
S1=[R1]
S2=[R2]
S3=[R3,R9]
S4=[R4]
S5=[R5]
S6=[R6]
S7=[R7]
S8=[R8]
S9=[R10]
S10=[R11]
S=[S1,S2,S3,S4,S5,S6,S7,S8,S9,S10]

name1=["R1"]
name2=["R2"]
name3=["R3","R9"]
name4=["R4"]
name5=["R5"]
name6=["R6"]
name7=["R7"]
name8=["R8"]
name9=["R10"]
name10=["R11"]
Name=[name1,name2,name3,name4,name5,name6,name7,name8,name9,name10]

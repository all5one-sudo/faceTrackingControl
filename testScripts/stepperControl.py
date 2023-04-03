Qm=0;
b=0;
a=0;
Q=pi32.5/180;
To=0.12;
b1=0;
b2=0;
b3=0;
b4=0;
while E>=pi/200 or E<=-pi/200:

    e=E;

    if e<pi/200 and e>-pi/200:
        break

    T=QTo/abs(e);

    if e>0:
        b=0;
        if a==4:
            a=1;
        else:
            a=a+1;
    elif e<0:
        b=1;
        if a==1:
            a=4;
        else:
            a=a-1;

    #Caso 1

    if a==1:
        b2=0;
        b3=0;
        b4=0;
        b1=1;
        if b==0:
            Qm=Qm+pi/100;
        else:
            Qm=Qm-pi/100;

    #Caso 2

    if a==2:
        b1=0;
        b2=0;
        b4=0;
        b3=1;
        if b==0:
            Qm=Qm+pi/100;
        else:
            Qm=Qm-pi/100;

    #Caso 3

    if a==3:
        b1=0;
        b3=0;
        b4=0;
        b2=1;
        if b==0:
            Qm=Qm+pi/100;
        else:
            Qm=Qm-pi/100;

    #Caso 4

    if a==4:
        b1=0;
        b2=0;
        b3=0;
        b4=1;
        if b==0:
            Qm=Qm+pi/100;
        else:
            Qm=Qm-pi/100;

    time.sleep(To/4)

#Fin del while


for x in range(1,10):
    for y in range(1,10):
        for a in range(1,10):
            for b in range(1,10):
                for c in range(1,10):
                    for d in range(1,10):
                        for z in range(1,10):
                            for w in range(1,10):
                                for t in range(1,10):
                                    if ((10*x)+y)*a ==(10*b)+c and (10*b)+c+(10*d)+z==(10*w)+t:
                                        if x*y*a*b*c*d*z*w*t==362880:
                                            print (x,y,a,b,c,d,z,w,t)

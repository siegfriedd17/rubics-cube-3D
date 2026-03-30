def darken(rgb, rate=0.6):
    rgb=rgb[1::]
    s=[]
    for i in [0,2,4]:
        c = rgb[i:i+2]
        c = int(c, 16)
        print(c)
        print('----')
        c = int(c * rate)
        s.append(c)
    return s

print(darken('#C1093D'))
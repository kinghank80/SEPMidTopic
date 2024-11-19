a = '04-05'.split('-')
b = '04-05'.split('-')

if( ( int(b[0])>=int(a[0]) and int(b[0])<=int(a[1]) ) or ( int(b[1])>=int(a[0]) and int(b[1])<=int(a[1]) ) or ( int(a[0])>=int(b[0]) and int(a[0])<=int(b[1]) ) or ( int(a[1])>=int(b[0]) and int(a[1])<=int(b[1]) )) : # not done here
    print('yes')
else : print('no')
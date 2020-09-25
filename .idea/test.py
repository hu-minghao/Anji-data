from intervals import IntInterval, IntervalSet
inter1 = IntInterval.open(2,3)
inter2 = IntInterval.open(6,7)
interSet =  IntervalSet([inter1, inter2])
if 2.5 in inter1:
    print('True')
else:
    print('False')

import time

def fmat_stamp(t):
	ti = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t / 1000))
	return ti


if __name__ == '__main__':
	t1 = 0
	# t2 = t1 - 86400000
	# t3 = t2 - 86400000
	# t4 = t3 - 86400000
	r1 = fmat_stamp(t1)
	print(r1)
	# r2 = fmat_stamp(t2)
	# r3 = fmat_stamp(t3)
	# r4 = fmat_stamp(t4)
	# print(r1)
	# print(r2)
	# print(r3)
	# print(r4)
	# a = time.mktime(time.strptime('2017-08-09 00:00:00', "%Y-%m-%d %H:%M:%S"))*1000
	# b = time.mktime(time.strptime('2017-06-08 23:59:59', "%Y-%m-%d %H:%M:%S"))*1000
	#
	# print(a)
	# print(b)


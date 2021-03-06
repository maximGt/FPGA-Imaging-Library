__author__ = 'Dai Tianyu (dtysky)'
# Generateing LUTs for sin and cos.
from math import sin, cos, radians

# Convert num(1sign-1bit.18bis) to 20bits fixed binary decimal
def format_d(num):
	r, d = format(num, 'f').split('.')
	r = '0' + r[0] if len(r) == 1 else '1' + r[1]
	d = float('0.' + d)
	res = ''
	for i in xrange(18):
		d = d * 2
		res += '1' if d >= 1 else '0'
		d = d - 1 if d >= 1 else d
	res = r[1] + res
	if r[0] == '1':
		if eval(res) == 0:
			res = '0'
		else:
			res = bin(2 ** 19 - eval('0b' + res))[2:]
		for i in xrange(19 - len(res)):
			res = '0' + res
	res = r[0] + res
	if res == '10000000000000000000':
		res = '00000000000000000000'
	return res

fo = open('SinLUT.dat', 'w')
fo.write('module SinLUT(angle, value);\n')
fo.write('\tinput[8 : 0] angle;\n')
fo.write('\toutput[19 : 0] value;\n')
fo.write('\treg[19 : 0] reg_value;\n')
fo.write('\tassign value = reg_value;\n')
fo.write('\talways@(*) begin\n')
fo.write('\t\tcase(angle)\n')
for i in xrange(360):
	fo.write("\t\t\t%d : reg_value <= 20'b%s;\n" % (i, format_d(sin(radians(i)))))
fo.write('\t\t\tdefault: reg_value <= 0;\n')
fo.write('\t\tendcase\n')
fo.write('\tend\n')
fo.write('endmodule')

fo = open('CosLUT.dat', 'w')
fo.write('module CosLUT(angle, value);\n')
fo.write('\tinput[8 : 0] angle;\n')
fo.write('\toutput[19 : 0] value;\n')
fo.write('\treg[19 : 0] reg_value;\n')
fo.write('\tassign value = reg_value;\n')
fo.write('\talways@(*) begin\n')
fo.write('\t\tcase(angle)\n')
for i in xrange(360):
	fo.write("\t\t\t%d : reg_value <= 20'b%s;\n" % (i, format_d(cos(radians(i)))))
fo.write('\t\t\tdefault: reg_value <= 0;\n')
fo.write('\t\tendcase\n')
fo.write('\tend\n')
fo.write('endmodule')
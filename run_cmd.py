from B64_EncDec import *
import argparse

def return_dict():
	jn.update(cjn)
	return jn

def return_prints():
	_prints.extend(c_prints)
	print('')
	for p1, p2 in _prints:
		print(p1, p2)

if __name__ == '__main__':

	jn = {}
	_prints = []

	ap = argparse.ArgumentParser()
	ap.add_argument('-Ps', help='password to be encripted')
	ap.add_argument('-Pt', help='pattern to be used. Separated by "," . Use "default" for default pattern')
	ap.add_argument('-Jn', help='if you went dictionary like attributes')
	ap.add_argument('-ag', help='algorithm to use. use s, d or i')
	ap.add_argument('-ts', help='number of iteration if algorithm is i')
	args = ap.parse_args().__dict__

	if 'Ps' in args.keys():
		if 'Pt' in args.keys():
			patt = args['Pt']
		else:
			patt = 'default'
		num = args['Ps']
		if 'ag' in args.keys():
			algo = args['ag']

			if algo  in ['single', '1', 's']:
				en = SingelEncDec.enci_base64(num, patt)
				dc = SingelEncDec.deci_base64(en)
				
				jn.update({'SingleEnc': en})
				jn.update({'SingleDec': dc})
				_prints.append(('[X] --Single Enc-- ', en))
				_prints.append(('[X] --Single Dec-- ', dc))
			if algo in ['double', '2', 'd']:
				en = SingelEncDec.enci_base64(num, patt)
				dn = DobuleEncDec.double_enci(en)
				dd = DobuleEncDec.double_deci(dn)

				jn.update({'DoubleEnc': dn})
				jn.update({'DoubleDec': dd})
				_prints.append(('[X] --Double Enc--', dn))
				_prints.append(('[X] --Double Dec', dd))

			if algo in ['iter', '3', 'i']:
				en = SingelEncDec.enci_base64(num, patt)

				if 'ts' in args.keys():
					times = int(args['ts'])

					ie = IterEncDec.iter_enci(en, times)
					i_d = IterEncDec.iter_deci(ie, times, num)

					jn.update({'IterEnc': ie})
					jn.update({'IterDec': i_d})
					_prints.append(('[X] --Iter Enc--', ie))
					_prints.append(('[X] --Iter Dec--', i_d))

		if 'Jn' in args.keys() and args['Jn'] is not None:
			print(return_dict())
		else:
			return_prints()
	else:
		ap.print_help()

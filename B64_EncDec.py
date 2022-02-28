from collections import OrderedDict
import base64

cjn = {}
c_prints = []

def define_pattern(pattern):
	pattern_dict = {}
	length = len(pattern)

	for i in range(length):
		pattern_dict.update({i: pattern[i]})

	return pattern_dict

def generate_default_pattern(length, pattern):
	_pattern = []
	
	if pattern == 'default':
		jump = 0
		for i in range(length):
			if jump:
				jump = 0
				continue
			elif i % 2 == 0:
				_pattern.append(2)
				jump = 1
			else:
				_pattern.append(1)
	else:
		st_patt = [int(pn) for pn in pattern.split(',')]
		if length != sum(st_patt):
			raise AttributeError(f'Length of password and sum of pattern {pattern} is not equal')

		_pattern = st_patt

	cjn.update({'pattern': _pattern})
	c_prints.append(('[X] --pattern-- ', _pattern))
	default_pattern = define_pattern(_pattern)

	return default_pattern

def accept_num(num, rule='default'):
	serialed_keys = []
	if len(num) < 2:
		raise AttributeError(f'length of the password {num} must be greater than one')
	_num = str(num).replace(' ', '')
	str_num = ' '.join(_num)
	str_list = str_num.split(' ')
	reversed_str_list = str_list
	reversed_str_list.reverse()
	length = len(str_list)
	pattern = generate_default_pattern(length, rule)
	
	for key, value in pattern.items():
		if len(reversed_str_list) > 0:
			n_temp = []
			
			for i in range(int(value)):
				if len(reversed_str_list) > 0:
					num = reversed_str_list.pop()
					n_temp.append(num)
			serialed_keys.append((key, ''.join(n_temp)))
	
	return length, serialed_keys

class SingelEncDec:

	@staticmethod
	def enci_base64(num, rule):
		base64_str = ''

		length, keys = accept_num(num, rule)
		keys_dict = OrderedDict(keys)

		for value in keys_dict.values():
			
			base64_str += base64_bytes(value)+':'

		cjn.update({'OEBase64': base64_str})
		c_prints.append(('[X] --OEBase64-- ', base64_str))
		base64_str = base64_bytes(base64_str)

		return base64_str

	@staticmethod
	def deci_base64(_str, num=None):
		dec_num = ''

		if _str == num:
			return _str
		
		sp_str = base64.decodebytes(bytes(_str, 'utf-8')).decode()
		sp_str = sp_str.split(':')
		with_e_str = [ s+'=' for s in sp_str]
		
		for v in with_e_str:
			dec_num += base64.decodebytes(bytes(v, 'utf-8')).decode()

		return dec_num

class DobuleEncDec:

	@staticmethod
	def double_enci(_str, _num=None):

		li = []

		str_64_list = ' '.join(_str).split(' ')
		if _num is None:
			_num = 1
		for i in range(len(str_64_list)):
			ll = []
			for j in range(2):
				if len(str_64_list)>= 1:
					ll.append(str_64_list.pop())
				else:
					break
			li.append(ll)

		li.reverse()
		
		enci_list = ''
		for in_lst in li:
			if len(in_lst) > 0:
				in_lst.reverse()
				join_list = ''.join(in_lst)
				enci_list += base64_bytes(join_list)[:-1]+':'
			if len(in_lst) == 0:
				continue

		cjn.update({f'--{_num}OEBase64--': enci_list})
		c_prints.append((f'[X] --{_num}OEBase64--',enci_list))
		_encrptd = base64_bytes(enci_list)

		return _encrptd

	@staticmethod
	def double_deci(_str, num=None):
		double_num = ''

		if _str == num:
			return _str
		d_str = base64.decodebytes(bytes(_str, 'utf-8')).decode()

		d_list = d_str.split(':')
		d_e_list = [e+'=' for e in d_list]

		for d_e in d_e_list:
			double_num += base64.decodebytes(bytes(d_e, 'utf-8')).decode()

		double_num = SingelEncDec.deci_base64(double_num, num)
		return double_num

class IterEncDec:

	@staticmethod
	def iter_enci(_str, _num):

		n_str = _str

		for i in range(_num):
			n_str = DobuleEncDec.double_enci(n_str, _num)

		return n_str

	@staticmethod
	def iter_deci(_str, _num, _in_num=None):

		id_str = _str
		for i in range(_num):
			id_str = DobuleEncDec.double_deci(id_str, _in_num)

		return id_str

def base64_bytes(v, encodeing='utf-8'):
	_str  = base64.encodebytes(bytes(v, encodeing)).decode().replace('\n', '')
	return _str


import sqlite3

from B64_EncDec import *

commands_table = {
	'insert password': ['password', 'pattern', 'algorithm'],
	'show password': '',
}
password_table = {}

def compare_string(str1, str2):
	failed_in_len = False
	true_str = str1.replace(' ', '')
	_str2 = str2.replace(' ', '')

	if len(true_str) != len(_str2):
		failed_in_len = True

	sucess_count = 0
	for l_1, l_2 in zip(true_str, _str2):
		if l_1 != l_2:
			continue

		sucess_count += 1

	true_len = len(true_str)
	similarity = int(100*sucess_count/true_len)

	if failed_in_len:
		return False, similarity

	return True, similarity

def check_command(_command):
	faild_commands_dict = {}

	for n_cmd in commands_table.keys():
		flag, similarity = compare_string(n_cmd, _command)
		
		if flag:
			return True, n_cmd
		faild_commands_dict.update({similarity :n_cmd})

	max_sim = max(list(faild_commands_dict.keys()))
	probbl_cmd = faild_commands_dict[max_sim]

	return False, probbl_cmd

def return_prints():
	_prints.extend(c_prints)
	print('')
	for p1, p2 in _prints:
		print(p1, p2)

'''
class FileOper:

	def __init__(self, filename):
		self._filename = filename

	def open_file(self, mode):

		self._file = open(self._filename, mode)

	def close_file(self):
		self._file.close()

	def write_to_file(self, content):
		self._file.write(content)

	def read_from_file(self):

		return self._file.read()
'''

def print_table(_data):
	pr_order = ['password', 'pattern', 'algorithm', 'Encripted', 'Decripted']

	print('---------------------------------------------------')
	for row in data:

		print('================================================')
		for label, col in zip(pr_order, row):
			print('%s : %s ' % (label, col))
		print('================================================')
		print()

	print('---------------------------------------------------')

class DB:

	def __init__(self, db_name):
		self._db = db_name

	def connect(self):

		self.con = sqlite3.Connection(self._db)

	def execute(self, arg):
		self.con.execute(arg)

	def table(self, _table):
		self.table = _table

	def fetchall(self):
		data = self.con.execute('select * from %s' %(self.table))
		return data.fetchall()

	def commit(self):
		self.con.commit()

	def close(self):
		self.con.close()

if __name__ == '__main__':

	database = DB('sqlite.db')

	try:
		db = database
		db.connect()
		db.table('password')
		db.execute('create table %s (pass, pattern, algo, enc, dec)' %(db.table))
		db.close()
	except Exception as e:
		pass

	while True:

		_prints = []
		fpass_table = []

		user_input = input('$: ')
		if user_input == 'exit':
			break

		flag, command = check_command(user_input)
		if flag:
			if command == 'insert password':
				user_coms = {}
				inpts = commands_table[command]
				for inpt in inpts:
					u_inpt = input(f'{inpt}: ')
					user_coms.update({inpt: u_inpt})

				se = SingelEncDec.enci_base64(user_coms['password'], user_coms['pattern'])
				if user_coms['algorithm'] in ['s', 'single', 0]:
					sd = SingelEncDec.deci_base64(se)
					_prints.append(('[X] --Single Enc-- ', se))
					_prints.append(('[X] --Single Dec-- ', sd))

					fpass_table.append(('Enc', se))
					fpass_table.append(('Dec', sd))

				if user_coms['algorithm'] in ['d', 'double', 1]:
					de = DobuleEncDec.double_enci(se)
					dd = DobuleEncDec.double_deci(de)
					_prints.append(('[X] --Dobule Enc-- ', de))
					_prints.append(('[X] --Dobule Dec--', dd))

					fpass_table.append(('Enc' ,de))
					fpass_table.append(('Dec', dd))

				if user_coms['algorithm'] in ['i', 'iter', 2]:
					times = int(input('times:>> '))
					ie = IterEncDec.iter_enci(se, times)
					_id = IterEncDec.iter_deci(ie, times)
					_prints.append(('[X] --Iter Enc-- ', ie))
					_prints.append(('[X] --Iter Dec-- ', _id))

					fpass_table.append(('Enc', ie))
					fpass_table.append(('Dec', _id))

				fpass_table.extend([('password', user_coms['password']), ('pattern', user_coms['pattern']), ('algorithm', user_coms['algorithm'])])

				'''f = FileOper('pass.txt')
				f.open_file('a')
				for content in fpass_table:
					f.write_to_file(content[0]+' '+content[1]+'\n')
				f.close_file()'''
				d_cotet = OrderedDict(fpass_table)

				db = database
				db.connect()
				db.execute('insert into {} (pass, pattern, algo, enc, dec) values("{}", "{}", "{}", "{}", "{}")'.format(db.table, d_cotet['password'], d_cotet['pattern'], d_cotet['algorithm'], d_cotet['Enc'], d_cotet['Dec']))
				db.commit()
				db.close()

				return_prints()
			if command == 'show password':
				'''f = FileOper('pass.txt')
				f.open_file('r')
				print_table(f.read_from_file())
				f.close_file()'''
				con = database
				con.connect()
				data = con.fetchall()
				print_table(data)
				con.close()
		else:
			print(f'do you mean {command}')



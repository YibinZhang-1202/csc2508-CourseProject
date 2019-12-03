import argparse
import os
import sys

def read_detect_result(path):
	detect_result = []
	
	with open(path, 'r') as f:
		for line in f:
			the_line = line.split()
			for i,t in enumerate(the_line):
				vehicle_color = t.split(',')[0].split('(')[1]
				vehicle_type = t.split(',')[1].split(')')[0]
				the_line[i] = (vehicle_color, vehicle_type)
			detect_result.append(the_line)

	return detect_result

def read_reid_result(path):
	reid_result = []
	
	with open(path, 'r') as f:
		for line in f:
			the_line = line.split('[')[1].split(']')[0]
			the_line = the_line.split(',')
			the_line = [int(x) for x in the_line if x != '']
			reid_result.append(the_line)

	return reid_result

def remove_self(detect_result, reid_result_self_1, reid_result_self_2):
	for i, d in enumerate(reid_result_self_1):
		if i in d:
			d.remove(i)

	for i, d in enumerate(reid_result_self_2):
		if i in d:
			d.remove(i)

	pop_times = 0

	for i in reid_result_self_1:
		i.sort()
		for j in i:
			reid_result_self_1[j].clear()
			detect_result[0].pop(j-pop_times)
			pop_times += 1

	pop_times = 0

	for i in reid_result_self_2:
		i.sort()
		for j in i:
			reid_result_self_2[j].clear()
			detect_result[1].pop(j-pop_times)
			pop_times += 1


def remove_cross(detect_result, reid_result):
	duplicate_set = set()

	for i in reid_result:
		for j in i:
			duplicate_set.add(j)

	pop_times = 0
	duplicate_list = list(duplicate_set)
	duplicate_list.sort()
	
	for i in duplicate_list:
		detect_result[1].pop(i-pop_times)
		pop_times += 1

def aggregate_color(detect_result):
	color_dict = {}

	for i in detect_result:
		for j in i:
			if j[0] not in color_dict:
				color_dict[j[0]] = 0
			color_dict[j[0]] += 1

	return color_dict

def aggregate_type(detect_result):
	type_dict = {}

	for i in detect_result:
		for j in i:
			if j[1] not in type_dict:
				type_dict[j[1]] = 0
			type_dict[j[1]] += 1

	return type_dict

def aggregate_color_type(detect_result):
	color_type_dict = {}

	for i in detect_result:
		for j in i:
			if j not in color_type_dict:
				color_type_dict[j] = 0
			color_type_dict[j] += 1

	return color_type_dict

def dump_result(color_dict, type_dict, color_type_dict, path):
	if not os.path.isdir(path):
		mkdir(path)
	with open(os.path.join(path, 'color_aggregation.txt'), 'w') as f:
		f.write(str(color_dict))
	with open(os.path.join(path, 'type_aggregation.txt'), 'w') as f:
		f.write(str(type_dict))
	with open(os.path.join(path, 'color_type_aggregation.txt'), 'w') as f:
		f.write(str(color_type_dict))


parser = argparse.ArgumentParser(description='Process detect and reid results.')
parser.add_argument('-dir-path', type=str, default='../aic19-track2-reid/t/', help='Detect result file.')
parser.add_argument('-detect-result', type=str, default='detect_result.txt', help='Detect result file.')
parser.add_argument('-reid-result-self', type=str, default='reid_result_self.txt', help='Reid result file.')
parser.add_argument('-reid-result-cross', type=str, default='reid_result_cross.txt', help='Reid result file.')


def main():
	detect_result = read_detect_result(os.path.join(args.dir_path, args.detect_result))
	print(detect_result)

	reid_result_self_1 = read_reid_result(os.path.join(args.dir_path, args.reid_result_self.split('.')[0] + '_1.' + args.reid_result_self.split('.')[1]))
	reid_result_self_2 = read_reid_result(os.path.join(args.dir_path, args.reid_result_self.split('.')[0] + '_2.' + args.reid_result_self.split('.')[1]))
	remove_self(detect_result, reid_result_self_1, reid_result_self_2)

	# print(reid_result_self)
	print(detect_result)

	reid_result_cross = read_reid_result(os.path.join(args.dir_path, args.reid_result_cross))
	remove_cross(detect_result, reid_result_cross)
	# # print(reid_result_cross)
	print(detect_result)

	color_dict = aggregate_color(detect_result)
	print(color_dict)

	type_dict = aggregate_type(detect_result)
	print(type_dict)

	color_type_dict = aggregate_color_type(detect_result)
	print(color_type_dict)

	dump_result(color_dict, type_dict, color_type_dict, args.dir_path)


if __name__ == '__main__':
	args = parser.parse_args()

	main()
import argparse
import os
import math
import sys

mode_list = ['min', 'max', 'average']

def read_detect_result(path):
	detect_result = []
	
	with open(path, 'r') as f:
		for line in f:
			the_line = line.split()
			for i,t in enumerate(the_line):
				vehicle_color = t.split(',')[0].split('(')[1]
				vehicle_type = t.split(',')[1].split(')')[0]
				start_length = t.split(',')[2]
				the_line[i] = (vehicle_color, vehicle_type, start_length)
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

def aggregate(detect_result, interval_size, batch_size):
	count_dict = {}

	for each_cam in detect_result:
		for each_veh in each_cam:
			start = each_veh[2].split('_')[0]
			length = each_veh[2].split('_')[1]
			index = (int(start) // interval_size) * interval_size
			end = int(start) + int(length) - 1

			while index <= end:
				# print(start, length, index, end)
				if index not in count_dict:
					count_dict[index] = 0
				count_dict[index] += 1
				index += interval_size
			# print("\n")

	return count_dict

def compute_average(count_interval, interval_size, batch_size):
	count = 0

	for e in count_interval.values():
		count += e

	return count/math.ceil(batch_size/interval_size)

def compute_min(count_interval, interval_size, batch_size):
	the_min = 0
	interval_list = []
	num_intervals = math.ceil(batch_size/interval_size)

	if num_intervals == len(count_interval):
		the_min = sys.maxsize
		for e in count_interval.values():
			if e < the_min:
				the_min = e

		for key in count_interval:
			if count_interval[key] == the_min:
				interval_list.append((key, key+interval_size))
	else:
		for x in range(0, num_intervals):
			the_key = x * interval_size
			if the_key not in count_interval:
				interval_list.append((the_key, the_key+interval_size))
			else:
				if count_interval[the_key] == the_min:
					interval_list.append((the_key, the_key+interval_size))

	return the_min, interval_list

def compute_max(count_interval, interval_size, batch_size):
	interval_list = []
	the_max = 0

	if len(count_interval) != 0:
		for e in count_interval.values():
			if e > the_max:
				the_max = e

	if the_max != 0:
		for key in count_interval:
			if count_interval[key] == the_max:
				interval_list.append((key, key+interval_size))
	else:
		num_intervals = math.ceil(batch_size/interval_size)
		for x in range(0, num_intervals):
			interval_list.append((x*interval_size, x*interval_size+interval_size))

	return the_max, interval_list

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
			color_type = (j[0], j[1])
			if color_type not in color_type_dict:
				color_type_dict[color_type] = 0
			color_type_dict[color_type] += 1

	return color_type_dict

def dump_result(interval_size, batch_size, average, the_min, min_interval_list, the_max, max_interval_list, color_dict, type_dict, color_type_dict, path):
	if not os.path.isdir(path):
		mkdir(path)
	with open(os.path.join(path, 'aggregation_result.txt'), 'w') as f:
		f.write("Aggregate by color:\n")
		f.write(str(color_dict))
		f.write("\n\nAggregate by type:\n")
		f.write(str(type_dict))
		f.write("\n\nAggregate by color and type:\n")
		f.write(str(color_type_dict))
		f.write("\n\nSlide size = " + str(interval_size) + ", batch size = " + str(batch_size) + ", number of slices = " + str(math.ceil(batch_size/interval_size)))
		f.write("\nAverage of every slide = " + str(average))
		f.write("\nMin = " + str(the_min) + " among slides = " + str(min_interval_list))
		f.write("\nMax = " + str(the_max) + " among slides = " + str(max_interval_list))


parser = argparse.ArgumentParser(description='Process detect and reid results.')
parser.add_argument('-dir-path', type=str, default='../aic19-track2-reid/t/', help='Detect result file.')
parser.add_argument('-detect-result', type=str, default='detect_result.txt', help='Detect result file.')
parser.add_argument('-reid-result-self', type=str, default='reid_result_self.txt', help='Reid result file.')
parser.add_argument('-reid-result-cross', type=str, default='reid_result_cross.txt', help='Reid result file.')
parser.add_argument('-interval-size', type=int, default=10, help='Interval size for aggregation.')
parser.add_argument('-batch-size', type=int, default=100, help='Interval size for aggregation.')


def main():
	detect_result = read_detect_result(os.path.join(args.dir_path, args.detect_result))
	# print(detect_result)

	reid_result_self_1 = read_reid_result(os.path.join(args.dir_path, args.reid_result_self.split('.')[0] + '_1.' + args.reid_result_self.split('.')[1]))
	reid_result_self_2 = read_reid_result(os.path.join(args.dir_path, args.reid_result_self.split('.')[0] + '_2.' + args.reid_result_self.split('.')[1]))
	remove_self(detect_result, reid_result_self_1, reid_result_self_2)
	# print(detect_result)

	reid_result_cross = read_reid_result(os.path.join(args.dir_path, args.reid_result_cross))
	remove_cross(detect_result, reid_result_cross)
	# print(detect_result)

	count_interval = aggregate(detect_result, args.interval_size, args.batch_size)
	print(count_interval)
	
	average = compute_average(count_interval, args.interval_size, args.batch_size)
	print(average)

	the_max, max_interval_list = compute_max(count_interval, args.interval_size, args.batch_size)
	print(the_max, max_interval_list)

	the_min, min_interval_list = compute_min(count_interval, args.interval_size, args.batch_size)
	print(the_min, min_interval_list)

	color_dict = aggregate_color(detect_result)
	print(color_dict)

	type_dict = aggregate_type(detect_result)
	print(type_dict)

	color_type_dict = aggregate_color_type(detect_result)
	print(color_type_dict)

	dump_result(args.interval_size, args.batch_size, average, the_min, min_interval_list, the_max, max_interval_list, color_dict, type_dict, color_type_dict, args.dir_path)


if __name__ == '__main__':
	args = parser.parse_args()

	main()
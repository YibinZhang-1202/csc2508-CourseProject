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

			# print(start, length, index)
			while index <= end:
				if index not in count_dict:
					count_dict[index] = 0
				count_dict[index] += 1
				index += interval_size

	return count_dict

def compute_average(count_interval, interval_size, batch_size):
	count = 0

	for e in count_interval.values():
		count += e

	return count/math.ceil(batch_size/interval_size)

def compute_min(count_interval, interval_size, batch_size):
	the_min = 0
	num_intervals = math.ceil(batch_size/interval_size)

	if num_intervals >= len(count_interval):
		the_min = sys.maxsize
		print(num_intervals)
		for e in count_interval.values():
			if e < the_min:
				the_min = e

	return the_min


parser = argparse.ArgumentParser(description='Process detect and reid results.')
parser.add_argument('-dir-path', type=str, default='../aic19-track2-reid/t/', help='Detect result file.')
parser.add_argument('-detect-result', type=str, default='detect_result.txt', help='Detect result file.')
parser.add_argument('-reid-result-self', type=str, default='reid_result_self.txt', help='Reid result file.')
parser.add_argument('-reid-result-cross', type=str, default='reid_result_cross.txt', help='Reid result file.')
parser.add_argument('-interval-size', type=int, default=10, help='Interval size for aggregation.')
parser.add_argument('-batch-size', type=int, default=100, help='Interval size for aggregation.')
parser.add_argument('-mode', type=str, default=min, help='Aggregation mode.')


def main():
	if args.mode not in mode_list:
		print("Please set a valid aggregation mode from: ", mode_list)
		raise("args error")

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
	# print(average)

	the_min = compute_min(count_interval, args.interval_size, args.batch_size)
	print(the_min)


if __name__ == '__main__':
	args = parser.parse_args()

	main()
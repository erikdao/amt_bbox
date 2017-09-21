#-*- encoding: utf-8
from __future__ import print_function

from itertools import groupby
from operator import itemgetter
import os.path as osp
import json
import csv

AWS_PREFIX = """https://s3-ap-southeast-1.amazonaws.com/ivul-fishdata/"""
LOCAL_PREFIX = """/home/cuongdd/Datasets/FishData/dotted-data/"""

def sanitize_url(s3_url):
    return s3_url.replace(AWS_PREFIX, LOCAL_PREFIX)

def load_annotation(string):
    return json.loads(string)

def load_amt_csv(path):
    if not osp.exists(path):
        raise ValueError("{} not existed!".format(path))
    
    temp, results = [], []

    with open(path, 'r') as csvf:
        raw = csv.reader(csvf, delimiter=',')
        for idx, row in enumerate(raw):
            if idx == 0:
                continue
            hit_id = row[0]
            assignment_id = row[14]
            worker_id = row[15]
            image_url = sanitize_url(row[27])
            annotations = load_annotation(row[28])
            temp.append({
                'hit_id': hit_id,
                'assignment_id': assignment_id,
                'worker_id': worker_id,
                'image_url': image_url,
                'annotations': annotations
            })

        temp.sort(key=itemgetter("image_url"))

        for key, group in groupby(temp[:9], lambda item: item['image_url']):
            print([item for item in group])
            # workers = [item['worker_id'] for item in group]
            # annotations = [item2['annotations'] for item2 in group]

            # for annotation in annotations:
            #     print(annotation)
            #     print()
            # for item in zip(workers, annotations):
            #     print(item)
            # print([item['annotations'] for item in group])
            print()

if __name__ == '__main__':
    csv_path = """/home/cuongdd/Datasets/FishData/AMT/bbox_task/Batch_2938680_batch_results.csv"""
    load_amt_csv(csv_path)
    # annotations = load_amt_csv(csv_path)
    # print(len(annotations))

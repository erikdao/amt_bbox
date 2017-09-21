#-*- encoding: utf-8
from __future__ import print_function

from itertools import groupby
from operator import itemgetter
import os.path as osp
import pprint
import time
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

        # get distinct image_url
        image_urls = set([item['image_url'] for item in temp])

        tic = time.time()
        for image_url in image_urls:
            temp_anno = {
                'hit_id': None, 'image_url': None, 'assignments_id': list(), 'workers_id': list(), 'annotations': dict()}
            for item in temp:
                if item['image_url'] == image_url:
                    temp_anno['hit_id'] = item['hit_id']
                    temp_anno['image_url'] = image_url
                    temp_anno['assignments_id'].append(item['assignment_id'])
                    temp_anno['workers_id'].append(item['worker_id'])
                    temp_anno['annotations'][item['worker_id']] = item['annotations']
            results.append(temp_anno)
        toc = time.time()
        print(">>> {} sec".format(toc - tic))
        return results

if __name__ == '__main__':
    csv_path = """/home/cuongdd/Datasets/FishData/AMT/bbox_task/Batch_2938680_batch_results.csv"""
    load_amt_csv(csv_path)
    annotations = load_amt_csv(csv_path)
    print(len(annotations))
    pprint.pprint(annotations[0])
import json
import os
from PIL import Image

use_val = 1
# Change working directory to DET dataset path
os.chdir(
    'E:\\VisDrone Dataset\\1 - Object Detection in Images\\VisDrone2018-DET-' + ('val' if use_val == 1 else 'train'))
outfile = open('instances_val2014.json' if use_val == 1 else 'instances_val2014.json', 'w')
data = {}
data['info'] = {"description": "COCO 2017 Dataset", "url": "http://cocodataset.org", "version": "1.0",
                "year": 2017, "contributor": "COCO Consortium", "date_created": "2017/09/01"}
data['licenses'] = [{"url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
                     "id": 1, "name": "Attribution-NonCommercial-ShareAlike License"}]
images = []
annotations = []
imfiles = os.listdir('images')
index = 1
anid = 1
numTrunc = 0
numOcclu = 0
# Number of objects that are neither truncated nor occluded
numComplete = 0
numType = [0] * 12
for imf in imfiles:
    im = Image.open('images/'+imf)
    item = {}
    item['license'] = 1
    item['file_name'] = imf
    item['coco_url'] = 'http://images.cocodataset.org/val2017/'+imf
    item['height'], item['width'] = im.size
    item['date_captured'] = '2013-11-15 00:09:17'
    item['flickr_url'] = ''
    item['id'] = index
    images.append(item)
    anfile = open('annotations/'+imf.replace('jpg', 'txt'))
    lines = anfile.readlines()
    for line in lines:
        # print(line)
        if len(line) < 2:
            continue
        anitem = {'segmentations': [[]]}
        nums = [int(x) for x in line.split(',')]
        if nums[4] == 0:
            continue
        anitem['area'] = nums[2]*nums[3]
        anitem['iscrowd'] = 0
        anitem['image_id'] = index
        anitem['bbox'] = nums[0:4]
        anitem['category_id'] = nums[5]
        anitem['id'] = anid
        anid += 1
        anitem['trunc'] = nums[6]
        anitem['occlu'] = nums[7]
        if nums[6] == 0 and nums[7] == 0:
            numComplete += 1
        if nums[6] == 1:
            numTrunc += 1
        if nums[7] == 1:
            numOcclu += 1
        numType[nums[5]] += 1
        annotations.append(anitem)
    print(index)
    index += 1
data['images'] = images
data['annotations'] = annotations
data['categories'] = [{'supercategory': 'person', 'id': 1, 'name': 'pedestrian'},
                      {'supercategory': 'person', 'id': 2, 'name': 'people'},
                      {'supercategory': 'sm_vehicle', 'id': 3, 'name': 'bicycle'},
                      {'supercategory': 'lg_vehicle', 'id': 4, 'name': 'car'},
                      {'supercategory': 'lg_vehicle', 'id': 5, 'name': 'van'},
                      {'supercategory': 'lg_vehicle', 'id': 6, 'name': 'truck'},
                      {'supercategory': 'sm_vehicle', 'id': 7, 'name': 'tricycle'},
                      {'supercategory': 'sm_vehicle',
                          'id': 8, 'name': 'awning-tricycle'},
                      {'supercategory': 'lg_vehicle', 'id': 9, 'name': 'bus'},
                      {'supercategory': 'sm_vehicle', 'id': 10, 'name': 'motor'}]
print('Complete: ', numComplete/len(annotations))
print('Truncated: ', numTrunc/len(annotations))
print('Occluded: ', numOcclu/len(annotations))
print(len(annotations))
print(numType)
json.dump(data, outfile, indent=4)

import json
import os
from PIL import Image

print('hi')
os.chdir(
    'E:\\VisDrone Dataset\\1 - Object Detection in Images\\VisDrone2018-DET-train')
outfile = open('instances_val2017.json', 'w')
data = {}
data['info'] = {"description": "COCO 2017 Dataset", "url": "http://cocodataset.org", "version": "1.0",
                "year": 2017, "contributor": "COCO Consortium", "date_created": "2017/09/01"}
data['licenses'] = [{"url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
                     "id": 1, "name": "Attribution-NonCommercial-ShareAlike License"}]
images = []
annotations = []
imfiles = os.listdir('images')
#imfiles = imfiles[4504:]
index = 1
anid = 1
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
        #print(line)
        if len(line) < 2:
            continue
        anitem = {'segmentations': [[]]}
        nums = [int(x) for x in line.split(',')]
        if nums[4]==0:
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
        annotations.append(anitem)
    print(index)
    index += 1
data['images'] = images
data['annotations'] = annotations
json.dump(data, outfile, indent=4)

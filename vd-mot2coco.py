import json
import os
from PIL import Image
import shutil

# Change working directory to DET dataset path
os.chdir(
    '/home/magus/dataset/VisDrone-Dataset/2-Object-Detection-in-Videos/VisDrone2018-VID-train')
outfile = open('coco/annotations/instances_train2014.json', 'w')
data = {}
data['info'] = {"description": "COCO 2015 Dataset", "url": "http://cocodataset.org", "version": "1.0",
                "year": 2015, "contributor": "COCO Consortium", "date_created": "2015/09/01"}
data['licenses'] = [{"url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
                     "id": 1, "name": "Attribution-NonCommercial-ShareAlike License"}]
images = []
annotations = []
videoList = os.listdir('sequences')
videoList.sort()
videoIndex = -1
anid = 1
numTrunc = 0
numOcclu = 0
# Number of objects that are neither truncated nor occluded
numComplete = 0
numType = [0] * 12
imageIndex = -1
frameMap = {}
frameStep = 8
for vid in videoList:
    videoIndex += 1
    frameList = os.listdir('sequences/'+vid)
    frameList.sort()
    for i in xrange(0, len(frameList), frameStep):
        frame = frameList[i]
        imageIndex+=1
        im = Image.open('sequences/'+vid+'/'+frame)
        item = {}
        item['license'] = 1
        item['file_name'] = vid+'-'+frame
        item['coco_url'] = 'http://images.cocodataset.org/val2017/'+frame
        item['height'], item['width'] = im.size
        item['date_captured'] = '2013-11-15 00:09:17'
        item['flickr_url'] = ''
        item['id'] = imageIndex
        frameMap[videoIndex*10000+i+1] = imageIndex
        images.append(item)
        shutil.copy2('sequences/'+vid+'/'+frame, 'coco/images/'+vid+'-'+frame)
    annoFile = open('annotations/'+vid+'.txt')
    lines = annoFile.readlines()
    for line in lines:
        # print(line)
        if len(line) < 2:
            continue
        anitem = {'segmentations': [[]]}
        nums = [int(x) for x in line.split(',')]
        if nums[0]%frameStep is not 0:
            continue
        anitem['area'] = nums[4]*nums[5]
        anitem['iscrowd'] = 0
        anitem['image_id'] = frameMap[videoIndex*10000+nums[0]]
        anitem['bbox'] = nums[2:6]
        anitem['category_id'] = nums[7]
        anitem['id'] = anid
        anid += 1
        anitem['trunc'] = nums[8]
        anitem['occlu'] = nums[9]
        if nums[8] == 0 and nums[9] == 0:
            numComplete += 1
        if nums[8] == 1:
            numTrunc += 1
        if nums[9] == 1:
            numOcclu += 1
        numType[nums[7]] += 1
        annotations.append(anitem)
    print(videoIndex)
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
print(numComplete/anid)
print(numTrunc/anid)
print(numOcclu/anid)
print(numType)
json.dump(data, outfile, indent=4)

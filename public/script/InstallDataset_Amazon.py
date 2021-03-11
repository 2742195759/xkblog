import os
import os.path as osp
import sys
os.system("mkdir -p /home/data/dataset")
os.system("mkdir -p /home/data/cache")
if not osp.exists(osp.join('/home/data/cache', 'Amazon.tar')):
    print ("Downloading Amazon dataset for cvpack_rec")
    os.system('cd /home/data/cache && wget -c https://cloud.tsinghua.edu.cn/f/38cf90e4c5984b388ef5/?dl=1')
    print ("Downloaded")
os.system('tar -xf /home/data/cache/Amazon.tar -C /home/data/cache/')
os.system('mv /home/data/cache/Amazon /home/data/dataset')

print ("Process Complete!!")
os.system('rm -r /home/data/cache')


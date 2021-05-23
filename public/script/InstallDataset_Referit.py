import os
import os.path as osp
import sys
os.system("mkdir -p /home/data/dataset")
os.system("mkdir -p /home/data/cache")
if not osp.exists(osp.join('/home/data/cache', 'Amazon.tar')):
    print ("Downloading Amazon dataset for cvpack_rec")
    os.system('wget -c https://cloud.tsinghua.edu.cn/f/38cf90e4c5984b388ef5/?dl=1 -O /home/data/cache/Amazon.tar')
    print ("Downloaded")
os.system('tar -xf /home/data/cache/Amazon.tar -C /home/data/cache/')
os.system('mv /home/data/cache/Amazon /home/data/dataset')

print ("Process Complete!!")
# os.system('rm -r /home/data/cache')
(xkcv) root@2623330f9feb:~# cat InstallDataset_Referit.py 
import os
import os.path as osp
import sys
os.system("mkdir -p /home/data/dataset/cv/")
os.system("mkdir -p /home/data/cache")
if not osp.exists(osp.join('/home/data/cache', 'Referit.tar')):
    print ("Downloading Referit dataset for cvpack_model")
    os.system('wget -c https://cloud.tsinghua.edu.cn/f/add87fb900294f0eb67d/?dl=1 -O /home/data/cache/Referit.tar')
    print ("Downloaded")
if not osp.exists('/home/data/dataset/cv/referit'):
    os.system('tar -xf /home/data/cache/Referit.tar -C /home/data/dataset/cv/')

os.system('cd /home/data/dataset/cv/referit/refer && python setup.py install')
os.system('pip install scikit-image -i https://pypi.tuna.tsinghua.edu.cn/simple')
os.system('pip install h5py -i https://pypi.tuna.tsinghua.edu.cn/simple')

print ("Process Complete!!")
# os.system('rm -r /home/data/cache')
(xkcv) root@2623330f9feb:~# read escape sequence
xiongkun@192 Downloads % docker attach xkcv
(xkcv) root@2623330f9feb:~# ls
Important  InstallDataset_Amazon.py  InstallDataset_Referit.py  Update_Cvlib.sh  cvpack2  cvpack2_model  cvpack2_rec  llvm  miniconda3
(xkcv) root@2623330f9feb:~# cat InstallDataset_Referit.py 
import os
import os.path as osp
import sys
os.system("mkdir -p /home/data/dataset/cv/")
os.system("mkdir -p /home/data/cache")
if not osp.exists(osp.join('/home/data/cache', 'Referit.tar')):
    print ("Downloading Referit dataset for cvpack_model")
    os.system('wget -c https://cloud.tsinghua.edu.cn/f/38cf90e4c5984b388ef5/?dl=1 -O /home/data/cache/Referit.tar')
    print ("Downloaded")
if not osp.exists('/home/data/dataset/cv/referit'):
    os.system('tar -xf /home/data/cache/Referit.tar -C /home/data/dataset/cv/')

os.system('cd /home/data/dataset/cv/referit/refer && python setup.py install')
os.system('pip install scikit-image -i https://pypi.tuna.tsinghua.edu.cn/simple')
os.system('pip install h5py -i https://pypi.tuna.tsinghua.edu.cn/simple')

print ("Process Complete!!")
# os.system('rm -r /home/data/cache')


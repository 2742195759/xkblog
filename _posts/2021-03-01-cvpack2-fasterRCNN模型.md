---
layout : post
title  : cvpack2-fasterRCNN模型eval结果
date   : 2021-03-01 9:00:00 +0000
category : cvpack2
typora-copy-images-to: ../../../code/xkblog/public/img/
typora-root-url: ../../../code
---

#### Res-50

###### Overall: 

```text
 Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.415
 Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=100 ] = 0.628
 Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=100 ] = 0.457
 Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.238
 Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.450
 Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.523
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.327
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.505
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.522
 Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.313
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.561
 Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.664
```

###### valuation results for bbox:

|   AP   |  AP50  |  AP75  |  APs   |  APm   |  APl   |
| :----: | :----: | :----: | :----: | :----: | :----: |
| 41.455 | 62.824 | 45.693 | 23.757 | 44.967 | 52.269 |

###### Per-category bbox AP:

| category      | AP     | category     | AP     | category       | AP     |
| :------------ | :----- | :----------- | :----- | :------------- | :----- |
| person        | 53.699 | bicycle      | 32.262 | car            | 43.182 |
| motorcycle    | 42.475 | airplane     | 54.949 | bus            | 61.014 |
| train         | 59.469 | truck        | 34.839 | boat           | 28.515 |
| traffic light | 33.961 | fire hydrant | 65.982 | stop sign      | 66.547 |
| parking meter | 38.287 | bench        | 23.683 | bird           | 39.851 |
| cat           | 65.339 | dog          | 60.634 | horse          | 55.011 |
| sheep         | 52.596 | cow          | 54.702 | elephant       | 66.071 |
| bear          | 71.827 | zebra        | 66.860 | giraffe        | 68.027 |
| backpack      | 17.680 | umbrella     | 34.382 | handbag        | 13.332 |
| tie           | 37.317 | suitcase     | 34.656 | frisbee        | 65.197 |
| skis          | 23.674 | snowboard    | 35.225 | sports ball    | 49.833 |
| kite          | 44.184 | baseball bat | 31.820 | baseball glove | 40.864 |
| skateboard    | 48.359 | surfboard    | 41.444 | tennis racket  | 48.883 |
| bottle        | 38.744 | wine glass   | 39.805 | cup            | 43.182 |
| fork          | 30.274 | knife        | 20.845 | spoon          | 18.205 |
| bowl          | 41.915 | banana       | 26.028 | apple          | 23.027 |
| sandwich      | 37.525 | orange       | 32.460 | broccoli       | 29.369 |
| carrot        | 24.893 | hot dog      | 35.454 | pizza          | 53.418 |
| donut         | 53.192 | cake         | 37.654 | chair          | 28.647 |
| couch         | 37.438 | potted plant | 27.466 | bed            | 43.155 |
| dining table  | 29.916 | toilet       | 62.139 | tv             | 54.037 |
| laptop        | 57.970 | mouse        | 54.484 | remote         | 33.276 |
| keyboard      | 50.512 | cell phone   | 36.260 | microwave      | 53.313 |
| oven          | 34.123 | toaster      | 23.077 | sink           | 36.282 |
| refrigerator  | 47.133 | book         | 14.523 | clock          | 52.582 |
| vase          | 42.106 | scissors     | 32.431 | teddy bear     | 47.881 |
| hair drier    | 5.968  | toothbrush   | 19.086 |                |        |

#### Res-101




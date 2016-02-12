#!/usr/bin/env python
import os,sys,argparse,tempfile
from subprocess import Popen,PIPE

CSVTABLE='''X,Y,APD,PreAmp,LEDchan,LEDdriver,FADCslot,FADCchan,Splitter,HVGroup,JOUT,MB,Channel,Gain
1,5,514,348,112,1.9,14,2,1,1,1,LT,1,33841
-23,5,208,266,219,1.3,20,12,1,1,1,RT,1,33743
1,4,12,280,117,1.9,14,1,2,1,1,LT,2,33764
-23,4,207,287,220,1.3,20,11,2,1,1,RT,2,33587
1,3,512,261,116,1.9,14,0,3,1,1,LT,3,33661
-23,3,228,199,221,1.3,20,10,3,2,1,RT,3,33798
1,2,43,297,113,1.9,9,15,4,1,1,LT,4,33623
-23,2,224,419,222,1.3,20,9,4,2,1,RT,4,33714
1,1,39,207,118,1.9,9,14,5,1,1,LT,5,33593
-23,1,190,102,223,1.3,20,8,5,2,1,RT,5,33707
2,5,439,34,107,1.8,9,13,6,2,1,LT,6,34304
-22,5,141,86,214,1.3,20,7,6,4,1,RT,6,34497
2,4,436,122,108,1.8,9,12,7,2,1,LT,7,33879
-22,4,85,403,215,1.3,20,6,7,4,1,RT,7,33777
2,3,437,369,109,1.8,9,11,8,2,1,LT,8,33710
-22,3,136,119,216,1.3,20,5,8,4,1,RT,8,33540
2,2,379,420,110,1.8,9,10,9,2,1,LT,9,33564
-22,2,102,196,217,1.3,20,4,9,3,1,RT,9,33800
2,1,434,81,111,1.8,9,9,10,2,1,LT,10,33415
-22,1,105,80,218,1.3,20,3,10,3,1,RT,10,33640
3,5,441,96,102,1.8,9,8,11,2,1,LT,11,34075
-21,5,142,47,209,1.3,20,2,11,4,1,RT,11,33923
3,4,435,208,103,1.8,9,7,12,2,1,LT,12,33808
-21,4,143,197,210,1.3,20,1,12,4,1,RT,12,33620
3,3,377,265,104,1.8,9,6,13,2,1,LT,13,33589
-21,3,157,125,211,1.3,20,0,13,4,1,RT,13,33501
3,2,381,339,105,1.8,9,5,14,2,1,LT,14,33460
-21,2,170,376,212,1.3,19,15,14,3,1,RT,14,33769
3,1,442,61,106,1.8,9,4,15,2,1,LT,15,33313
-21,1,179,248,213,1.3,19,14,15,3,1,RT,15,33640
4,5,344,492,97,1.8,9,3,16,3,1,LT,16,34533
-20,5,89,145,204,1.3,19,13,16,4,1,RT,16,33804
4,4,343,59,98,1.8,9,2,1,3,2,LT,17,34016
-20,4,88,353,205,1.3,19,12,1,4,2,RT,17,33602
4,3,337,246,99,1.8,9,1,2,3,2,LT,18,33704
-20,3,99,233,206,1.3,19,11,2,4,2,RT,18,33413
4,2,340,74,100,1.8,9,0,3,3,2,LT,19,33471
-20,2,108,219,207,1.3,19,10,3,3,2,RT,19,33753
4,1,342,299,101,1.8,8,15,4,3,2,LT,20,33449
-20,1,173,307,208,1.3,19,9,4,3,2,RT,20,33592
5,5,345,87,92,1.8,8,14,5,3,2,LT,21,34459
-19,5,287,46,199,1.3,19,8,5,5,2,RT,21,33916
5,4,347,230,93,1.8,8,13,6,3,2,LT,22,33795
-19,4,286,71,200,1.3,19,7,6,5,2,RT,22,33869
5,3,346,278,94,1.8,8,12,7,3,2,LT,23,33561
-19,3,288,456,201,1.3,19,6,7,5,2,RT,23,33788
5,2,348,177,95,1.8,8,11,8,3,2,LT,24,33458
-19,2,281,338,202,1.3,19,5,8,5,2,RT,24,33595
5,1,339,247,96,1.8,8,10,9,3,2,LT,25,33399
-19,1,285,326,203,1.3,19,4,9,5,2,RT,25,33493
6,5,368,70,87,1.8,8,9,10,4,2,LT,26,34303
-18,5,277,346,194,1.3,19,3,10,5,2,RT,26,33893
6,4,370,302,88,1.8,8,8,11,4,2,LT,27,33933
-18,4,280,170,195,1.3,19,2,11,5,2,RT,27,33811
6,3,363,452,89,1.8,8,7,12,4,2,LT,28,33842
-18,3,283,116,196,1.3,19,1,12,5,2,RT,28,33753
6,2,371,495,90,1.8,8,6,13,4,2,LT,29,33601
-18,2,278,404,197,1.3,19,0,13,5,2,RT,29,33576
6,1,369,267,91,1.8,8,5,14,4,2,LT,30,33548
-18,1,282,379,198,1.3,18,15,14,5,2,RT,30,33476
7,5,362,23,82,1.8,8,4,15,4,2,LT,31,33986
-17,5,67,222,189,1.3,18,14,15,6,2,RT,31,33899
7,4,372,106,83,1.8,8,3,16,4,2,LT,32,33919
-17,4,109,384,190,1.3,18,13,16,6,2,RT,32,33734
7,3,367,173,84,1.8,8,2,1,4,3,LT,33,33606
-17,3,118,423,191,1.3,18,12,1,6,3,RT,33,33642
7,2,364,6,85,1.8,8,1,2,4,3,LT,34,33571
-17,2,19,350,192,1.3,18,11,2,6,3,RT,34,33600
7,1,361,221,86,1.8,8,0,3,4,3,LT,35,33329
-17,1,71,389,193,1.3,18,10,3,6,3,RT,35,33580
8,5,400,88,77,1.8,7,15,4,5,3,LT,36,34082
-16,5,68,273,184,1.3,18,9,4,6,3,RT,36,33775
8,4,408,114,78,1.8,7,14,5,5,3,LT,37,33799
-16,4,156,449,185,1.3,18,8,5,6,3,RT,37,33687
8,3,295,285,79,1.8,7,13,6,5,3,LT,38,33668
-16,3,22,188,186,1.3,18,7,6,6,3,RT,38,33634
8,2,403,375,80,1.8,7,12,7,5,3,LT,39,33591
-16,2,50,336,187,1.3,18,6,7,6,3,RT,39,33583
8,1,292,432,81,1.8,7,11,8,5,3,LT,40,33397
-16,1,24,257,188,1.3,18,5,8,6,3,RT,40,33577
-15,5,91,238,179,1.3,18,4,9,17,3,RT,41,33886
9,5,407,195,72,1.8,7,10,9,5,3,LT,41,34015
-15,4,124,358,180,1.3,18,3,10,17,3,RT,42,33800
9,4,488,210,73,1.8,7,9,10,5,3,LT,42,33842
-15,3,140,172,181,1.3,18,2,11,17,3,RT,43,33705
9,3,399,7,74,1.8,7,8,11,5,3,LT,43,33667
-15,2,33,378,182,1.3,18,1,12,17,3,RT,44,33602
9,2,397,270,75,1.8,7,7,12,5,3,LT,44,33504
-15,1,129,84,183,1.3,18,0,13,17,3,RT,45,33583
9,1,486,347,76,1.8,7,6,13,5,3,LT,45,33350
-14,5,151,397,174,1.3,17,15,14,17,3,RT,46,33843
10,5,433,140,67,1.8,7,5,14,6,3,LT,46,34112
-14,4,132,426,175,1.3,17,14,15,17,3,RT,47,33780
10,4,443,446,68,1.8,7,4,15,6,3,LT,47,33854
-14,3,36,390,176,1.3,17,13,16,17,3,RT,48,33655
10,3,383,231,69,1.8,7,3,16,6,3,LT,48,33711
-14,2,25,143,177,1.3,17,12,1,17,4,RT,49,33593
10,2,380,212,70,1.8,7,2,1,6,4,LT,49,33598
-14,1,134,324,178,1.3,17,11,2,17,4,RT,50,33579
10,1,450,289,71,1.8,7,1,2,6,4,LT,50,33540
11,5,440,457,62,1.8,7,0,3,6,4,LT,51,33876
-13,5,264,152,169,1.3,17,10,3,8,4,RT,51,33894
11,4,447,386,63,1.8,6,15,4,6,4,LT,52,33750
-13,4,258,189,170,1.3,17,9,4,8,4,RT,52,33809
11,3,384,440,64,1.8,6,14,5,6,4,LT,53,33615
-13,3,253,383,171,1.3,17,8,5,8,4,RT,53,33734
11,2,375,470,65,1.8,6,13,6,6,4,LT,54,33586
-13,2,257,460blue,172,1.3,17,7,6,8,4,RT,54,33593
11,1,475,331,66,1.8,6,12,7,6,4,LT,55,33413
-13,1,261,290,173,1.3,17,6,7,8,4,RT,55,33562
12,5,222,17,57,1.8,6,11,8,7,4,LT,56,34032
-12,5,262,40,164,1.9,17,5,8,8,4,RT,56,33850
12,4,202,255,58,1.8,6,10,9,7,4,LT,57,33958
-12,4,255,63,165,1.9,17,4,9,8,4,RT,57,33806
12,3,201,305,59,1.8,6,9,10,7,4,LT,58,33734
-12,3,256,444,166,1.9,17,3,10,8,4,RT,58,33722
12,2,227,134,60,1.8,6,8,11,7,4,LT,59,33592
-12,2,260,469red,167,1.9,17,2,11,8,4,RT,59,33589
12,1,200,16,61,1.8,6,7,12,7,4,LT,60,33454
-12,1,259,284,168,1.9,17,1,12,8,4,RT,60,33460
13,5,223,39,52,1,6,6,13,7,4,LT,61,33998
-11,5,87,24,159,1.9,17,0,13,9,4,RT,61,33915
13,4,221,355,53,1,6,5,14,7,4,LT,62,33909
-11,4,27,35,160,1.9,16,15,14,9,4,RT,62,33838
13,3,199,442,54,1,6,4,15,7,4,LT,63,33634
-11,3,138,191,161,1.9,16,14,15,9,4,RT,63,33758
13,2,217,352,55,1,6,3,16,7,4,LT,64,33558
-11,2,139,234,162,1.9,16,13,16,9,4,RT,64,33594
13,1,220,460red,56,1,6,2,1,7,5,LT,65,33341
-11,1,90,381,163,1.9,16,12,1,9,5,RT,65,33498
14,5,421,488,47,1,6,1,2,8,5,LT,66,33929
-10,5,137,241,154,1.9,16,11,2,9,5,RT,66,33882
14,4,422,166,48,1,6,0,3,8,5,LT,67,33882
-10,4,92,325,156,1.9,16,10,3,9,5,RT,67,33835
14,3,432,447,49,1,5,15,4,8,5,LT,68,33865
-10,3,32,503,157,1.9,16,9,4,9,5,RT,68,33717
14,2,423,269,50,1,5,14,5,8,5,LT,69,33552
-10,2,29,204,158,1.9,16,8,5,9,5,RT,69,33578
-9,5,182,461,155,1.9,16,7,6,10,5,RT,70,34083
14,1,428,388,51,1,5,13,6,8,5,LT,70,33458
-9,4,184,123,151,1.9,16,6,7,10,5,RT,71,33835
15,5,426,113,42,1,5,12,7,8,5,LT,71,33924
-9,3,189,60,152,1.9,16,5,8,10,5,RT,72,33593
15,4,431,334,43,1,5,11,8,8,5,LT,72,33873
-9,2,186,315,153,1.9,16,4,9,10,5,RT,73,33462
15,3,429,435,44,1,5,10,9,8,5,LT,73,33598
-8,5,172,343,149,1.9,16,3,10,10,5,RT,74,33876
15,2,427,373,45,1,5,9,10,8,5,LT,74,33549
-8,4,185,97,150,1.9,16,2,11,10,5,RT,75,33662
15,1,425,215,46,1,5,8,11,8,5,LT,75,33334
-8,3,181,286,147,1.9,16,1,12,10,5,RT,76,33556
16,5,299,146,37,1,5,7,12,9,5,LT,76,33953
-8,2,187,496,148,1.9,16,0,13,10,5,RT,77,33454
16,4,482,357,38,1,5,6,13,9,5,LT,77,33898
-7,5,178,128,144,1.9,15,15,14,12,5,RT,78,33887
16,3,293,193,39,1,5,5,14,9,5,LT,78,33701
-7,4,171,484,145,1.9,15,14,15,12,5,RT,79,33735
16,2,289,398,40,1,5,4,15,9,5,LT,79,33577
-7,3,419,445,146,1.9,15,13,16,11,5,RT,80,33919
16,1,294,408,41,1,5,3,16,9,5,LT,80,33498
-7,2,352,318,143,1.9,15,12,1,11,6,RT,81,33671
17,5,290,198,32,1,5,2,1,9,6,LT,81,33939
-6,5,180,18,139,1.9,15,11,2,12,6,RT,82,33887
17,4,490,356,33,1,5,1,2,9,6,LT,82,33878
-6,4,188,272,140,1.9,15,10,3,12,6,RT,83,33705
17,3,296,281,34,1,5,0,3,9,6,LT,83,33582
-6,3,420,263,141,1.9,15,9,4,11,6,RT,84,33830
17,2,300,425,35,1,4,15,4,9,6,LT,84,33564
-6,2,414,89,142,1.9,15,8,5,11,6,RT,85,33590
17,1,291,133,36,1,4,14,5,9,6,LT,85,33414
18,5,10,169,27,1,4,13,6,10,6,LT,86,33941
-5,5,98,162,134,1.9,15,7,6,12,6,RT,86,33875
18,4,41,412,28,1,4,12,7,10,6,LT,87,33792
-5,4,106,486,136,1.9,15,6,7,12,6,RT,87,33563
18,3,44,333,29,1,4,11,8,10,6,LT,88,33772
-5,3,409,303,137,1.9,15,5,8,11,6,RT,88,33711
18,2,37,436,30,1,4,10,9,10,6,LT,89,33696
-5,2,418,363,138,1.9,15,4,9,11,6,RT,89,33554
18,1,51,115,31,1,4,9,10,10,6,LT,90,33629
-4,5,176,171,129,1.9,15,3,10,12,6,RT,90,33839
19,5,1,130,22,1,4,8,11,10,6,LT,91,33889
-4,4,183,127,130,1.9,15,2,11,12,6,RT,91,33478
19,4,4,509,23,1,4,7,12,10,6,LT,92,33791
-4,3,351,33,131,1.9,15,1,12,11,6,RT,92,33688
19,3,2,245,24,1,4,6,13,10,6,LT,93,33740
-4,2,410,117,133,1.9,15,0,13,11,6,RT,93,33434
19,2,9,236,25,1,4,5,14,10,6,LT,94,33650
-3,5,225,451,124,1.9,14,15,14,13,6,RT,94,33805
19,1,112,244,26,1,4,4,15,10,6,LT,95,33589
-3,4,197,320,125,1.9,14,14,15,13,6,RT,95,33671
20,5,119,473,17,1,4,3,16,11,6,LT,96,33821
-3,3,219,351,132,1.9,14,13,16,13,6,RT,96,33447
20,4,61,359,18,1,4,2,1,11,7,LT,97,33772
-3,2,416,155,128,1.9,14,12,1,14,7,RT,97,33673
-2,5,192,216,114,1.9,14,11,2,13,7,RT,98,33884
20,3,113,235,19,1,4,1,2,11,7,LT,98,33705
20,2,14,54,20,1,4,0,3,11,7,LT,99,33680
-2,4,204,150,120,1.9,14,10,3,13,7,RT,99,33760
20,1,147,112,21,1,3,15,4,11,7,LT,100,33597
-2,3,194,300,126,1.9,14,9,4,13,7,RT,100,33563
21,5,155,161,12,1,3,14,5,11,7,LT,101,33790
-2,2,411,176,127,1.9,14,8,5,14,7,RT,101,33689
21,4,80,311,13,1,3,13,6,11,7,LT,102,33716
-1,5,169,142,119,1.9,14,7,6,13,7,RT,102,34112
21,3,70,259,14,1,3,12,7,11,7,LT,103,33683
-1,4,203,502,115,1.9,14,6,7,13,7,RT,103,33802
21,2,154,78,15,1,3,11,8,11,7,LT,104,33605
-1,3,196,1,121,1.9,14,5,8,13,7,RT,104,33591
21,1,62,224,16,1,3,10,9,11,7,LT,105,33585
-1,2,413,434,122,1.9,14,4,9,14,7,RT,105,33631
22,5,374,79,7,1,3,9,10,12,7,LT,106,33940
-1,1,415,480,123,1.9,14,3,10,14,7,RT,106,33905
22,4,478,156,8,1,3,8,11,12,7,LT,107,33919
22,3,446,319,9,1,3,7,12,12,7,LT,108,33754
22,2,376,443,10,1,3,6,13,12,7,LT,109,33672
22,1,473,90,11,1,3,5,14,12,7,LT,110,33595
23,5,378,22,2,1,3,4,15,12,7,LT,111,33924
23,4,445,416,3,1,3,3,16,12,7,LT,112,33760
23,3,477,181,4,1,3,2,1,12,8,LT,113,33693
-20,-5,326,120,17,1.4,19,13,1,18,8,RB,122,33850
23,2,474,458,5,1,3,1,2,12,8,LT,114,33595
-21,-1,393,109,16,1.4,19,14,2,17,8,RB,121,33597
23,1,453,310,6,1,3,0,3,12,8,LT,115,33584
-21,-2,267,406,15,1.4,19,15,3,17,8,RB,120,33853
-21,-3,335,293,14,1.4,20,0,4,18,8,RB,119,33461
-21,-4,333,30,13,1.4,20,1,5,18,8,RB,118,33595
-21,-5,331,13,12,1.4,20,2,6,18,8,RB,117,34002
-22,-1,461,345,11,1.4,20,3,7,17,8,RB,116,33615
-22,-2,263,341,10,1.4,20,4,8,17,8,RB,115,33854
-22,-3,329,330,9,1.4,20,5,9,18,8,RB,114,33536
-22,-4,330,237,8,1.4,20,6,10,18,8,RB,113,33715
-22,-5,327,220,7,1.4,20,7,11,18,8,RB,112,34247
-23,-1,366,288,6,1.4,20,8,12,16,8,RB,111,33593
-23,-2,444,41,5,1.4,20,9,13,16,8,RB,110,33783
-23,-3,438,500,4,1.4,20,10,14,16,8,RB,109,33796
-23,-4,232,382,3,1.4,20,11,15,15,8,RB,108,33732
-23,-5,237,44,2,1.4,20,12,16,15,8,RB,107,33736
4,-5,359,411,124,1.6,9,3,1,15,9,LB,131,33921
-17,-4,460,485,33,1.4,18,13,1,20,9,RB,138,33796
3,-1,160,296,123,1.6,9,4,2,14,9,LB,130,33586
-17,-5,483,82,32,1.4,18,14,2,20,9,RB,137,33883
3,-2,166,337,122,1.6,9,5,3,14,9,LB,129,33595
-18,-1,86,279,31,1.4,18,15,3,19,9,RB,136,33465
3,-3,167,262,121,1.6,9,6,4,14,9,LB,128,33605
-18,-2,30,306,30,1.4,19,0,4,19,9,RB,135,33581
3,-4,161,490,120,1.6,9,7,5,14,9,LB,127,33670
-18,-3,128,252,29,1.4,19,1,5,19,9,RB,134,33592
3,-5,159,83,119,1.6,9,8,6,14,9,LB,126,34223
-18,-4,126,283,28,1.4,19,2,6,19,9,RB,133,33713
2,-1,163,52,118,1.6,9,9,7,14,9,LB,125,33268
-18,-5,82,399,27,1.4,19,3,7,19,9,RB,132,33917
2,-2,158,69,117,1.6,9,10,8,14,9,LB,124,33594
-19,-1,94,396,26,1.4,19,4,8,19,9,RB,131,33567
2,-3,162,124,116,1.6,9,11,9,14,9,LB,123,33595
-19,-2,95,438,25,1.4,19,5,9,19,9,RB,130,33586
2,-4,164,349,115,1.6,9,12,10,14,9,LB,122,33654
-19,-3,153,329,24,1.4,19,6,10,19,9,RB,129,33595
2,-5,168,291,114,1.6,9,13,11,14,9,LB,121,33758
-19,-4,73,29,23,1.4,19,7,11,19,9,RB,128,33769
1,-1,7,400,111,1.5,9,14,12,13,9,LB,120,33526
-19,-5,121,42,22,1.4,19,8,12,19,9,RB,127,33998
1,-2,3,274,110,1.5,9,15,13,13,9,LB,119,33585
-20,-1,472,260,21,1.4,19,9,13,17,9,RB,126,33591
1,-3,45,49,113,1.5,14,0,14,13,9,LB,118,33656
-20,-2,458,374,20,1.4,19,10,14,17,9,RB,125,33842
1,-4,46,56,108,1.5,14,1,15,13,9,LB,117,33808
-20,-3,325,243,19,1.4,19,11,15,18,9,RB,124,33150
1,-5,8,182,112,1.5,14,2,16,13,9,LB,116,33813
-20,-4,328,77,18,1.4,19,12,16,18,9,RB,123,33590
-14,-3,23,105,49,1.4,17,13,1,21,10,RB,154,33709
-14,-4,110,108,48,1.4,17,14,2,21,10,RB,153,33768
-14,-5,114,141,47,1.4,17,15,3,21,10,RB,152,33882
5,-2,355,168,132,1.6,8,11,4,15,10,LB,139,33612
-15,-1,79,254,46,1.4,18,0,4,21,10,RB,151,33592
5,-3,349,395,131,1.6,8,12,5,15,10,LB,138,33858
-15,-2,111,240,45,1.4,18,1,5,21,10,RB,150,33648
5,-4,358,103,130,1.6,8,13,6,15,10,LB,137,33887
-15,-3,78,226,44,1.4,18,2,6,21,10,RB,149,33737
5,-5,354,20,129,1.6,8,14,7,15,10,LB,136,34018
-15,-4,64,258,43,1.4,18,3,7,21,10,RB,148,33760
4,-1,356,441,128,1.6,8,15,8,15,10,LB,135,33101
-15,-5,17,62,42,1.4,18,4,8,21,10,RB,147,33899
4,-2,357,153,127,1.6,9,0,9,15,10,LB,134,33609
-16,-1,489,380,41,1.4,18,5,9,20,10,RB,146,33572
4,-3,360,3,126,1.6,9,1,10,15,10,LB,133,33838
-16,-2,404,316,40,1.4,18,6,10,20,10,RB,145,33579
4,-4,353,28,125,1.6,9,2,11,15,10,LB,132,33863
-16,-3,402,448,39,1.4,18,7,11,20,10,RB,144,33593
-16,-4,405,428,38,1.4,18,8,12,20,10,RB,143,33782
-16,-5,484,118,37,1.4,18,9,13,20,10,RB,142,33811
-17,-1,485,218,36,1.4,18,10,14,20,10,RB,141,33574
-17,-2,487,276,35,1.4,18,11,15,20,10,RB,140,33584
-17,-3,492,183,34,1.4,18,12,16,20,10,RB,139,33672
8,-1,396,190,148,1.6,7,11,1,17,11,LB,155,33355
-11,-2,336,249,65,1.5,16,13,1,23,11,RB,170,33610
8,-2,391,418,147,1.6,7,12,2,17,11,LB,154,33565
-11,-3,320,164,64,1.5,16,14,2,23,11,RB,169,33706
8,-3,385,8,146,1.6,7,13,3,17,11,LB,153,33593
-11,-4,315,494,63,1.5,16,15,3,23,11,RB,168,33883
8,-4,395,414,145,1.6,7,14,4,17,11,LB,152,33843
-11,-5,321,295,62,1.5,17,0,4,23,11,RB,167,33906
8,-5,386,277,144,1.6,7,15,5,17,11,LB,151,34020
-12,-1,502,228,61,1.5,17,1,5,8,11,RB,166,33579
7,-1,505,250,143,1.6,8,0,6,16,11,LB,150,33137
-12,-2,496,65,60,1.5,17,2,6,8,11,RB,165,33595
7,-2,511,43,142,1.6,8,1,7,16,11,LB,149,33835
-12,-3,504,362,59,1.5,17,3,7,8,11,RB,164,33598
7,-3,515,111,141,1.6,8,2,8,16,11,LB,148,33879
-12,-4,500,163,58,1.5,17,4,8,8,11,RB,163,33649
7,-4,510,328,140,1.6,8,3,9,16,11,LB,147,33938
-12,-5,498,251,57,1.5,17,5,9,8,11,RB,162,33875
7,-5,513,165,139,1.6,8,4,10,16,11,LB,146,34007
-13,-1,493,394,56,1.4,17,6,10,8,11,RB,161,33590
6,-1,507,304,138,1.6,8,5,11,16,11,LB,145,33067
-13,-2,494,322,55,1.4,17,7,11,8,11,RB,160,33596
6,-2,506,294,137,1.6,8,6,12,16,11,LB,144,33417
-13,-3,495,393,54,1.4,17,8,12,8,11,RB,159,33601
6,-3,509,159,136,1.6,8,7,13,16,11,LB,143,33842
-13,-4,503,214,53,1.4,17,9,13,8,11,RB,158,33870
6,-4,516,186,135,1.6,8,8,14,16,11,LB,142,33894
-13,-5,499,483,52,1.4,17,10,14,8,11,RB,157,33992
6,-5,508,27,134,1.6,8,9,15,16,11,LB,141,33948
-14,-1,69,469blue,51,1.4,17,11,15,21,11,RB,156,33590
5,-1,350,427,133,1.6,8,10,16,15,11,LB,140,33462
-14,-2,76,417,50,1.4,17,12,16,21,11,RB,155,33607
12,-5,459,75,164,1.6,6,11,1,19,12,LB,171,33923
-7,-3,34,126,84,1.5,15,13,1,25,12,RB,186,33934
11,-1,275,138,163,1.6,6,12,2,18,12,LB,170,33318
-7,-4,307,209,83,1.5,15,14,2,26,12,RB,185,33664
11,-2,276,131,162,1.6,6,13,3,18,12,LB,169,33734
-7,-5,310,301,78,1.5,15,15,3,26,12,RB,184,33963
11,-3,269,377,161,1.6,6,14,4,18,12,LB,168,33763
-8,-2,148,31,81,1.5,16,0,4,24,12,RB,183,33563
11,-4,270,413,160,1.6,6,15,5,18,12,LB,167,33882
-8,-3,115,26,79,1.5,16,1,5,24,12,RB,182,33590
11,-5,272,453,159,1.6,7,0,6,18,12,LB,166,33992
-8,-4,16,239,73,1.5,16,2,6,24,12,RB,181,33599
10,-1,266,501,158,1.6,7,1,7,18,12,LB,165,33298
-8,-5,116,364,77,1.5,16,3,7,24,12,RB,180,33794
10,-2,268,437,157,1.6,7,2,8,18,12,LB,164,33346
-9,-2,84,459,76,1.5,16,4,8,24,12,RB,179,33837
10,-3,274,4,156,1.6,7,3,9,18,12,LB,163,33755
-9,-3,117,439,75,1.5,16,5,9,24,12,RB,179,33592
10,-4,271,36,155,1.6,7,4,10,18,12,LB,162,33858
-9,-4,150,179,74,1.5,16,6,10,24,12,RB,177,33671
10,-5,273,38,154,1.6,7,5,11,18,12,LB,161,33946
-9,-5,20,370,72,1.5,16,7,11,24,12,RB,176,33892
9,-1,394,282,153,1.6,7,6,12,17,12,LB,160,33419
-10,-2,324,466red,71,1.5,16,8,12,23,12,RB,175,33386
9,-2,387,507,152,1.6,7,7,13,17,12,LB,159,33566
-10,-3,317,129,70,1.5,16,9,13,23,12,RB,174,33664
9,-3,392,323,151,1.6,7,8,14,17,12,LB,158,33770
-10,-4,314,321,68,1.5,16,10,14,23,12,RB,173,33881
9,-4,388,50,150,1.6,7,9,15,17,12,LB,157,34016
-10,-5,316,335,67,1.5,16,11,15,23,12,RB,172,33886
9,-5,390,275,149,1.6,7,10,16,17,12,LB,156,34075
-11,-1,332,327,66,1.5,16,12,16,23,12,RB,171,33498
15,-4,59,462,180,1.7,5,11,1,20,13,LB,187,33856
-3,-3,211,223,95,1.5,14,13,1,27,13,RB,202,33465
15,-5,60,424,179,1.7,5,12,2,20,13,LB,186,34016
-3,-4,216,225,94,1.5,14,14,2,27,13,RB,201,33599
14,-1,53,180,178,1.7,5,13,3,20,13,LB,185,33374
-3,-5,212,32,97,1.5,14,15,3,27,13,RB,200,34137
14,-2,49,368,177,1.7,5,14,4,20,13,LB,184,33461
-4,-2,96,455,96,1.5,15,0,4,25,13,RB,199,33557
14,-3,56,232,176,1.7,5,15,5,20,13,LB,183,33603
-4,-3,72,407,89,1.5,15,1,5,25,13,RB,198,33792
14,-4,52,104,175,1.7,6,0,6,20,13,LB,182,33843
-4,-4,309,167,98,1.5,15,2,6,26,13,RB,197,33430
14,-5,55,332,174,1.7,6,1,7,20,13,LB,181,33891
-4,-5,308,292,92,1.5,15,3,7,26,13,RB,196,33848
13,-1,401,360,173,1.7,6,2,8,19,13,LB,180,33330
-5,-2,152,421,90,1.5,15,4,8,25,13,RB,195,33597
13,-2,464,206,172,1.7,6,3,9,19,13,LB,179,33613
-5,-3,63,184,85,1.5,15,5,9,25,13,RB,194,33856
13,-3,480,405,171,1.7,6,4,10,19,13,LB,178,33746
-5,-4,302,354,87,1.5,15,6,10,26,13,RB,193,33463
13,-4,466,98,170,1.7,6,5,11,19,13,LB,177,33918
-5,-5,312,342,93,1.5,15,7,11,26,13,RB,192,33852
13,-5,469,53,169,1.7,6,6,12,19,13,LB,176,33933
-6,-2,13,415,91,1.5,15,8,12,25,13,RB,191,33607
12,-1,465,385,168,1.6,6,7,13,19,13,LB,175,33288
-6,-3,31,95,86,1.5,15,9,13,25,13,RB,190,33894
12,-2,468,366,167,1.6,6,8,14,19,13,LB,174,33591
-6,-4,313,410,88,1.5,15,10,14,26,13,RB,189,33475
12,-3,467,67,166,1.6,6,9,15,19,13,LB,173,33659
-6,-5,305,431,82,1.5,15,11,15,26,13,RB,188,33907
12,-4,462,504,165,1.6,6,10,16,19,13,LB,172,33858
-7,-2,146,136,80,1.5,15,12,16,25,13,RB,187,33706
18,-3,81,157,196,1.7,4,11,1,22,14,LB,203,33641
18,-4,21,450,195,1.7,4,12,2,22,14,LB,202,33752
18,-5,149,51,194,1.7,4,13,3,22,14,LB,201,33822
17,-1,242,121,193,1.7,4,14,4,21,14,LB,200,33476
17,-2,247,194,192,1.7,4,15,5,21,14,LB,199,33607
17,-3,251,68,191,1.7,5,0,6,21,14,LB,198,33705
17,-4,246,401,190,1.7,5,1,7,21,14,LB,197,33885
-1,-1,318,160,106,1.5,14,3,7,28,14,RB,212,33470
17,-5,244,58,189,1.7,5,2,8,21,14,LB,196,33944
-1,-2,319,66,105,1.5,14,4,8,28,14,RB,211,34017
16,-1,250,178,188,1.7,5,3,9,21,14,LB,195,33354
-1,-3,206,5,109,1.5,14,5,9,27,14,RB,210,33694
16,-2,245,344,187,1.7,5,4,10,21,14,LB,194,33585
-1,-4,205,372,103,1.5,14,6,10,27,14,RB,209,33730
16,-3,249,158,186,1.7,5,5,11,21,14,LB,193,33670
-1,-5,209,15,107,1.5,14,7,11,27,14,RB,208,34216
16,-4,243,99,185,1.7,5,6,12,21,14,LB,192,33880
-2,-2,322,387,100,1.5,14,8,12,28,14,RB,207,33783
16,-5,241,487,184,1.7,5,7,13,21,14,LB,191,33925
-2,-3,210,298,104,1.5,14,9,13,27,14,RB,206,33580
15,-1,54,422,183,1.7,5,8,14,20,14,LB,190,33410
-2,-4,214,48,99,1.5,14,10,14,27,14,RB,205,33709
15,-2,57,154,182,1.7,5,9,15,20,14,LB,189,33588
-2,-5,213,268,102,1.5,14,11,15,27,14,RB,204,33788
15,-3,58,454,181,1.7,5,10,16,20,14,LB,188,33738
-3,-2,323,201,101,1.5,14,12,16,28,14,RB,203,33506
21,-2,35,2,212,1.7,3,11,1,23,15,LB,219,33729
21,-3,28,21,211,1.7,3,12,2,23,15,LB,218,33748
21,-4,77,271,210,1.7,3,13,3,23,15,LB,217,33758
21,-5,127,91,209,1.7,3,14,4,23,15,LB,216,33802
20,-1,74,85,208,1.7,3,15,5,23,15,LB,215,33584
20,-2,145,256,207,1.7,4,0,6,23,15,LB,214,33699
20,-3,130,264,206,1.7,4,1,7,23,15,LB,213,33740
20,-4,26,100,205,1.7,4,2,8,23,15,LB,212,33755
20,-5,123,505,204,1.7,4,3,9,23,15,LB,211,33760
19,-1,131,175,203,1.7,4,4,10,22,15,LB,210,33621
19,-2,66,57,202,1.7,4,5,11,22,15,LB,209,33639
19,-3,122,491,201,1.7,4,6,12,22,15,LB,208,33709
19,-4,120,361,200,1.7,4,7,13,22,15,LB,207,33811
19,-5,65,312,199,1.7,4,8,14,22,15,LB,206,33917
18,-1,15,472,198,1.7,4,9,15,22,15,LB,205,33590
18,-2,75,429,197,1.7,4,10,16,22,15,LB,204,33635
23,-1,457,107,223,1.7,3,0,11,24,16,LB,230,33472
22,-2,456,37,217,1.7,3,6,12,24,16,LB,224,33653
23,-2,470,308,222,1.7,3,1,12,24,16,LB,229,33664
22,-3,451,200,216,1.7,3,7,13,24,16,LB,223,33666
23,-3,449,110,221,1.7,3,2,13,24,16,LB,228,33669
22,-4,479,229,215,1.7,3,8,14,24,16,LB,222,33681
23,-4,476,367,220,1.7,3,3,14,24,16,LB,227,33703
22,-5,448,94,214,1.7,3,9,15,24,16,LB,221,33795
23,-5,455,174,219,1.7,3,4,15,24,16,LB,226,33834
21,-1,83,409,213,1.7,3,10,16,23,16,LB,220,33588
22,-1,463,211,218,1.7,3,5,16,24,16,LB,225,33463'''


class ECalChannel:

  XOFF=23
  YOFF=5

  def __init__(self,a,b,c=None):

    if type(a) is list and type(b) is str:
      self.initFromSpreadsheet(a,b)
    elif type(a) is int and type(b) is int and type(c) is int:
      self.initFromFADC(a,b,c)
    else:
      sys.exit('Invalid Constructor.')

  def initData(self):
    self.vals['GAIN']=1.0
    self.vals['PED']=0.0
    self.vals['PEDRMS']=3.0
    self.vals['TET']=0

  def initFromFADC(self,crate,slot,chan):
    self.vals={}
    self.vals['DBID']=-1
    self.vals['FADCCRATE']=crate
    self.vals['FADCSLOT']=slot
    self.vals['FADCCHAN']=chan
    self.vals['X']=0
    self.vals['Y']=0
    self.initData()

  def initFromSpreadsheet(self,keys,csvRow):

    self.vals={}

    cols = csvRow.rstrip().lstrip().split(',')
    ncols = len(cols)

    if ncols!=14: sys.exit('Incorrect # of columns:  '+str(ncols))

    if ncols!=len(keys): sys.exit('Mismatch.')

    for ii in range(ncols):

      col=cols[ii]
      key=keys[ii].upper()

      if   key=='MB' or key=='PREAMP': self.vals[key]=str(col)
      elif key=='LEDDRIVER':           self.vals[key]=float(col)
      else:                            self.vals[key]=int(col)

    if self.vals['MB'].find('T')>=0: self.vals['FADCCRATE']=37
    else:                            self.vals['FADCCRATE']=39

    self.initData()
    self.setDBID()
    self.setTreeIndex()

  def dump(self):
    for key in self.vals.keys():
      print '%15s'%(key+'='+str(self.vals[key])),
    print

  def setDBID(self):
    x = self.vals['X']
    y = self.vals['Y']
    ix = x + self.XOFF
    iy = y + self.YOFF
    if x>0: ix -= 1
    if y>0: iy -= 1
    dbid = ix + 2*self.XOFF*(self.YOFF*2-iy-1) + 1;
    if   y== 1 and x>-10: dbid -= 9
    elif y==-1 and x<-10: dbid -= 9
    elif y<0:             dbid -= 18
    self.vals['DBID']=dbid

  def setTreeIndex(self):
    x = self.vals['X']
    y = self.vals['Y']
    iy = y+self.YOFF
    ix = x+self.XOFF
    if y>0: iy -= 1
    if x>0: ix -= 1
    self.vals['XINDEX'] = ix
    self.vals['YINDEX'] = iy




class ECalChannelCollection:

  def __init__(self,csvFileName=None):

    self.chans=[]
    self.keys=[]
    self.FADCslots=[3,4,5,6,7,8,9,14,15,16,17,18,19,20]
    self.FADCcrates={37:'hps1',39:'hps2',46:'hps11',58:'hps12'}
    self.ECALFADCcrates={37:'hps1',39:'hps2'}
    self.FADCchans=range(0,16)

    if csvFileName==None:
      csvTable=CSVTABLE.split('\n')
    else:
      if not os.path.isfile(csvFileName):
        sys.exit('Missing File:  '+csvFileName)
      csvTable=open(csvFileName)

    nRows=0
    for csvRow in csvTable:

      nRows += 1
      if nRows==1:
        self.keys=csvRow.rstrip().lstrip().split(',')
        if len(self.keys)!=14:
          sys.exit('Incorrect # of keys:  '+str(len(self.keys)))
        continue

      self.chans.append(ECalChannel(self.keys,csvRow))

    nEcalChannels=len(self.chans)

    for crate in self.ECALFADCcrates.keys():
      for chan in range(13,16):
         self.chans.append(ECalChannel(crate,20,chan))

    nNonEcalChannels = len(self.chans)-nEcalChannels

    print 'Loaded '+str(nEcalChannels)+' ECal Channels.'
    print 'Loaded '+str(nNonEcalChannels)+' Non-ECal Channels.'

  def comparePeds(self,chanelCollection):
    for dbid in range(1,443):
      cc1=self.findChannelDBID(dbid)
      cc2=channelCollection.findChannelDBID(dbid)
      print dbid,cc1.vals['PED'],cc2,vals['PED']

  def dump(self):
    for xx in self.chans: xx.dump()

  def findChannel(self,keyvals):
    if type(keyvals) is not tuple: return None
    if len(keyvals)%2 != 0:        return None
    for chan in self.chans:
      match=True
      for ii in range(0,len(keyvals),2):
        key = keyvals[ii]
        val = keyvals[ii+1]
        if not key in chan.vals:
          sys.exit('Missing Key:  '+key)
        if chan.vals[key] != val:
          match=False
          break
      if match:
        return chan
    print('Missing:  ')
    print(keyvals)

  def findChannelXY(self,x,y):
    return self.findChannel(('X',x,'Y',y))

  def findChannelDBID(self,dbid):
    return self.findChannel(('DBID',dbid))

  def findChannelFADC(self,crate,slot,chan):
    return self.findChannel(
        ('FADCCRATE',crate,'FADCSLOT',slot,'FADCCHAN',chan))

  def getGainFADC(self,crate,slot,chan):
    return float(self.findChannelFADC(crate,slot,chan).vals['GAIN'])
  def getThreshFADC(self,crate,slot,chan):
    return int(self.findChannelFADC(crate,slot,chan).vals['TET'])
  def getPedFADC(self,crate,slot,chan):
    return float(self.findChannelFADC(crate,slot,chan).vals['PED'])
  def getNoiseFADC(self,crate,slot,chan):
    return float(self.findChannelFADC(crate,slot,chan).vals['PEDRMS'])


  def isValidFADC(self,crate,slot,chan):
    if not crate in self.FADCcrates.keys():
      return False
    if not slot in self.FADCslots:
      return False
    if not chan in self.FADCchans:
      return False
    if slot==20  and chan>12:
      return False
    return True

  def xy2fadc(self,x,y):
    cc=self.findChannelXY(x,y)
    return (cc.vals["FADCSLOT"],cc.vals["FADCCHAN"])

  def fadc2xy(self,crate,slot,chan):
    cc=self.findChannelFADC(crate,slot,chan)
    return (cc.vals["X"],cc.vals["Y"])

  def printXY(self,x,y):
    cc=self.findChannelXY(x,y)
    for xx in self.keys:
      print xx+' = '+str(cc.vals[xx.upper()])

class ECalCollectionIO:

  def loadEvioConfig(self,channelCollection,filename=None):

    if filename==None: return

    evio2xml='/usr/local/clas12/release/0.2/coda/Linux_i686/bin/evio2xml4.0'
    cmd='%s -max 10 %s | egrep -B10 \'FADC|SSP\''%(evio2xml,filename)
    pp=Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    self.loadDaqConfig(channelCollection,pp.stdout)

#    ftmp=tempfile.NamedTemporaryFile()
#    os.system('echo aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
#    os.system('cat '+ftmp.name)
#    self.loadDaqConfig(channelCollection,ftmp.name)
#    ftmp.close()
#    for xx in pp.stdout:
#      print xx.rstrip()

  def loadDaqConfig(self,channelCollection,filename=None):

    if filename==None: return

    print "Reading DAQ Config:  ",filename

    slot=-1
    crate=-1

    # fix this hackery:
    datas=[]
    if type(filename) is str:
      ff = open(filename, 'r')
      for xx in ff:
        datas.append(xx)
    else:
      datas = filename


    for data in datas:

      daqrows=data.lstrip().rstrip().split('\n')

      for daqrow in daqrows:

        cols=daqrow.split()
        if len(cols)<2: continue

        # CRATE LINE:
        if daqrow.find('tag="57614"')>=0:
          if daqrow.find('num="37"')>=0:   crate=37
          elif daqrow.find('num="39"')>=0: crate=39
          elif daqrow.find('num="46"')>=0: crate=46
          continue

        # CRATE LINE:
        if daqrow.find('FADC250_CRATE')>=0:
          for key in channelCollection.FADCcrates:
            if channelCollection.FADCcrates[key]==cols[1].rstrip():
              crate=key
          continue

        # IGNORE NON-ECAL CRATES:
        if crate!=37 and crate!=39:
          continue;

        # SLOT LINE:
        key = cols.pop(0)
        if key.find('FADC250_SLOT')>=0:
          if cols[0] != 'all': slot = int(cols[0])
          continue

        # PEDESTAL/TET/GAIN LINE:
        if key.find('FADC250_ALLCH')>=0:

          if slot<0 or crate<0:
            sys.exit('FADC250_ALLCH found without a crate,slot:  %d,%d'%(crate,slot))

          if len(cols) != 16:
            sys.exit('FADC250_ALLCH_* Format Error:  '+cols)

          key = key.replace('FADC250_ALLCH_','')

          if crate==37 or crate==39:
            for chan in range(len(cols)):
              if key=='TET': val=int(cols[chan])
              else:          val=float(cols[chan])
              channelCollection.findChannelFADC(crate,slot,chan).vals[key]=val

  def loadDbPedestals(self,channelCollection,filename=None):

    if filename==None: return

    print "Reading DB Pedestals:  ",filename

    cc=channelCollection

    nlines=0
    for line in open(filename):
      nlines += 1
      if nlines==1: continue
      cols=line.rstrip().lstrip().split()
      dbid=int(cols[0])
      ped=float(cols[1])
      rms=float(cols[2])
      cc.findChannelDBID(dbid).vals['PED']=ped
      cc.findChannelDBID(dbid).vals['PEDRMS']=rms

  def loadTreeGains(self,channelCollection,filename=None):

    if filename==None: return

    print "Reading TTree Gains:  ",filename

    cc=channelCollection

    for line in open(filename):
      cols=line.rstrip().lstrip().split()
      ix=int(cols[0])
      iy=int(cols[1])
      gain=float(cols[2])
      cc.findChannel(('XINDEX',ix,'YINDEX',iy)).vals['GAIN']=gain

  def loadTreePedestals(self,channelCollection,filename=None):

    if filename==None: return

    print "Reading TTree Pedestals:  ",filename

    cc=channelCollection

    for line in open(filename):
      cols=line.rstrip().lstrip().split()
      ix=int(cols[0])
      iy=int(cols[1])
      ped=float(cols[2])
      if len(cols)>3:
        noise=float(cols[3])
      cc.findChannel(('XINDEX',ix,'YINDEX',iy)).vals['PED']=ped
      cc.findChannel(('XINDEX',ix,'YINDEX',iy)).vals['PEDRMS']=noise

  def printGainsForDB(self,channelCollection,filePrefix):

    if filePrefix==None:
      oo=sys.stdout
    else:
      if os.path.isfile(filePrefix+'_DB_gains.txt'):
        sys.exit('File Already Exists:   '+filePrefix+'_DB_gain.txt')
      print 'Writing DB gain file:  '+filePrefix+'_DB_gain.txt'
      oo=open(filePrefix+'_DB_gains.txt','w')

    cc=channelCollection

    print >>oo, 'ecal_channel_id gain'
    for dbid in range(1,442+1):
      ch=cc.findChannelDBID(dbid)
      print >>oo, '%3d %7.3f'%(dbid,ch.vals['GAIN'])

  def printPedestalsForDB(self,channelCollection,filePrefix):

    if filePrefix==None:
      oo=sys.stdout
    else:
      if os.path.isfile(filePrefix+'_DB_ped.txt'):
        sys.exit('File Already Exists:   '+filePrefix+'_DB_ped.txt')
      print 'Writing DB pedestal file:  '+filePrefix+'_DB_ped.txt'
      oo=open(filePrefix+'_DB_peds.txt','w')

    cc=channelCollection

    print >>oo, 'ecal_channel_id pedestal noise'
    for dbid in range(1,442+1):
      ch=cc.findChannelDBID(dbid)
      print >>oo, '%3d %7.3f %5.3f'%(dbid,ch.vals['PED'],ch.vals['PEDRMS'])

#  def printDaqSlotConfig(self,channelCollection,key):
#    print 'FADC_ALLCH_'+key+' ',
#    for chain in cc.FADCchans:


  def printThreshForDAQ(self,channelCollection,filePrefix):
    if filePrefix==None:
      oo=sys.stdout
    else:
      if os.path.isfile(filePrefix+'_DAQ_thresh.txt'):
        sys.exit('File Already Exists:   '+filePrefix+'_DAQ_thresh.txt')
      print 'Writing DAQ threshold file:  '+filePrefix+'_DAQ_thresh.txt'
      oo=open(filePrefix+'_DAQ_thresh.txt','w')

    cc=channelCollection

    for crate in cc.FADCcrates.keys():
      print >>o, 'FADC250_CRATE ',cc.FADCcrates[crate]

      for slot in cc.FADCslots:

        print >>oo, 'FADC250_SLOT ',slot

        print 'FADC250_ALLCH_TET ',
        for chan in cc.FADCchans:
           print >>oo, '%5d'%(cc.getThreshFADC(crate,slot,chan)),
        print >>oo

      print >>oo, 'FADC250_CRATE end'

    oo.close()

  def printPedestalsForDAQ(self,channelCollection,filePrefix,newFormat):

    if filePrefix==None:
      oo=sys.stdout

    cc=channelCollection

    if newFormat:
      if filePrefix!=None:
        if os.path.isfile(filePrefix+'_DAQ_ped.txt'):
          sys.exit('File Already Exists:   '+filePrefix+'_DAQ_ped.txt')
        print 'Writing DAQ pedestal file (NEW FORMAT):  '+filePrefix+'_DAQ_ped.txt'
        oo=open(filePrefix+'_DAQ_ped.txt','w')
      for crate in cc.ECALFADCcrates.keys():
        print >>oo, 'FADC250_CRATE ',cc.FADCcrates[crate]
        for slot in cc.FADCslots:
          print >>oo, 'FADC250_SLOT ',slot
          print >>oo, 'FADC250_ALLCH_PED ',
          for chan in cc.FADCchans:
             print >>oo, '%7.3f'%(cc.getPedFADC(crate,slot,chan)),
          print >>oo
        print >>oo, 'FADC250_CRATE end'
    else:
      for crate in cc.ECALFADCcrates.keys():
        if filePrefix!=None:
          if os.path.isfile(filePrefix+'_DAQ_ped.txt'):
            sys.exit('File Already Exists:   '+filePrefix+'_DAQ_ped_fadc'+str(crate)+'.txt')
          print 'Writing DAQ pedestal file:  '+filePrefix+'_DAQ_ped_fadc'+str(crate)+'.txt'
          oo=open(filePrefix+'_DAQ_ped_fadc'+str(crate)+'.txt','w')
        for slot in cc.FADCslots:
          for chan in cc.FADCchans:
            print >>oo, '%2d %2d %7.3f %7.3f %3d'%(slot,chan,cc.getPedFADC(crate,slot,chan),cc.getNoiseFADC(crate,slot,chan),0)

    oo.close()

  def printGainsForDAQ(self,channelCollection,filePrefix):

    if filePrefix==None:
      oo=sys.stdout
    else:
      if os.path.isfile(filePrefix+'_DAQ_gain.txt'):
        sys.exit('File Already Exists:   '+filePrefix+'_DAQ_gain.txt')
      print 'Writing DAQ gain file:  '+filePrefix+'_DAQ_gain.txt'
      oo=open(filePrefix+'_DAQ_gain.txt','w')

    cc=channelCollection

    for crate in cc.FADCcrates.keys():
      print >>oo, 'FADC250_CRATE ',cc.FADCcrates[crate]

      for slot in cc.FADCslots:

        print >>oo, 'FADC250_SLOT ',slot

        print >>oo, 'FADC250_ALLCH_GAIN ',
        for chan in cc.FADCchans:
           print >>oo, '%7.3f'%(cc.getGainFADC(crate,slot,chan)),
        print >>oo

      print >>oo, 'FADC250_CRATE end\n'

    oo.close()

def main():

  parser=argparse.ArgumentParser()

  # options:
  parser.add_argument('-X',dest='mode',action='store_true',help='Channel conversion mode.')
  parser.add_argument('-x',dest='x',default=None,help='crystal X')
  parser.add_argument('-y',dest='y',default=None,help='crystal Y')
  parser.add_argument('-crate',dest='crate',default=None,help='fadc crate')
  parser.add_argument('-slot',dest='slot',default=None,help='fadc slot')
  parser.add_argument('-channel',dest='channel',default=None,help='fadc channel')

  # input options:
  parser.add_argument('-w',dest='inputWiringFile',default=None,help='full wiring spreadsheet, else use internal one' )
  parser.add_argument('-d',dest='inputDaqFile', default=None,help='load input file in DAQ config file format.')
  parser.add_argument('-b',dest='inputDbPedFile', default=None,help='load input pedestals from DB file format.')
  parser.add_argument('-e',dest='inputEvioFile',default=None,help='load gains and peds from EVIO file via evio2xml.')
  parser.add_argument('-p',dest='inputTreePedFile',default=None,help='load pedestals via array indices.  {ix iy ped [rms]}')
  parser.add_argument('-g',dest='inputTreeGainFile',default=None,help='load gains via array indices. {ix iy gain}')

  # output options:
  parser.add_argument('-O',dest='outputFilePrefix', default=None,help='set prefix for output filenames (else stdout)')
  parser.add_argument('-S',dest='printSpreadsheet',action='store_true',help='dump dict from spreadsheet to stdout for testing')
  parser.add_argument('-DB',dest='printDatabase',action='store_true',help='output includes formatting for conditions database')
  parser.add_argument('-DAQ',dest='printDAQ',action='store_true',help='output includes formatting for DAQ')
  parser.add_argument('-P',dest='printPedestals',action='store_true',help='output includes pedestals')
  parser.add_argument('-G',dest='printGains',action='store_true',help='output includes gains')
  parser.add_argument('-N',dest='newPedFormatDAQ',action='store_true',help='format pedestals for new DAQ format')

  # compare options:
  parser.add_argument('-CP',dest='comparePeds',action='store_true',help='compare two pedestal files')
  parser.add_argument('-CG',dest='compareGains',default=None,help='compare two gains files')
  parser.add_argument('-d2',dest='inputDaqFile2',default=None,help='2nd DAQ Config file to compare')

  args=parser.parse_args()

  io=ECalCollectionIO()
  chans=ECalChannelCollection(args.inputWiringFile)

  if args.comparePeds:
    chans2=ECalChannelCollection(args.inputWiringFile)
    io.loadDaqConfig(chans,args.inputDaqFile)
    io.loadDaqConfig(chans2,args.inputDaqFile2)
    chans.comparePeds(chans2)

  if args.mode:
    if args.x!=None and args.y!=None:
      slotchan=chans.xy2fadc(int(args.x),int(args.y))
      chans.printXY(int(args.x),int(args.y))
      print '(%s,%s)=(%d,%d)'%(args.x,args.y,slotchan[0],slotchan[1])
    elif args.crate!=None and args.slot!=None and args.chan!=None:
      xy=chans.fadc2xy(int(args.crate),int(args.slot),int(args.chan))
      print '(%s,%s,%s)=(%d,%d)'%(args.crate,args.slot,args.chan,xy[0],xy[1])
    else:
      print 'NO.'
    sys.exit()

  if args.printSpreadsheet:
    chans.dump()

  io.loadDbPedestals(chans,args.inputDbPedFile)
  io.loadEvioConfig(chans,args.inputEvioFile)
  io.loadDaqConfig(chans,args.inputDaqFile)
  io.loadTreePedestals(chans,args.inputTreePedFile)
  io.loadTreeGains(chans,args.inputTreeGainFile)


  if args.printDAQ:
    if args.printGains:
      io.printGainsForDAQ(chans,args.outputFilePrefix)
    if args.printPedestals:
      io.printPedestalsForDAQ(chans,args.outputFilePrefix,args.newPedFormatDAQ)

  if args.printDatabase:
    if args.printGains:
      io.printGainsForDB(chans,args.outputFilePrefix)
    if args.printPedestals:
      io.printPedestalsForDB(chans,args.outputFilePrefix)

  if args.printSpreadsheet:
    chans.dump()


if __name__ == '__main__': main()


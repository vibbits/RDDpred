# RDDpred Docker Container
I do not own any rights of this software. This is solely available on GitHub for testing purposes. Please refer to the authors of the software for any other questions: http://epigenomics.snu.ac.kr/RDDpred/. 

Container build around RDDpred version 1.1 with adjustments in favour of this container. 

Test whether it's working with the following commands:

```
sudo docker build -t rddpred-github:1.1.3
sudo docker run rddpred-github:1.1.3 python RDDpred.py
``` 

Original RDDpred.py file = `RDDpred.py.org`
Original README file     = `README-org`
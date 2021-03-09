# RDDpred - Docker Container

This repository contains a Docker container, build around RDDpred version 1.1 with adjustments in favour of this container. 

This software is part of the following publication: 
> Kim, M. S., Hur, B., & Kim, S. (2016, January). RDDpred: a condition-specific RNA-editing prediction model from RNA-seq data. In BMC genomics (Vol. 17, No. 1, p. 5). BioMed Central.

Please refer to the authors of the software for any questions: http://epigenomics.snu.ac.kr/RDDpred/. 


**Test** whether it's working with the following commands:

```
docker build -t rddpred-github:1.1.3
docker run rddpred-github:1.1.3 python RDDpred.py
``` 

Original RDDpred.py file = `RDDpred.py.org`

Original README file     = `README-org`

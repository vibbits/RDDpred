# docker build -t rddpred-github:1.1.3
# docker run rddpred-github:1.1.3 python RDDpred.py


########## BASE IMAGE ############
FROM continuumio/miniconda3:latest 


########### METADATA #############
# Arguments
ARG software_version=1.1
LABEL base_image="continuumio/miniconda3:latest"
LABEL software="RDDpred"
LABEL software.version="$software_version"
LABEL about.summary="A condition-specific RNA-editing prediction model from RNA-seq data"
LABEL about.home="http://epigenomics.snu.ac.kr/RDDpred/"
LABEL about.documentation="http://epigenomics.snu.ac.kr/RDDpred/"
LABEL about.tags="Epitranscriptomics"
LABEL description="This Docker Container installs RDDpred software. The software has been slightly adapted in favour of the container. "
LABEL maintainer="VIB Bioinformatics Core (tuur.muyldermans@vib.be"

# Installing dependencies that are not in a conda environment
# Install jre requires man folder to exist on the server
RUN mkdir -p /usr/share/man/man1
RUN apt-get update -y && apt-get install -y \ 
	default-jre \
	weka \
	libsvm-java \ 
    libncurses5 

# && apt-get clean && apt-get purge

# Explicit package names --> rather put them in environment yml file
# RUN conda create -y -n tmp-env -f env.yml
RUN conda config --add channels conda-forge && \ 
    conda config --add channels bioconda && \
    conda config --append channels hcc && \
    conda create -y -n tmp-env python=2.7 numpy=1.16.5 bamtools=2.4.0 bcftools=1.2 htslib=1.2.1 samtools=1.2 weka=3.8.1

# Defining the workdirectory and adding the software to this workdir
WORKDIR /code
ADD . /code/

# Activating the conda environment by appending to bashrc file. 
RUN echo "source activate tmp-env" >> ~/.bashrc

# Add conda env path to workdir path. 
ENV PATH /opt/conda/envs/tmp-env/bin:$PATH


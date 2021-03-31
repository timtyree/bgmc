# docker pull rapidsai/rapidsai:cuda10.2-runtime-ubuntu18.04-py3.7
# docker run --gpus all --rm -it \
# -p 8888:8888 -p 8787:8787 -p 8786:8786 rapidsai/rapidsai:cuda10.2-runtime-ubuntu18.04-py3.7 \


# -v /home/timothytyree/Documents/GitHub/bgmc/python:/rapids/notebooks/host
#then type $ jupyter notebook list and go to the url listed.  badaboom.
#
docker run --gpus all --rm -it --name devtest \
-p 8888:8888 -p 8787:8787 -p 8786:8786 \
--mount type=bind,source="$(pwd)/..",target=/rapids/notebooks/host \
rapidsai/rapidsai:cuda10.2-runtime-ubuntu18.04-py3.7

#help found at
# https://docs.docker.com/storage/bind-mounts/

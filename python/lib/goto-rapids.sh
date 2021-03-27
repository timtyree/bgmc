# docker pull rapidsai/rapidsai:cuda10.2-runtime-ubuntu18.04-py3.7
docker run --gpus all --rm -it \
-p 8890:8888 -p 8787:8787 -p 8786:8786 rapidsai/rapidsai:cuda10.2-runtime-ubuntu18.04-py3.7 \
-v /home/timothytyree/Documents/GitHub/bgmc/python:/rapids/notebooks
#then type $ jupyter notebook list and go to the url listed.  badaboom.
#

echo 'data/osg_output/run_1_to_3_merged.csv'
echo 'needs to be loaded in a (gpu) notebook running on a virtual machine with at least 5.7GB of virtual memory.''
jupyter notebook --NotebookApp.max_buffer_size=10000000000

#GPU acceleration is not working
# # goto-rapids=alias
# docker run --gpus all --rm -it --name devtest \
# -p 8888:8888 -p 8787:8787 -p 8786:8786 \
# --mount type=bind,source="$(pwd)/..",target=/rapids/notebooks/host \
# --NotebookApp.max_buffer_size=10000000000 \
# rapidsai/rapidsai:cuda10.2-runtime-ubuntu18.04-py3.7
#
# goto-rapids=alias docker run --gpus all --rm -it --name devtest \
# -p 8888:8888 -p 8787:8787 -p 8786:8786 \
# --mount type=bind,source="$(pwd)/..",target=/rapids/notebooks/host \
# --NotebookApp.max_buffer_size=10000000000 \
# rapidsai/rapidsai:cuda10.2-runtime-ubuntu18.04-py3.7

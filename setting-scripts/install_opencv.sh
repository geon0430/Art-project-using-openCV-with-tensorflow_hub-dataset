#!/bin/bash

# Variables --------------------
CPU_ARCH=$(arch)
COMPUTE_CAPABILITY="6.0,6.1,7.0,7.5,8.0,8.6,8.9,9.0"
CUDNN_VERSION="8"
OPENCV_VERSION="4.8.1"
OPENCV_CONTRIB_VERSION="4.8.1"
PYTHON3_VERSION="3.8"
#-------------------------------

# OpenCV build --------------------------------------------------------------------------------------------
cd / && \
mkdir -p /tmp/opencv && \
cd /tmp/opencv && \
	wget https://github.com/opencv/opencv/archive/refs/tags/${OPENCV_VERSION}.zip -O opencv.zip && \
		unzip -qq opencv.zip && \
		rm opencv.zip && \
	wget https://github.com/opencv/opencv_contrib/archive/refs/tags/${OPENCV_CONTRIB_VERSION}.zip -O opencv-co.zip && \
		unzip -qq opencv-co.zip && \
		rm opencv-co.zip && \
	cd opencv-${OPENCV_VERSION} && \
		mkdir build && \
		cd build && \
			cmake \
				-D BUILD_DOCS=OFF \
				-D BUILD_EXAMPLES=OFF \
				-D BUILD_JAVA=OFF \
				-D BUILD_opencv_cudacodec=ON \
				-D BUILD_opencv_java=OFF \
				-D BUILD_PACKAGE=OFF \
				-D BUILD_PERF_TESTS=ON \
				-D BUILD_TESTS=OFF \
				-D BUILD_JPEG=ON \
				-D CMAKE_BUILD_TYPE=RELEASE \
				-D CMAKE_C_COMPILER=/usr/bin/gcc-9 \
				-D CMAKE_INSTALL_PREFIX=/usr/local \
				-D CMAKE_LIBRARY_PATH=/usr/local/cuda/lib64/stubs \
				-D CUDA_ARCH_BIN=${COMPUTE_CAPABILITY} \
				-D CUDA_ARCH_PTX=${COMPUTE_CAPABILITY} \
				-D CUDA_FAST_MATH=1 \
				-D CUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda \
				-D CUDNN_LIBRARY=/usr/lib/${CPU_ARCH}-linux-gnu/libcudnn.so.${CUDNN_VERSION} \
				-D ENABLE_FAST_MATH=1 \
				-D OPENCV_DNN_CUDA=ON \
				-D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-${OPENCV_CONTRIB_VERSION}/modules \
				-D OPENCV_GENERATE_PKGCONFIG=ON \
				-D PYTHON_EXECUTABLE=/usr/bin/python${PYTHON3_VERSION} \
				-D PYTHON3_EXECUTABLE=/usr/bin/python3 \
				-D PYTHON3_INCLUDE_DIR=/usr/include/python${PYTHON3_VERSION} \
				-D PYTHON3_LIBRARY=/usr/lib/${CPU_ARCH}-linux-gnu/libpython${PYTHON3_VERSION}.so \
				-D PYTHON3_NUMPY_INCLUDE_DIRS=/usr/local/lib/python${PYTHON3_VERSION}/dist-packages/numpy/core/include \
				-D PYTHON3_PACKAGES_PATH=/usr/local/lib/python${PYTHON3_VERSION}/dist-packages \
				-D WITH_CUBLAS=ON \
				-D WITH_CUDA=ON \
				-D WITH_CUDNN=ON \
				-D WITH_CUFFT=ON \
				-D WITH_EIGEN=ON \
				-D WITH_IPP=OFF \
				-D WITH_LIBV4L=ON \
				-D WITH_NVCUVID=ON \
				-D WITH_OPENGL=OFF \
				-D WITH_QT=OFF \
				-D WITH_SIMD=ON \
				-D WITH_LIBJPEG_TURBO_SIMD=ON \
				-D WITH_TBB=ON \
					.. && \
			make -j$(nproc) && \
			make -j$(nproc) install && \
			ldconfig

rm -r /tmp/opencv


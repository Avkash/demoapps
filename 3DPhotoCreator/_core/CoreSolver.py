import streamlit as st
from datetime import datetime

import random
import numpy as np
from PIL import Image
from scipy import stats
from imageio import imsave
import matplotlib.pyplot as plt
from skimage.util.shape import view_as_blocks

import image_slicer

import skimage.io

import utils.globalDefine as globalDefine

import core.ImageFormater as ImageFormater
import core.ImageScrambler as ImageScrambler
import core.ImageToTrainAndTestData as ImageToTrainAndTestData
import core.ModelBuilder as ModelBuilder

model = None


def run_main(title, subtitle):
    st.write("Puzzle Solution Walkthrough")    
    frameST = st.empty()

    st.sidebar.title(title)
    st.sidebar.info(
        subtitle
    )

    puzzlesize_keys = globalDefine.PUZZLE_SIZE.keys()    
    puzzlesize_id = st.sidebar.selectbox("Select Puzzle Size: ", list(puzzlesize_keys))
    puzzle_size = globalDefine.PUZZLE_SIZE.get(puzzlesize_id)

    imageList = globalDefine.IMAGE_LIST.keys()    
    img = st.sidebar.selectbox("Select Image: ", list(imageList))
    imgUrl = globalDefine.IMAGE_LIST.get(img)

    ##puzzle_size = st.sidebar.slider("Select Puzzle Size (2x2, 3x3, 4x4, 5x5):", 2,5,4,1)
    ##frameST.image(imgUrl, channels="BGR")
    input_img_url = ImageFormater.setup_image_requirements(imgUrl, puzzle_size)

    original_image_np=np.array(Image.open(input_img_url).convert('RGB'))
    st.image(original_image_np)

    if st.checkbox("Shuffle Image? "):
        shuffled_image_np, original_image_blocks, key_map_orig, blk_size, shuffle_img_blks = ImageScrambler.shuffle_image(original_image_np, puzzle_size)
        st.image(shuffled_image_np)

    ## Using Shuffled Image
    if st.checkbox("Generate Training Data? "):
        training_image_files = ImageToTrainAndTestData.generate_training_data(shuffled_image_np, puzzle_size)

    ## Using Original Image
    if st.checkbox("Generate Test Data? "):
        test_image_files = ImageToTrainAndTestData.generate_test_data(input_img_url, puzzle_size)

    if st.checkbox("Verify Training Data? "):
        st.write("Total ", len(training_image_files), " files are generated!!")
        ## TODO: Verify all the files on disk to make sure they do exist

    if st.checkbox("Verify Test Data? "):
        st.write("Total ", len(test_image_files), " files are generated!!")
        ## TODO: Verify all the files on disk to make sure they do exist

    if st.checkbox("Load Traing and Test Data for Deep Learning? "):
        imgs_train = ImageToTrainAndTestData.load_images_into_memory(training_image_files, "train_img", 'train')
        imgs_test = ImageToTrainAndTestData.load_images_into_memory(test_image_files, "test_img",  'test')
        ##shape_img = imgs_train[0].shape
        ##print("Image shape = {}".format(shape_img))
        st.write("Total ", len(imgs_train), " training and ", len(imgs_test), " test images are loaded into memory for deep learning")

    model_list_keys = globalDefine.MODELS_LIST.keys()
    model_master_id = st.selectbox("Select Network type: ", list(model_list_keys), 0)
    model_master = globalDefine.MODELS_LIST.get(model_master_id)

    n_epochs = None
    epoch_limit = 0
    if model_master == "simpleAE":
        n_epochs = 300
    elif model_master == 'convAE':
        n_epochs = 500
    else:
        n_epochs = None
    
    if st.checkbox("Current epochs setting is  {} . Do you want to modify it? ".format(n_epochs)):
        n_epochs = st.slider("Select epochs between 50 to {}:".format(epoch_limit), 50,500,200,25)

    if st.checkbox("Prepare model configuration? "):
        shape_img = imgs_train[0].shape
        model, shape_img_resize, input_shape_model, output_shape_model, n_epochs, outDir = ModelBuilder.config_model_builder(model_master, shape_img)
    
    if st.checkbox("Show model summary? "):
        if model_master in ["simpleAE", "convAE"]:
            st.write(model.info)
        elif model_master in ["vgg19"]:
            st.write(model.summary())

    if st.checkbox("Transforming training and test data based on selected model type? "):
        X_train, X_test = ModelBuilder.applying_transformer(shape_img_resize, imgs_train, imgs_test, input_shape_model)

    if st.checkbox("Start building model and save to disk after completion. (This process will run {} times)?".format(n_epochs)):
        all_model_files = ModelBuilder.get_saved_models_info(outDir)
        if (len(all_model_files)) == 0:
            model = ModelBuilder.start_batch_process(model_master, X_train, model, n_epochs)
        else:
            st.write("Model is already available....")
            if st.checkbox("Do you want to rebuild the model? "):
                model = ModelBuilder.start_batch_process(model_master, X_train, model, n_epochs)


    if st.checkbox("Verify model stored into disk? "):
        all_model_files = ModelBuilder.get_saved_models_info(outDir)
        st.write(all_model_files)

    if st.checkbox("Generate embeddings by using model? "):
        E_train_flatten, E_test_flatten = ModelBuilder.generate_embedding_from_model(model, X_train, X_test, output_shape_model)
    
    if st.checkbox("Fit KNN Model"):
        knn_neighbors = 5
        knn_metric = "cosine"
        knn = ModelBuilder.fit_knn_model(E_train_flatten, knn_neighbors, knn_metric)
        st.write(knn)
        
    if st.checkbox("Generate final result map (image sequence)? "):
        final_list_map = ModelBuilder.generate_final_mapping_list(knn, E_test_flatten)
        st.write(final_list_map)

    if st.checkbox("Reconstruct result image based on image sequence? "):
        final_image_np = ModelBuilder.generate_final_result_image(shuffled_image_np, blk_size, puzzle_size, shuffle_img_blks, final_list_map)
        st.image(final_image_np)


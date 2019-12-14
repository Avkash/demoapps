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

import utils.filemgmt as filemgmt
import utils.display as udisp
import utils.globalDefine as globalDefine
import core.ImageFormater as ImageFormater
import core.ImageScrambler as ImageScrambler
import core.ImageToTrainAndTestData as ImageToTrainAndTestData
import core.ModelBuilder as ModelBuilder

def run_main(title, subtitle):
    st.write("Solve your Puzzle")    
    frameST = st.empty()

    st.sidebar.title("Choose selection..")

    if st.checkbox("Read Instructions before start? "):
        udisp.render_md("resources/beforeyoustart.md")

    puzzlesize_keys = globalDefine.PUZZLE_SIZE.keys()    
    puzzlesize_id = st.sidebar.selectbox("Select Puzzle Size: ", list(puzzlesize_keys))
    puzzle_size = globalDefine.PUZZLE_SIZE.get(puzzlesize_id)

    model_list_keys = globalDefine.MODELS_LIST.keys()
    model_master_id = st.sidebar.selectbox("Select Network type: ", list(model_list_keys), 0)
    model_master = globalDefine.MODELS_LIST.get(model_master_id)

    input_img_type_keys = globalDefine.INPUT_TYPES.keys()
    input_img_type_id = st.sidebar.selectbox("Select Image Location: ", list(input_img_type_keys))
    input_img_type = globalDefine.INPUT_TYPES.get(input_img_type_id)

    problem_img_path = st.text_input('Please input puzzle image file/url here...')
    solution_file_path = st.text_input('Please input target solution file/url here...')

    progress_start = False
    if st.checkbox("Validate input images and solve puzzle"):
        st.write("Validating input path....")
        if input_img_type == "LOCAL":
            problem_valid = filemgmt.validateLocalPath(problem_img_path)
            solution_valid = filemgmt.validateLocalPath(solution_file_path)
        else:
            problem_valid = filemgmt.validateUrlPath(problem_img_path)
            solution_valid = filemgmt.validateUrlPath(solution_file_path)

        if (problem_valid and solution_valid):
            st.write("Success: Both file contents are valid..")
            progress_start = True
        else:
            st.write("Error: Both file contents are invalid..")

    if progress_start:
        ##st.image(problem_img_path)
        ##st.image(solution_file_path)

        ## Step 1.1 - Original Input Image (Selected) >>> SOLUTION
        input_img_url = ImageFormater.setup_image_requirements(solution_file_path, puzzle_size)
        original_image_np=np.array(Image.open(input_img_url).convert('RGB'))
        st.image(original_image_np)

        ## Step 1.2 - Shuffled Image (Auto) >>>> PROBLEM
        ##shuffled_image_np, original_image_blocks, key_map_orig, blk_size, shuffle_img_blks = ImageScrambler.shuffle_image(problem_img_path, puzzle_size)
        problem_img_url = ImageFormater.setup_image_requirements(problem_img_path, puzzle_size)
        shuffled_image_np=np.array(Image.open(problem_img_url).convert('RGB'))
        st.image(shuffled_image_np)
        blk_size, shuffle_img_blks = ImageScrambler.zigsaw_image(shuffled_image_np, puzzle_size)

        st.title(" Start Solving Puzzle......")
        ## Using Shuffled Image
        st.write("Generating Training Data...")
        training_image_files = ImageToTrainAndTestData.generate_training_data(shuffled_image_np, puzzle_size)
        st.write("Total ", len(training_image_files), " training image files are generated!!")
        ## TODO: Verify all the files on disk to make sure they do exist

        ## Using Original Image
        st.write("Generating Test Data...")
        test_image_files = ImageToTrainAndTestData.generate_test_data(input_img_url, puzzle_size)
        st.write("Total ", len(test_image_files), " test image files are generated!!")
        ## TODO: Verify all the files on disk to make sure they do exist

        st.write("Loading Training and Test Data for Deep Learning... ")
        imgs_train = ImageToTrainAndTestData.load_images_into_memory(training_image_files, "train_img", 'train')
        imgs_test = ImageToTrainAndTestData.load_images_into_memory(test_image_files, "test_img",  'test')
        st.write("Total ", len(imgs_train), " training and ", len(imgs_test), " test images are loaded into memory for deep learning")

        st.title("Now starting deep learning using {} Network..".format(model_master))

        n_epochs = None

        st.write("Preparing model configuration...")
        shape_img = imgs_train[0].shape
        model, shape_img_resize, input_shape_model, output_shape_model, n_epochs, outDir = ModelBuilder.config_model_builder(model_master, shape_img)
        
        st.write("Displaying model summary.. ")
        if model_master in ["simpleAE", "convAE"]:
            st.write(model.info)
        elif model_master in ["vgg19"]:
            st.write(model.summary())

        st.write("Transforming training and test data based on selected model type.. ")
        X_train, X_test = ModelBuilder.applying_transformer(shape_img_resize, imgs_train, imgs_test, input_shape_model)

        st.write("First checking the stored model and if not found then building it..")
        all_model_files = ModelBuilder.get_saved_models_info(outDir)
        if (len(all_model_files)) == 0:
            st.write("Start building model (The batch counts are {} for this process.)... Please wait...".format(n_epochs))
            model = ModelBuilder.start_batch_process(model_master, X_train, model, n_epochs)
        else:
            st.write("Model is already available so we are not building it to expedite the demo......")


        st.write("Verifing model stored into disk..")
        all_model_files = ModelBuilder.get_saved_models_info(outDir)
        st.write(all_model_files)

        st.write("Generate embeddings by using model.. ")
        E_train_flatten, E_test_flatten = ModelBuilder.generate_embedding_from_model(model, X_train, X_test, output_shape_model)
        
        st.write("Fitting KNN Model..")
        knn_neighbors = 5
        knn_metric = "cosine"
        knn = ModelBuilder.fit_knn_model(E_train_flatten, knn_neighbors, knn_metric)
        st.write(knn)
            
        st.title("Generate final result map (image sequence)...")
        final_list_map = ModelBuilder.generate_final_mapping_list(knn, E_test_flatten)
        st.write(final_list_map)

        st.write("Reconstructing result image based on image sequence generate in previoud step... ")
        final_image_np = ModelBuilder.generate_final_result_image(shuffled_image_np, blk_size, puzzle_size, shuffle_img_blks, final_list_map)
        st.image(final_image_np)
import os
import numpy as np
import tensorflow as tf
from sklearn.neighbors import NearestNeighbors

from img_retrival_src.autoencoder import AutoEncoder
from img_retrival_src.CV_transform_utils import resize_img, normalize_img
from img_retrival_src.CV_IO_utils import read_imgs_dir
from img_retrival_src.CV_transform_utils import apply_transformer
from img_retrival_src.CV_transform_utils import resize_img, normalize_img
from img_retrival_src.CV_plot_utils import plot_query_retrieval, plot_tsne, plot_reconstructions

import core.ImageScrambler as ImageScrambler

outDir = None
## modelName = "convAE"  # try: "simpleAE", "convAE", "vgg19"

trainModel = True
parallel = False  
n_epochs_simpleAE = 300
n_epochs_convAE = 500

def setup_model_out_dir(modelName):
    outDir = os.path.join(os.getcwd(), "output", modelName)
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    return outDir

def config_model_builder(modelName, shape_img):
    ## Setting up OutDir
    outDir = setup_model_out_dir(modelName)
    # Build models
    if modelName in ["simpleAE", "convAE"]:
        # Set up autoencoder
        info = {
            "shape_img": shape_img,
            "autoencoderFile": os.path.join(outDir, "{}_autoecoder.h5".format(modelName)),
            "encoderFile": os.path.join(outDir, "{}_encoder.h5".format(modelName)),
            "decoderFile": os.path.join(outDir, "{}_decoder.h5".format(modelName)),
        }
        model = AutoEncoder(modelName, info)
        model.set_arch()

        if modelName == "simpleAE":
            shape_img_resize = shape_img
            input_shape_model = (model.encoder.input.shape[1],)
            output_shape_model = (model.encoder.output.shape[1],)
            n_epochs = n_epochs_simpleAE
        elif modelName == "convAE":
            shape_img_resize = shape_img
            input_shape_model = tuple([int(x) for x in model.encoder.input.shape[1:]])
            output_shape_model = tuple([int(x) for x in model.encoder.output.shape[1:]])
            n_epochs = n_epochs_convAE
        else:
            raise Exception("Invalid modelName!")

    elif modelName in ["vgg19"]:

        # Load pre-trained VGG19 model + higher level layers
        print("Loading VGG19 pre-trained model...")
        model = tf.keras.applications.VGG19(weights='imagenet', include_top=False,
                                            input_shape=shape_img)
        model.summary()

        shape_img_resize = tuple([int(x) for x in model.input.shape[1:]])
        input_shape_model = tuple([int(x) for x in model.input.shape[1:]])
        output_shape_model = tuple([int(x) for x in model.output.shape[1:]])
        n_epochs = None

    else:
        raise Exception("Invalid modelName!")

    return model, shape_img_resize, input_shape_model, output_shape_model, n_epochs, outDir

def applying_transformer(shape_img_resize, imgs_train, imgs_test, input_shape_model):
    # Apply transformations to all images
    class ImageTransformer(object):
        def __init__(self, shape_resize):
            self.shape_resize = shape_resize

        def __call__(self, img):
            img_transformed = resize_img(img, self.shape_resize)
            img_transformed = normalize_img(img_transformed)
            return img_transformed

    transformer = ImageTransformer(shape_img_resize)
    ##print("Applying image transformer to training images...")
    imgs_train_transformed = apply_transformer(imgs_train, transformer, parallel=parallel)
    ##print("Applying image transformer to test images...")
    imgs_test_transformed = apply_transformer(imgs_test, transformer, parallel=parallel)
    # Convert images to numpy array
    X_train = np.array(imgs_train_transformed).reshape((-1,) + input_shape_model)
    X_test = np.array(imgs_test_transformed).reshape((-1,) + input_shape_model)
    ##print(" -> X_train.shape = {}".format(X_train.shape))
    ##print(" -> X_test.shape = {}".format(X_test.shape))
    return X_train, X_test

def start_batch_process(modelName, X_train, model, n_epochs):
    # Train (if necessary)
    if modelName in ["simpleAE", "convAE"]:
        if trainModel:
            model.compile(loss="binary_crossentropy", optimizer="adam")
            model.fit(X_train, n_epochs=n_epochs, batch_size=256)
            model.save_models()
            ##trainModel = False
        else:
            model.load_models(loss="binary_crossentropy", optimizer="adam")
    return model


def get_saved_models_info(data_dir):
    all_files = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files


def generate_embedding_from_model(model, X_train, X_test, output_shape_model ):
    # Create embeddings using model
    ##print("Inferencing embeddings using pre-trained model...")
    E_train = model.predict(X_train)
    E_train_flatten = E_train.reshape((-1, np.prod(output_shape_model)))
    E_test = model.predict(X_test)
    E_test_flatten = E_test.reshape((-1, np.prod(output_shape_model)))
    ##print(" -> E_train.shape = {}".format(E_train.shape))
    ##print(" -> E_test.shape = {}".format(E_test.shape))
    ##print(" -> E_train_flatten.shape = {}".format(E_train_flatten.shape))
    ##print(" -> E_test_flatten.shape = {}".format(E_test_flatten.shape))
    return E_train_flatten, E_test_flatten

def make_reconstruction_visualizations(modelName, model, E_train, imgs_train,  shape_img_resize, E_train_flatten):
    # Make reconstruction visualizations
    if modelName in ["simpleAE", "convAE"]:
        ##print("Visualizing database image reconstructions...")
        imgs_train_reconstruct = model.decoder.predict(E_train)
        if modelName == "simpleAE":
            imgs_train_reconstruct = imgs_train_reconstruct.reshape((-1,) + shape_img_resize)
        plot_reconstructions(imgs_train, imgs_train_reconstruct,
                            os.path.join(outDir, "{}_reconstruct.png".format(modelName)),
                            range_imgs=[0, 255],
                            range_imgs_reconstruct=[0, 1])

def fit_knn_model(E_train_flatten, knn_neighbors, knn_metric):
    # Fit kNN model on training images
    ## print("Fitting k-nearest-neighbour model on training images...")
    knn = NearestNeighbors(n_neighbors=knn_neighbors, metric=knn_metric)
    knn.fit(E_train_flatten)
    return knn

def generate_final_mapping_list(knn, E_test_flatten):
    final_list_map = {}
    for i, emb_flatten in enumerate(E_test_flatten):
        _, indices = knn.kneighbors([emb_flatten])
        final_list_map[i] = indices[0][0]
    return final_list_map

def generate_final_result_image(shuffled_image, blk_size, row_col, shuffle_img_blks, final_list_map):
    ai_image = ImageScrambler.unscramble_image(shuffled_image, blk_size, row_col, shuffle_img_blks, final_list_map, sortMap=False)
    return ai_image
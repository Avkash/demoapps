

## Image Processing to rearrange problem and solution images
- User enters both source puzzle image and the solution images
- User also select the size of puzzle between 3x3 to 10x10
- Both images are resized to be square and size is in the multiple of puzzle size times 100. For example if you puzzle size is 5x5 then both images height and width will be 500
- Next step is to extract image blocks of size 100x100 from both source and solution images and saved to disk 
- Solution images are considers as test images which stroed with train_img_* prefix and problem images are saved with test_img_* prefix as training images.

## Creating Training and Test Dataset
- We read the shuffle problem image as training data and break into 100x100 images and save it into disk
  - ImageToTrainAndTestData.generate_training_data()
- We also read the targer solution image as test data and break into 100x100 blocks as save it also to disk
  - ImageToTrainAndTestData.generate_test_data()
- After both training and test images of fize 100x100 are generated, the next step is to load training and test image data into memory for model building
  - ImageToTrainAndTestData.load_images_into_memory()

## Bulding Deep Learning Model
- To build model we select the following first as configuration
  - Model Type : SimpleAE | convAE | VGG19
  - epochs - Total number of times the training process will be conducted, VGG19 requires no epocs.
- Each model type you select has a fixed required to read the training and test data. So after you select the model type you will have to transform the input training and test data to meet the model type requirements.
  - ModelBuilder.applying_transformer()
- Now we start the batch process by passing the model configuration, training image data and epochs
  - ModelBuilder.start_batch_process(()
- Once model is ready now we need to pass training and test data to generate the model embeddings
  - ModelBuilder.generate_embedding_from_model()
- To build KNN model will pass the number of neighbors and distance metrics along with flattened training image data
  - ModelBuilder.fit_knn_model()

## Generating results image map
- After KNN model is ready the we pass the solution puzzle images (flattened test data) to generate the image map sequence
  - ModelBuilder.generate_final_mapping_list()
- The final mapping sequence is sent to image processing function which rearrange the shuffle image blocks based on final image map.
  - ModelBuilder.generate_final_result_image()


## Credits 
- Please visit credits page to learn more about credits and code/tools
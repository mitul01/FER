# set matplotlib backend so figures can be saved in the background
import matplotlib
matplotlib.use("Agg")

# import packages
from config import emotion_config as config
from pipeline.preprocessing import ImageToArrayPreprocessor
from pipeline.callbacks import EpochCheckpoint
from pipeline.callbacks import TrainingMonitor
from pipeline.io import HDF5DatasetGenerator
from pipeline.nn.conv import EmotionVGGNet 
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import SGD
from keras.optimizers import Adam
from keras.models import load_model
from keras import backend as K
import argparse
import os

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--checkpoints", required = True,
    help = "path to output checkpoint directory")
ap.add_argument("-m", "--model", type = str,
    help = "path to specific model checkpoint to load")
ap.add_argument("-s", "--start_epoch", type = int, default = 0,
    help = "epoch to restart training at")
args = vars(ap.parse_args())

# construct the training and testing image generators for data
# augmentation, then initialize the image preprocessor
trainAug = ImageDataGenerator(rotation_range = 10, zoom_range = 0.1,
    horizontal_flip = True, rescale = 1 / 255.0, fill_mode = "nearest")
valAug = ImageDataGenerator(rescale = 1 / 255.0)
iap = ImageToArrayPreprocessor()

# initialize the training and validation dataset generators
trainGen = HDF5DatasetGenerator(config.TRAIN_HDF5, config.BATCH_SIZE,
    aug = trainAug, preprocessors = [iap], classes = config.NUM_CLASSES)
valGen = HDF5DatasetGenerator(config.VAL_HDF5, config.BATCH_SIZE,
    aug = valAug, preprocessors = [iap], classes = config.NUM_CLASSES)

# if there is no specific model checkpoint supplied, then initialize
# the network and compile the model
if args["model"] is None:
    print("compiling model...")
    model = EmotionVGGNet.build(width = 48, height = 48, depth = 1,
        classes = config.NUM_CLASSES)
    # opt = SGD(lr = 1e-2, momentum = 0.9, nesterov = True)
    opt = Adam(lr = 1e-3)
    model.compile(loss = "categorical_crossentropy", optimizer = opt,
        metrics = ["accuracy"])

# otherwise, load the checkpoint from disk
else:
    print("[INFO] loding {}...".format(args["model"]))
    model = load_model(args["model"])

    # update the learning rate
    print("[INFO] old learning rate: {}".format(K.get_value(model.optimizer.lr)))
    K.set_value(model.optimizer.lr, 1e-5)
    print("[INFO] new learning rate: {}".format(K.get_value(model.optimizer.lr)))

# construct the set of callbacks
figPath = os.path.sep.join([config.OUTPUT_PATH, "vggnet_emotion_4.png"])
jsonPath = os.path.sep.join([config.OUTPUT_PATH, "vggnet_emotion_4.json"])
callbacks = [
    EpochCheckpoint(args["checkpoints"], every = 5, startAt = args["start_epoch"]),
    TrainingMonitor(figPath, jsonPath = jsonPath, startAt = args["start_epoch"])
]

# train network
model.fit_generator(
    trainGen.generator(),
    steps_per_epoch = trainGen.numImages // config.BATCH_SIZE,
    validation_data = valGen.generator(),
    validation_steps = valGen.numImages // config.BATCH_SIZE,
    epochs = 15,
    max_queue_size = config.BATCH_SIZE * 2,
    callbacks = callbacks,
    verbose = 1
)

# close the dataset
trainGen.close()
valGen.close()

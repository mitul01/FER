# FER

## About Dataset 
The data consists of 48x48 pixel grayscale images of faces. The faces have been automatically registered so that the face is more or less centered and occupies about the same amount of space in each image. The task is to categorize each face based on the emotion shown in the facial expression in to one of six categories (0=Angry, 1=Disgust, 2=Fear, 3=Happy, 4=Sad, 5=Surprise, 6=Neutral).

train.csv contains two columns, "emotion" and "pixels". The "emotion" column contains a numeric code ranging from 0 to 6, inclusive, for the emotion that is present in the image. The "pixels" column contains a string surrounded in quotes for each image. The contents of this string a space-separated pixel values in row major order. test.csv contains only the "pixels" column and your task is to predict the emotion column.

The training set consists of 28,709 examples. The public test set used for the leaderboard consists of 3,589 examples. The final test set, which was used to determine the winner of the competition, consists of another 3,589 examples.

This dataset was prepared by Pierre-Luc Carrier and Aaron Courville, as part of an ongoing research project.

src:- https://www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge/data

NOTE: No.of emotions have been reduced to 6. A class category of disgust (label=1) is labeled 0 (as anger only) to make the dataset more balanced. Very few training images were provided in original dataset for disgust class thus it was labeled as anger only to reduce biasness from the model. ( This step is carried out for all model implementation ) 


## Approaches Used 

| Model  | Test Accuracy |
| ------------- | ------------- |
| Xception  | 57.87  |
| Resnet  | 61.44  |
| FER_manual_1  | 67.35  |
| FER_manual_2  | --  |
| TransLearn_Oversampling_Resnet50  | 69.00  |

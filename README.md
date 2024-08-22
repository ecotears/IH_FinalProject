
# Pet Adoption Speed Prediction - Final Project




## Introduction
For the final project, I decided to work on a model that could actually improve or solve a current social problem. That's why I chose the **PetFinder Adoption Dataset** from **Kaggle**.

In **2023**, in the `US`, **6.5 million** of cats and dogs entered animal shelters (abandoned, returned, etc.)
In `Spain`, the number was **286 000** of animals abandoned from known data only!

This is why, building a model that efficiently and correctly predicts the adoption speed of abandoned animals could greatly help shelters and organizations to allocate their resources better or promote certain animals with predicted slow adoptions more.

We also developed a web application for our prediction tool using Streamlit and then deployed it on Heroku: Pet Adoption Prediction Application
## Variable context

**`General & key`**

|Variables | Variable description|
| :--- | :--- |
|Type| 1 = Dog, 2 = Cat|
|Gender|1 = Male, 2 = Female, 3 = Mixed|
|Age|Age of the animal when it was listed, in months|
|Name|I'll use it as whether the animal had a name or not|

**`Appearance related`**

|Variables | Variable description|
| :--- | :--- |
|Breed1|Primary breed|
|Breed2|Secondary breed|
|Color1|Primary color|
|Color2|Secondary color|
|Color3|Third color|
|MaturitySize|Size at maturity (1 = Small, 2 = Medium, 3 = Large, 4 = Extra Large, 0 = Not Specified)|
|FurLength|Fur length (1 = Short, 2 = Medium, 3 = Long, 0 = Not Specified)|

**`Health related`**
|Variables | Variable description|
| :--- | :--- |
|Vaccinated|Pet has been vaccinated (1 = Yes, 2 = No, 3 = Not Sure)|
|Dewormed|Pet has been dewormed (1 = Yes, 2 = No, 3 = Not Sure)|
|Sterilized|Pet has been spayed / neutered (1 = Yes, 2 = No, 3 = Not Sure)|
|Health|Health Condition (1 = Healthy, 2 = Minor Injury, 3 = Serious Injury, 0 = Not Specified)|

**`Informational elements`**
|Variables | Variable description|
| :--- | :--- |
|VideoAmt|Total uploaded videos for this pet|
|PhotoAmt|Total uploaded photos for this pet|
|Description score & magnitude|From description we have obtained the sentiment score and magnitude to see whether how the animal is described impacts adoption speed|

**`Miscellaneous`**

|Variables | Variable description|
| :--- | :--- |
|Quantity|Number of pets given for adoption. There are actually group adoptions given out.|
|Fee|Adoption fee (0 = Free)|

## EDA Conclusions

**1) General & key**

* Cats appear to have a faster adoption speed than dogs
* Younger animals have statistically significant faster adoptions than older animals
* A great part of the animals in the dataset young and < 1 year old
* Female and Mixed (when there is a group) animals have slower adoption speed

**2) Appearance related**
* No particular color mix makes the adoption speed faster/slower
* Unexpectedly, when the animal is pure breed, the adoption speed is slower
* The fastest breeds of dog to be adopted (above average) are: Rottweiler, Pug and Pomeranian. The slowest breeds of dog to be adopted are: Hound, Doberman Pinscher, Jack Russell Terrier.
* The fastest breeds of cat to be adopted (above average) are: Oriental Long Hair, Bengal, Persian. The slowest breeds of dog to be adopted are: Singapura, Burmese and Domestic Medium Hair.
* No clear difference in adoption speed when it comes to maturity size. However it seems that extra large dogs gets adopted easier than extra large Cats
* People absolutely love long fur animals

**3) Health related variables**
* Unexpected slower adoption speed for vaccinated animals
*  There doesn't seem to be a clear trend that not-dewormed animal get adopted slower. However, the not sure category does indeed spike up the group 4 (very slow adoption)
* The adoption gets significantly slower (group 4, and sometimes 3 spikes) when the animal is spayed or neutered!
* The more critical the health condition of the animal the slower the adoption speed

**4) Informational variables**
* There doesn't seem to be a clear indicator of whether the sentiment score or the magnitude of the description cause a faster or slower adoption
* Extremely slow adoption seems to have less photoes and videos. 

**5) Miscellaneous**
* Most of the dataset is single animal given for adoption
* 80% of animals are given for adoption for free
* We do have a higher amount of group animals in slow adoption groups (4). But they are sometimes adopted quite fast as well!
## Machine Learning Model

The model to be built is a **multiclass** one as we have in total 5 possible classifcations as output. **However**, I decided to group 0 (adoption the same day) and 1 (adoption the first week) together as there was very few examples of group 0, and they are quite redundante. So in the end, there are 4 possible classifications to predit --> 0,1,2,3.

The process of the model building has been the following one:

**1) Preprocessing the dataset**: For example, checking for nulls, changing variables, standard scaling numerical features, one-hot encoding categorical ones.

**2) Feature selection**: Assesing whether deleting some variables can help improve model's accuracy and selecting the best ones

**3) Hyperparameter tuning**: Used GridSearchCV to find the best hyperparameters for the model

After conducting the above steps, two main models were compared using their accuracy: **Random Forest** and **XGBoost**. I have to say that overall accuracy score was not the sole criterion, but I focused a lot on precision and recall for adoption group 3 (previously 4), which is the group that is still not adopted after 100 days. The reason is, if the model predicts incorrectly an animal that wil be adopted the first week, that is fine, however predicting incorrectly an animal that will not be adopted is a great deal.

After comparing the different models, and various versions with small details of difference. The final chosen model was a **Random Forest** with **`42%`** accuracy. However the recall rate for group 3 was almost **`70%`**!


## Tools used
Tools:
* Numpy, Pandas, Matplotlib, and Seaborn for data analysis and visualization
* Scipy and Pingouin for statistical signficance analysis
* Scikit-learn and XGB for model building
* Streamlit for web app design
* Github for web app deployment and version control
* Joblib to save the Data Science Model
* VS Code as IDE


Specific tools used with Scikit-learn + XGB:

* Models: RandomForestClassifier, XGBboost
* Features: OneHotEncoder, StandardScaler, ColumnTransformer
* GridSearchCV for hyperparameter tunning
* Pipeline so that everything will run smoothly and automatically once we recall the model from joblib

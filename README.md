# DeepLearning_Contribution
This is a repository for submitting my software contribution and report in the course of studying safety concepts for deep learning perception applications at DHBW Ravensburg.

## Software Contribution
Please note that the files *accuracy_log.py* and *signnames.txt* belong to Sarah Theuerkauf and are to be excluded from the scope of my SW contribution. However, they are part of this repository since elements of my SW implementation make use of the *mapping* function which is defined therein. 

### [Feature 1]: class_accuracy.py
The file *class_accuracy.py* defines a function that can be used to calculate the individual accuracy of each class in safetyBatch and has already been included in the provided validation pipeline, so to run this feature please execute the following command:
```
python ./validation_pipeline.py
```

### [Feature 2]: crawler.py
In order to adequately validate the machine learning model after extensive training, one must not use the exact same images for validation purposes as were previously in training. Therefore, it can be very helpful to have a range of additional images at hand. To prevent the user from wasting a lot of time and effort by manually acquiring a large amount of pictures, the search and storage of a specified number of images should be fully automated. The *crawler.py* script is able to do so by automatically downloading images from the internet based on predefined keywords and storing them in a directory on the PC. For this purpose the package iCrawler is used which provides methods for several common search engines. Said search keywords may either be entered individually by the user or read from a text file when running the script. Optionally, the user can also select between Bing and Google as their search engine of choice and additionally might automatically resize all downloaded images to a desired format.

To run the *crawler*, please execute the following command:
```
python ./crawler.py -n [max. number of images] -r [no, yes] -e [bing, google] -k [optional: keyword]
```

### requirements.txt
For running this code with python == 3.9, the crucial imports are:
```
numpy==1.22.3
tensorboard==2.6.0
tensorboard-data-server==0.6.0
tensorboard-plugin-wit==1.8.1
tensorflow==2.7.0
tensorflow-estimator==2.7.0
tensorflow-hub==0.12.0
tensorflow-io-gcs-filesystem==0.23.1
icrawler==0.6.6
opencv-contrib-python==4.5.5.64
matplotlib==3.5.2

protobuf<=3.20.1
```

## Report
The corresponding report to this SW contribution can be found in *report.pdf*.
It shall outline the motivation for implementing each feature and elaborate on the possible challenges with training and validating deep learning data including specific problems that occured during the implementation of the features at hand. Furthermore, the selected solution methods to cope with described issues shall be presented and explained by means of suitable examples and experiments. For used references as refered to in the report, additional material and code examples please see *literature.bib*.

### Contact
ludes.hanna-it19@it.dhbw-ravensburg.de

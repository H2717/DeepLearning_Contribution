# This python file and associated functionalities have been developed by Sarah Theuerkauf!
# Therefore, the following implementation must not be considered as part of my software contribution and is only included since "class_accuracy" resorts to "mapping".

#///////////// Imports
import numpy as np
import tensorflow as tf
import csv
import matplotlib.pyplot as plt
import os

#///////////// Variables
first_run = True

#///////////// Lists
class_names = [None] * 43        # List of all classnames
priority1 = [None] * 1           # STOP (highest priority)
priority2 = [None] * 13          # Speed and prohibitory signs
priority3 = [None] * 24          # Right of way and warning signs
priority4 = [None] * 5           # end-of-restriction signs
class_cnt = [0] * 43             # Number of images per Class
val_per_class = [0] * 43

#Loading classname database
with open('signnames.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    counter = 0
    for row in csv_reader:
        class_names[counter] = row[0]
        counter = counter+1

def mapping(ground_truth, prediction):
    sign_name = [None] * len(ground_truth)
    prdct_sign_name = [None] * len(prediction)
    global first_run

    for i in range(0, len(ground_truth)):
        for p in range(0, len(class_names)):                    #searching predicted sign
            if prediction[i] == p:
                prdct_sign_name[i] = class_names[p]
                break

        for g in range(0, len(class_names)):                    # searching groundtruth sign
            if ground_truth[i] == g:
                sign_name[i] = class_names[g]
                if first_run:                                   # only counting on first run
                    class_cnt[g] = class_cnt[g] + 1             # otherwise count multiplies by amount of runs
                break
    first_run = False

    return prdct_sign_name, sign_name, class_cnt


def priority_sorting():
    n = 0
    m = 0
    p = 0
    q = 0
    for i in range(len(class_names)):
        if not "Aufhebung" in class_names[i]:                   # 'Aufhebung' in combo with km/h would cause trouble
            if "STOP" in class_names[i]:                        # STOP sign
                priority1[n] = class_names[i]
                n = n+1
            elif "km/h" in class_names[i]:                      # speed signs
                priority2[m] = class_names[i]
                m = m+1
            elif "verbot" in class_names[i]:                    # prohibitory signs
                priority2[m] = class_names[i]
                m = m+1
            elif "Gebot" in class_names[i]:                     # mandatory signs
                priority3[p] = class_names[i]
                p = p+1
            elif "Vorsicht" in class_names[i]:                  # warning signs
                priority3[p] = class_names[i]
                p = p+1
            elif "Vorfahrt" in class_names[i]:                  # right-of-way signs
                priority3[p] = class_names[i]
                p = p+1
            else:
                priority4[q] = class_names[i]                   # other signs
                q = q + 1
        else:
            priority4[q] = class_names[i]                       # end-of-restriction signs
            q = q + 1

    return priority1, priority2, priority3, priority4


def priority_accuracy(ground_truth, prediction):
    priority_sorting()
    prdct_sign_name, sign_name, class_cnt = mapping(ground_truth, prediction)

    prio1_cnt = 0
    prio2_cnt = 0
    prio3_cnt = 0
    prio4_cnt = 0

    fls_prio1_cnt = 0
    fls_prio2_cnt = 0
    fls_prio3_cnt = 0
    fls_prio4_cnt = 0

    for i in range(0, len(ground_truth)):
        if prdct_sign_name[i] == sign_name[i]:                  # let's count all right predicitons per priority
            if sign_name[i] in priority1:
                prio1_cnt = prio1_cnt +1

            elif sign_name[i] in priority2:
                prio2_cnt = prio2_cnt + 1

            elif sign_name[i] in priority3:
                prio3_cnt = prio3_cnt + 1

            elif sign_name[i] in priority4:
                prio4_cnt = prio4_cnt + 1

        else:                                                   # everything falsely predicted per priority
            if sign_name[i] in priority1:
                fls_prio1_cnt = fls_prio1_cnt + 1

            elif sign_name[i] in priority2:
                fls_prio2_cnt = fls_prio2_cnt + 1

            elif sign_name[i] in priority3:
                fls_prio3_cnt = fls_prio3_cnt + 1

            elif sign_name[i] in priority4:
                fls_prio4_cnt = fls_prio4_cnt + 1
    # priority classes can be empty depending on validation batch and cause ZeroDivisionError
    try:
        prio1_acc = prio1_cnt / (prio1_cnt + fls_prio1_cnt)
    except ZeroDivisionError:
        prio1_acc = None                                        # Accuracy is not 0 when prio class is empty->Acc: None

    try:
        prio2_acc = prio2_cnt/(prio2_cnt+fls_prio2_cnt)
    except ZeroDivisionError:
        prio2_acc = None

    try:
        prio3_acc = prio3_cnt/(prio3_cnt+fls_prio3_cnt)
    except ZeroDivisionError:
        prio3_acc = None

    try:
        prio4_acc = prio4_cnt/(prio4_cnt+fls_prio4_cnt)
    except ZeroDivisionError:
        prio4_acc = None

    return prio1_acc, prio2_acc, prio3_acc, prio4_acc, prio1_cnt, prio2_cnt, prio3_cnt, prio4_cnt, fls_prio1_cnt, fls_prio2_cnt, fls_prio3_cnt, fls_prio4_cnt


def accuracy(ground_truth, prediction):                         # took this from validation_pipeline
    metric = tf.keras.metrics.Accuracy()
    metric.update_state(prediction, ground_truth)

    return metric.result().numpy()


def fls_predictions(ground_truth, prediction):
    fls_prdct_cnt = 0
    p = 0
    fls_prdcts = [None] * len(ground_truth)

    prdct_sign_name, sign_name, class_cnt = mapping(ground_truth, prediction)

    for i in range(0, len(ground_truth)):
        if not prediction[i] == ground_truth[i]:                # looking for all false predictions
            fls_prdct_cnt = fls_prdct_cnt + 1
            fls_prdcts[p] = ["Img No.", i + 1, "Predicted Sign: ", prdct_sign_name[i], "Actual Sign: ", sign_name[i]]
            p = p+1

    print("Predictions: ", prdct_sign_name)
    print("Ground Truth: ", sign_name)

    return fls_prdct_cnt, fls_prdcts, class_cnt


def get_log(ground_truth, prediction, NAME):

    if not os.path.exists(NAME + "_results"):                   # creating a new folder if it doesn't already exist
        os.mkdir(NAME + "_results")

    PATH = NAME + "_results"

    prio1_acc, prio2_acc, prio3_acc, prio4_acc, prio1_cnt, prio2_cnt, prio3_cnt, prio4_cnt, fls_prio1_cnt, fls_prio2_cnt, fls_prio3_cnt, fls_prio4_cnt = priority_accuracy(
        ground_truth, prediction)
    acc = accuracy(ground_truth, prediction)
    fls_prdct_cnt, fls_prdcts, class_cnt = fls_predictions(ground_truth, prediction)

    # /////////// let's start logging ///////////
    logfile = open(os.path.join(PATH, NAME + '.csv'), 'a', newline='', encoding='utf8')     # creating the csv-file
    logger_csv = csv.writer(logfile, delimiter=';')
    # Header
    logger_csv.writerow(['**********', '**********', '**********', '*************', '*******', '**********', '**********'])
    logger_csv.writerow(['**********', '**********', 'Welcome to', 'your Accuracy', 'Summary', '**********', '**********'])
    logger_csv.writerow(['**********', '**********', '**********', '*********', '****************', '**********', '**********'])
    logger_csv.writerow(['**********', '**********', 'Images', 'per', 'Class', '**********', '**********'])
    for r in range(43):
        if not class_cnt[r] == 0:
            logger_csv.writerow(["Number of", "Images", "in Class", class_names[r], ": ", class_cnt[r]])
    logger_csv.writerow(
        ['**********', '**********', '**********', '*********', '****************', '**********', '**********'])
    logger_csv.writerow(['**********', '**********', 'Accuracy', 'per', 'Priority', '**********', '**********'])
    logger_csv.writerow(["Prio 1: ", "Right: ", prio1_cnt, "False: ", fls_prio1_cnt, "Accuracy: ", prio1_acc])
    logger_csv.writerow(["Prio 2: ", "Right: ", prio2_cnt, "False: ", fls_prio2_cnt, "Accuracy: ", prio2_acc])
    logger_csv.writerow(["Prio 3: ", "Right: ", prio3_cnt, "False: ", fls_prio3_cnt, "Accuracy: ", prio3_acc])
    logger_csv.writerow(["Prio 4: ", "Right: ", prio4_cnt, "False: ", fls_prio4_cnt, "Accuracy: ", prio4_acc])
    logger_csv.writerow(
        ['**********', '**********', '**********', '*********', '****************', '**********', '**********'])
    logger_csv.writerow(['General', 'Model', 'Accuracy:', acc])
    logger_csv.writerow(
        ['**********', '**********', 'List of', 'false', 'Predictions', '**********', '**********'])
    for i in range(fls_prdct_cnt):
        img_no = fls_prdcts[i][1]
        prdct_sign_name = fls_prdcts[i][3]
        sign_name = fls_prdcts[i][5]
        logger_csv.writerow(["Img No.", img_no, "Predicted Sign: ", prdct_sign_name, " ", "Actual Sign: ", sign_name])
    logger_csv.writerow(
        ['**********', '**********', '**********', '*********', '****************', '**********', '**********'])

    # /////////// let's start plotting ///////////
    #  plotting accuracy overview
    if prio1_acc == None:   # value None can't be plotted
        prio1_acc = 0
    if prio2_acc == None:
        prio2_acc = 0
    if prio3_acc == None:
        prio3_acc = 0
    if prio4_acc == None:
        prio4_acc = 0

    names = ['Model', 'Prio 1', 'Prio 2', 'Prio 3', 'Prio 4']   # plotted bar names
    values = [acc, prio1_acc, prio2_acc, prio3_acc, prio4_acc]  # value data
    c = ['orange', 'blue', 'blue', 'blue', 'blue']              # plot color

    plt.bar(names, values, color = c)
    plt.title('Accuracy Overview')
    #plt.show()                     ---> only show for debugging -> saved img will be empty if plot was shown before
    plt.savefig(os.path.join(PATH, NAME + '_overview' + '.png'))


    # plotting accuracy and right and false predictions per priority
    names = ['Images', 'Right', 'False']
    val1 = [prio1_cnt+fls_prio1_cnt, prio1_cnt, fls_prio1_cnt]
    val2 = [prio2_cnt+fls_prio2_cnt, prio2_cnt, fls_prio2_cnt]
    val3 = [prio3_cnt+fls_prio3_cnt, prio3_cnt, fls_prio3_cnt]
    val4 = [prio4_cnt+fls_prio4_cnt, prio4_cnt, fls_prio4_cnt]

    fig = plt.figure(figsize=[7, 7.5])
    ax1 = fig.add_subplot(221)
    plt.bar(names, val1)
    ax2 = fig.add_subplot(222)
    plt.bar(names, val2)
    ax3 = fig.add_subplot(223)
    plt.bar(names, val3)
    ax4 = fig.add_subplot(224)
    plt.bar(names, val4)
    ax1.title.set_text('Prio 1')
    ax2.title.set_text('Prio 2')
    ax3.title.set_text('Prio 3')
    ax4.title.set_text('Prio 4')
    plt.suptitle('Result per Priority')
    #plt.show()                     ---> only show for debugging -> saved img will be empty if plot was shown before
    plt.savefig(os.path.join(PATH, NAME + '_result_per_prio' + '.png'))


    # plotting img count per class
    names = [None] * 3
    names_cl = [0] * 43
    for x in range(len(class_names)):
        val_per_class[x] = class_cnt[x]
        names_cl[x] = str(x)

    fig = plt.figure(figsize=[7, 7.5])
    ax1 = fig.add_subplot(221)
    plt.bar(names_cl[0:9], val_per_class[0:9])
    ax2 = fig.add_subplot(222)
    plt.bar(names_cl[10:20], val_per_class[10:20])
    ax3 = fig.add_subplot(223)
    plt.bar(names_cl[21:30], val_per_class[21:30])
    ax4 = fig.add_subplot(224)
    plt.bar(names_cl[31:42], val_per_class[31:42])
    ax1.title.set_text('Class 0-9')
    ax2.title.set_text('Class 10-20')
    ax3.title.set_text('Class 21-30')
    ax4.title.set_text('Class 31-42')
    plt.suptitle('Amount of Images per Class')
    #plt.show()                     ---> only show for debugging -> saved img will be empty if plot was shown before
    plt.savefig(os.path.join(PATH, NAME + '_img_amount_per_class' + '.png'))

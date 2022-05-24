import accuracy_log as log  # employ SW contribution by Sarah Theuerkauf


def class_accuracy(ground_truth, prediction):
    # use mapping feature as defined in Sarah Theuerkauf's SW contribution to get sign names and class count
    pred_sign_name, sign_name, class_cnt = log.mapping(ground_truth, prediction)
    # create internal counter that will be incremented with each correct prediction
    # (--> therefore max. as long as total amount of classes in used safetyBatch)
    internal_cnt = [0] * len(class_cnt)

    # pass through ground truth and class counts to compare validation results for each class
    for n in range(0, len(ground_truth)):       # n: variable representing numbering of inluded test_labels and thererfore quasi number of incl. images
        for p in range(0, len(class_cnt)):          # p: schau mir bild n an, laufe alle klassen durch und suche klasse p
            # increment internal counter in case prediction has been correct (dann sag ich noch, was ich richtig predicted hab mit P als Klassenummer)
            if prediction[n] == ground_truth[n] == p:
                internal_cnt[p] = internal_cnt[p]+1

    # pass through all classes in safetyBatch to calculate their individual accuracy
    # (--> c: variable representing the numbering of a particular class in used safetyBatch)
    for c in range(len(class_cnt)):
        # calculate accuracy of each class (--> divide correct predictions by total amount of classes)
        internal_acc = internal_cnt[c] / class_cnt[c]
        print(f"class accuracy of class no.{c}:", internal_acc)

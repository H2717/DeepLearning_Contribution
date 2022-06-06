# for-loop variables:
    # n: numbering of included test labels (indicates particular number of image)
    # p: expected class number in class count
    # c: particular number of a class in safetyBatch

import accuracy_log as log  # employ SW contribution by Sarah Theuerkauf


def class_accuracy(ground_truth, prediction):
    # use mapping feature to get sign names and class count
    # create internal counter to be incremented with each correct prediction
    pred_sign_name, sign_name, class_cnt = log.mapping(ground_truth, prediction)
    internal_cnt = [0] * len(class_cnt)

    # compare validation results for each class
    # increment when prediction has been correct and also fits expected class number
    for n in range(0, len(ground_truth)):
        for p in range(0, len(class_cnt)):
            if prediction[n] == ground_truth[n] == p:
                internal_cnt[p] = internal_cnt[p]+1

    # pass through all classes in safetyBatch to calculate their individual accuracy
    # --> divide correct predictions by total amount of classes
    for c in range(len(class_cnt)):
        internal_acc = internal_cnt[c] / class_cnt[c]
        print(f"class accuracy of class no.{c}:", internal_acc)

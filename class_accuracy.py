import accuracy_log as log  # employ SW contribution by Sarah Theuerkauf


def class_accuracy(ground_truth, prediction):
    # use mapping feature as defined in Sarah Theuerkauf's SW contribution to get sign names and class count
    pred_sign_name, sign_name, class_cnt = log.mapping(ground_truth, prediction)
    # create internal counter that will be incremented with each correct prediction
    # (--> therefore max. as long as total amount of classes in used safetyBatch)
    internal_cnt = [0] * len(class_cnt)

    # pass through ground truth and class count to compare validation results for each class
    # n: variable representing the numbering of included test labels (--> indicates particular number of image)
    # p: variable representing expected class number in class count
    for n in range(0, len(ground_truth)):
        for p in range(0, len(class_cnt)):
            # increment internal counter in case prediction has been correct and also fits expected class number
            if prediction[n] == ground_truth[n] == p:
                internal_cnt[p] = internal_cnt[p]+1

    # pass through all classes in safetyBatch to calculate their individual accuracy
    # c: variable representing the particular number of a class in used safetyBatch
    for c in range(len(class_cnt)):
        # calculate accuracy of each class (--> divide correct predictions by total amount of classes)
        internal_acc = internal_cnt[c] / class_cnt[c]
        print(f"class accuracy of class no.{c}:", internal_acc)

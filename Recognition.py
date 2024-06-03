


from numpy import *
import operator
import time
from os import listdir
import os
import pickle  # 导入 pickle 模块用于数据的读写
import pretreatment


def classify(input_point, data_set, labels, k):
    data_set_size = data_set.shape[0]

    diff_mat = tile(input_point, (data_set_size, 1)) - data_set

    sq_diff_mat = diff_mat ** 2
    sq_distances = sq_diff_mat.sum(axis=1)
    distances = sq_distances ** 0.5
    sorted_dist_indices = distances.argsort()
    class_count = {}
    for i in range(k):
        vote_label = labels[sorted_dist_indices[i]]
        class_count[vote_label] = class_count.get(vote_label, 0) + 1

    sorted_class_count = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True) 
    return sorted_class_count[0][0]


def img_to_vector(filename):
    return_vect = zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        line_str = fr.readline()
        for j in range(32):
            return_vect[0, 32 * i + j] = int(line_str[j])
    return return_vect


def class_number_cut(file_name):
    file_str = file_name.split('.')[0]
    class_num_str = int(file_str.split('_')[0])
    return class_num_str


def save_training_data_set(train_path):
    hw_labels = []
    training_file_list = listdir(train_path)
    m = len(training_file_list)
    training_mat = zeros((m, 1024))

    for i in range(m):
        file_name_str = training_file_list[i]
        hw_labels.append(class_number_cut(file_name_str))
        training_mat[i, :] = img_to_vector(train_path + '/%s' % file_name_str)

    # 使用 pickle 模块保存训练集数据
    with open('training_data_set.pkl', 'wb') as f:
        pickle.dump((hw_labels, training_mat), f)


def load_training_data_set():
    # 使用 pickle 模块加载训练集数据
    with open('training_data_set.pkl', 'rb') as f:
        hw_labels, training_mat = pickle.load(f)
    return hw_labels, training_mat


def handwriting_test(test_path):
    result = []

    # 首先尝试加载训练集数据，如果文件不存在，则重新构建训练集并保存到文件
    try:
        hw_labels, training_mat = load_training_data_set()
    except FileNotFoundError:
        print("请先构建训练集")
        return

    test_file_list = listdir(test_path)
    error_count = 0.0
    m_test = len(test_file_list)
    t1 = time.time()

    for i in range(m_test):
        file_name_str = test_file_list[i]
        class_num_str = class_number_cut(file_name_str)
        vector_under_test = img_to_vector(test_path + '/%s' % file_name_str)

        classifier_result = classify(vector_under_test, training_mat, hw_labels, 5)

        print("识别数字为: %d, 正确答案为: %d" % (classifier_result, class_num_str))

        if classifier_result != class_num_str:
            error_count += 1.0

    print("\n测试总数: %d" % m_test)
    print("错误总数: %d" % error_count)
    print("错误率: %f" % (error_count / float(m_test)))
    t2 = time.time()
    print("耗费时间: %.2fmin, %.4fs." % ((t2 - t1) // 60, (t2 - t1) % 60))

    result.append(m_test)
    result.append(error_count)
    result.append(error_count / float(m_test))

    return result


def classify_single_file(filename):
    try:
        hw_labels, training_mat = load_training_data_set()
    except FileNotFoundError:
        print("请先构建训练集")
        return

    pretreatment.pretreatment_image(filename, "temp_result.txt")

    vector_under_test = img_to_vector("temp_result.txt")
    classifier_result = classify(vector_under_test, training_mat, hw_labels, 5)
    print("识别数字为: %d" % classifier_result)

    os.remove("temp_result.txt")

    return classifier_result




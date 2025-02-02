#!/usr/bin/python3
# 2019.8.12
# Author Zhang Yihao @NUS

import scipy.sparse as sp
import numpy as np


class Dataset(object):
    def __init__(self, path, k):
        self.trainMatrix = self.load_rating_file_as_matrix(path + ".rmse.train.txt")
        self.user_review_fea = self.load_review_feature(path + "." + str(k) + ".user.txt")
        self.item_review_fea = self.load_review_feature(path + "." + str(k) + ".item.txt")
        self.testRatings = self.load_rating_file_as_matrix(path + ".rmse.test.txt")
        self.num_users, self.num_items = self.trainMatrix.shape

    def load_rating_file_as_matrix(self, filename):
        # Read .rating file and Return dok matrix.
        # The first line of .rating file is: num_users\t num_items
        # Get number of users and items
        num_users, num_items = 0, 0
        with open(filename, "r") as f:
            line = f.readline()
            while line is not None and line != "":
                arr = line.split("\t")
                u, i = int(arr[0]), int(arr[1])
                num_users = max(num_users, u)
                num_items = max(num_items, i)
                line = f.readline()
        # Construct matrix
        mat = sp.dok_matrix((num_users + 1, num_items + 1), dtype=np.float32)
        with open(filename, "r") as f:
            line = f.readline()
            while line is not None and line != "":
                arr = line.split("\t")
                user, item, rating = int(arr[0]), int(arr[1]), float(arr[2])
                if rating > 0:
                    mat[user, item] = rating
                line = f.readline()
        return mat

    def load_review_feature(self, filename):
        dict = {}
        with open(filename, "r") as f:
            line = f.readline()
            while line is not None and line != "":
                fea = line.replace("  ", " ").split(" ")
                index = int(fea[0])
                if index not in dict:
                    dict[index] = fea[1:]
                line = f.readline()
        return dict

    # 此函数没有用到
    def load_rating_file_as_list(self, filename):
        ratingList = []
        with open(filename, "r") as f:
            line = f.readline()
            while line is not None and line != "":
                arr = line.split("\t")
                user, item, rating = int(arr[0]), int(arr[1]), float(arr[2])
                ratingList.append([user, item, rating])
                line = f.readline()
        return ratingList

    # 此函数没有用到
    def load_negative_file(self, filename):
        negativeList = []
        with open(filename, "r") as f:
            line = f.readline()
            while line != None and line != "":
                arr = line.split("\t")
                negatives = []
                for x in arr[1:]:
                    negatives.append(int(x))
                negativeList.append(negatives)
                line = f.readline()
        return negativeList

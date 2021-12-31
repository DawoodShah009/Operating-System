from math import log10
from typing import Sized
from matplotlib import pyplot as plt
import numpy as np
import matplotlib
from numpy.lib.type_check import image
from matplotlib.patches import Rectangle
import cv2
import random
# import sys
# sys.setrecursionlimit(10000)

large_image = cv2.imread("large pic.jpg",0)
# small_image1 = cv2.imread("small pic.jpg",0)
small_image = cv2.imread("small pic.jpg",0)


def func_for_bit_count(size):
    no_of_bits = 0
    while size != 1 :
        size = size//2
        no_of_bits = no_of_bits + 1
    return no_of_bits


#           reading images
size_of_large_pic = large_image.shape
size_of_small_pic = small_image.shape

#           finding number of rows and columns of both images
no_of_rows_s = size_of_small_pic[0]
no_of_columns_s = size_of_small_pic[1]



no_of_rows_l = size_of_large_pic[0]
no_of_columns_l = size_of_large_pic[1]

#calculating large image  bits for x and y values;
row_bits = func_for_bit_count(no_of_rows_l)
column_bits = func_for_bit_count(no_of_columns_l)

best_fit_individual = []
best_fit_score = []
mean_fit_of_all_time = []
best_fit_dict = {}
population_size = 100
# global fit_co
# fit_point = 0
# fit_co = 0
#===================================================================================================================
def Population_Initialization():

    #no_of_rows_l = number of rows in the large image(height of large image)
    #no_of_columns_l = number of columns in the large image(width of large image)
    #population_size was set to hundred
    population = [(random.randrange(0, no_of_rows_l), 
                  random.randrange(0, no_of_columns_l))for i in range(population_size)]
    #returning population of randomly generated 100 individuals
    return population



def correlation_coefficient(T1, T2): 
    numerator = np.mean((T1 - np.mean(T1)) * (T2 - np.mean(T2)))
    denominator = np.std(T1) * np.std(T2)
    if denominator == 0:
        return 0
    else:
        result = numerator / denominator
        return result


# def Fitness_score(population):

    
#     large_image = cv2.imread("large pic.jpg",0)
#     small_image = cv2.imread("small pic.jpg",0)
#     threshold = 0.05
#     no_of_rows_l = size_of_large_pic[0]
#     no_of_columns_l = size_of_large_pic[1]
#     dict = {}

#     for point in population:
#         count = 0
#         row_value, column_value = point


#         for r in range(no_of_rows_s):
 
    #         for c in range(no_of_columns_s):

    #             if (column_value + c) < no_of_columns_l and (row_value + r) < no_of_rows_l :

    #                 if small_image[r,c] == large_image[(row_value + r),(column_value + c)]:

    #                     count +=1


    #     correlation = count/(no_of_rows_s*no_of_columns_s)

    #     dict[point] = correlation

    #     if correlation > threshold:
    #         print("The best point that has been discovered  is",point, dict[point])
    #         display(point)
    #         return False
    # sort_fit = sorted(dict, key=dict.get, reverse=True)
    # point = sort_fit[0]
    # best_fit_individual[point] = dict[point]
    # return dict








def Fitness_score(population, fit_co, fit_point):
    #large_image = reading the main image
    large_image = cv2.imread("large pic.jpg",0)

    #small_image = reading the template image
    small_image = cv2.imread("small pic.jpg",0)

    threshold = 0.85
    #no_of_rows_l = height of the main image
    no_of_rows_l = size_of_large_pic[0]

    #no_of_columns_l = width of the main image
    no_of_columns_l = size_of_large_pic[1]


    #populationList = keeping individuals
    populationList = []

    #scoreList = keeping fitness score against each individual in the generation
    global scoreList
    scoreList = []
    matrix_of_large_image = [[0 for i in range(29)] for j in range(35)]

    for point in population:
        row_value, column_value = point

        for r in range(no_of_rows_s): #no_of_rows_s = height of template image
            for c in range(no_of_columns_s): #no_of_columns_s = width of small image

                if (column_value + c) < no_of_columns_l and (row_value + r) < no_of_rows_l : #checking if any individual is near the 
                    #boundary of the main image

                    matrix_of_large_image[r][c] = large_image[row_value+r][column_value+c]

        # correlation_coefficient= a sub function for calculating fitness score
        correlation = correlation_coefficient(matrix_of_large_image, small_image)

        scoreList.append(correlation)
        populationList.append(point)

        if correlation > threshold: # checking if desired point(individual) is found
            point = populationList[len(populationList)-1]

            #best_fit_individual = is a list keeping best individual of each generation 
            best_fit_individual.append(point) 

            #best_fit_score = is a list keeping best fitness score of individual in each generation 
            best_fit_score.append(correlation) 


            #mean_fit_of_all_time = is a list keeping mean fitness score of each generation 
            mean_fit_value = np.mean(scoreList)
            mean_fit_of_all_time.append(mean_fit_value)
            print("The best point that has been discovered  is",point, correlation)

            # display = is a function drawing a rectangle against the individual in the main image
            display(point)
            return False


    scoreList.sort(reverse=True)
    populationList = Sorting(populationList)
    best_fit_score.append(fit_co)
    best_fit_individual.append(fit_point)
    mean_fit_value = np.mean(scoreList)
    mean_fit_of_all_time.append(mean_fit_value)

    return populationList



def Sorting(populationList):
    zipped_lists = zip(scoreList, populationList) 
    sorted_zipped_lists = sorted(zipped_lists)
    Sorted_Population = [element for _, element in sorted_zipped_lists]
    # Sorted_Population[len(Sorted_Population)-1] = fit_point
    return Sorted_Population





def bi_to_dec(ans):
    num = 0
    value_of_bit = 0
    for i in range(len(ans)) [::-1]:
        num = 2**value_of_bit * int(ans[i]) + num
        value_of_bit+=1
    return num

def func_for_merge(p1,p2,population_list):

    cross_over_point = random.randint(4,(len(p1)-4))
    crossed_parent1 = p1[0:cross_over_point] + p2[cross_over_point:len(p2)]
    crossed_parent2 = p2[0:cross_over_point] + p1[cross_over_point: len(p1)]

    num1 = bi_to_dec(crossed_parent1[0:9])
    num2 = bi_to_dec(crossed_parent1[9:len(crossed_parent1)])
    num3 = bi_to_dec(crossed_parent2[0:9])
    num4 = bi_to_dec(crossed_parent2[9:len(crossed_parent2)])

    off_spring1 = (num1, num2)
    off_spring2 = (num3, num4)

    population_list.append(off_spring1)
    population_list.append(off_spring2)


    


    # p1_first = p1[0]
    # p2_first = p2[0]

    # p1_last = p1[6]
    # p2_last = p2[6]

    # for i in range(7,len(p1)):
    #     p1_last = p1_last + p1[i]
    #     p2_last =  p2_last + p2[i] 

    # for i in range(1,6):
    #     p1_first = p1_first + p1[i] 
    #     p2_first =  p2_first + p2[i] 

    # p1 = p1_first + p2_last
    # p2 = p2_first + p1_last



    # off_spring1_of_parent1 = p1[0]
    # off_spring2_of_parent1 = p1[9]

    # off_spring1_of_parent2 = p2[0]
    # off_spring2_of_parent2 = p2[9]

    # # for i in range(1,10):
    # for i in range(1,9):
        
    #     off_spring1_of_parent1 = off_spring1_of_parent1 + p1[i]
    #     off_spring1_of_parent2= off_spring1_of_parent2 + p2[i]

    # for i in range(10,len(p1)):
    #     off_spring2_of_parent1 = off_spring2_of_parent1 + p1[i]
    #     off_spring2_of_parent2 = off_spring2_of_parent2 + p2[i]
    
    # poin1 = (off_spring1_of_parent1,off_spring2_of_parent1)
    # poin2 = (off_spring1_of_parent2, off_spring2_of_parent2)
    # num1 = bi_to_dec(off_spring1_of_parent1)
    # num2 = bi_to_dec(off_spring2_of_parent1)
    # poin1 = (num1,num2)

    # num3 = bi_to_dec(off_spring1_of_parent2)
    # num4 = bi_to_dec(off_spring2_of_parent2)
    # poin2 = (num3, num4)

    # population_list.append(poin1)
    # population_list.append(poin2)
    return population_list

def convert_to_binary(value, check):
    list_of_bits = []
    if check == 0:
        size = row_bits
    else:
        size = column_bits

    for i in range(size):
        m = str((value%2))
        list_of_bits.append(m)
        value = value//2

    num = list_of_bits[len(list_of_bits)-1]

    for i in range(len(list_of_bits)-1)[::-1]:
        num = num + list_of_bits[i]
    return num

def cross_over(dict):

    Population = []

    for i in range(0,(len(dict)-1),2):

        p1,p2 = dict[i]

        p3,p4 = dict[i+1]
        #convert_to_binary = helper function for converting decimal numbers to binary numbers.
        row_val1 = convert_to_binary(p1,0)
        col_val1 = convert_to_binary(p2,1)
        parent1 = row_val1 + col_val1

        row_val2 = convert_to_binary(p3,0)
        col_val2 = convert_to_binary(p4,1)
        parent2 = row_val2 + col_val2

        #func_for_merge = sub function for helping in cross over
        Population = func_for_merge(parent1, parent2,Population)

    return Population

def stop_func(count, generation, first_max_fit_score, Population):
    if count <= 500:
        # value_list = list(Population.values())
        if first_max_fit_score == max(scoreList):
            count +=1
            first_max_fit_score = first_max_fit_score
        else:
            first_max_fit_score = max(scoreList)
            count = 0

    if count > 500:
        max_score = max(scoreList)
        Population = Sorting(Population)
        # sorted_population = sorted(Population, key=Population.get, reverse=True)
        # point = sorted_population[0]

        print("The best fit individual repeating for", count ,"generation is:",Population[0], max_score)
        display(Population[0])
        return False

    if generation <= 10000:
        generation +=1
    else:

        # sorted_population = sorted(Population, key=Population.get, reverse=True)
        # point = sorted_population[0]
        # sorted_population = sorted(best_fit_individual, key=best_fit_individual.get, reverse=True)
        # point = sorted_population[0]
        max_score = max(scoreList)
        Population = Sorting(Population)
        # sorted_population = sorted(Population, key=Population.get, reverse=True)
        # point = sorted_population[0]

        # print("The best fit individual repeating for", count ,"generation is:",Population[0], max_score)
        # mean_fit_of_all_time.append()
        print("The best fit  individual after",generation-1," generation is", Population[0], max_score)
        display(Population[0])
        return False

    return count, generation

def mutation(population):

    Index_list = [random.randrange(1, 99) for i in range(2)] # generating 2 random indexes for mutating those individuals
    for i in Index_list: 
        num1, num2 = population[i]
        num1 = convert_to_binary(num1,0)
        num2 = convert_to_binary(num2,1)

        tuple1 = (num1, num2)

        #bit_index_row = index for switching bit of row value
        bit_index_row = random.randint(0,8)

        #bit_index_column = index for switching bit of column value
        bit_index_column = random.randint(0,9)

        num1 = tuple1[0]
        num2 = tuple1[1]
       
        l1 = list(num1)
        l2 = list(num2)

        #switching bits here(single bit switching)
        if l1[bit_index_row] == "0":
            l1[bit_index_row] = "1"
        else:
            l1[bit_index_row] = "0"

        if l2[bit_index_column] == "0":
                l2[bit_index_column] = "1"
        else:
                l2[bit_index_column] = "0"
        
        num1 = "".join(l1)
        num2 = "".join(l2)

        num1 = bi_to_dec(num1)
        num2 = bi_to_dec(num2)
        new_individual = (num1,num2)
        population[i] = new_individual

    return population

def display(point):
    window_name = 'Image'

    w = point[1]
    h = point[0]

    start_point = (w, h)
    end_point = (w+no_of_columns_s, h+no_of_rows_s)
    color = (255, 0, 0)
    thickness = 1
    image = cv2.rectangle(large_image, start_point, end_point,color, thickness)

    cv2.imshow(window_name, image) 
    cv2.waitKey(0) 

#=================================================================================================
def start():
    # global fit_co
    # global fit_point
    fit_point = 0
    fit_co = -1
    Population = Population_Initialization()
    Population,a,b = Fitness_score(Population, fit_co, fit_point)
    # print(Population)

    if Population == False:
        StopIteration
    else:

        # value_list = list(Population.values())
        first_max_fit_score = max(scoreList)

        max_fit_count = 1
        max_generation = 1

        while stop_func(max_fit_count, max_generation, first_max_fit_score,Population) != False:

            max_fit_count,max_generation =  stop_func(max_fit_count, max_generation, first_max_fit_score,Population)
            Population = Sorting(Population)
            Population = cross_over(Population,b)
            # print(Population)
            Population = mutation(Population)
            # print(Population)
            Population, a, b = Fitness_score(Population, a, b)
            # print(Population)
            if Population == False:
                break



start()
# print(mean_fit_of_all_time)
# plt.plot(mean_fit_of_all_time)

# list1= best_fit_individual.values
# new_list = list1
# best_fit_score.sort()

# mean_fit_of_all_time.sort()


plt.plot( mean_fit_of_all_time,label = "mean", )
plt.plot(best_fit_score, label = "best fit")

plt.legend()
plt.show()


# plt.plot(best_fit_score)

# plt.plot(best_fit_score)
# list1 = []
# plt.title("Testing")
# plt.xlabel("fitness")
# plt.ylabel("value")
# plt.show()


#==================================================================================================









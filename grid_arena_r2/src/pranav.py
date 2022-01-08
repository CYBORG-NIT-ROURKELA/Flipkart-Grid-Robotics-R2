# def check_if_two_digit(num):
#     return len(str(num)) == 2

# def check_validity(num1, num2, num3, num4, num5):
#     c = num1 * num2
#     if check_if_two_digit(c):
#         if c == num3:
#             d = c + num4
#             if check_if_two_digit(d):
#                 return d == num5
#             else:
#                 return False
#         else:
#             return False
#     else:
#         return False

# def check_all_num_used(num1, num2, num3, num4, num5):
#     allowed_nums = [str(x) for x in range(1,10)]
#     return sorted(str(num1) + str(num2) + str(num3) + str(num4) + str(num5)) == allowed_nums


# possible_num1 = [x for x in range(10, 101)]
# possible_num2 = [x for x in range(10, 101)]
# possible_num3 = [x for x in range(10, 101)]
# possible_num4 = [x for x in range(10, 101)]
# possible_num5 = [x for x in range(10, 101)]

# for i in range(len(possible_num1)):
#     for j in range(len(possible_num2)):
#         for k in range(len(possible_num3)):
#             for l in range(len(possible_num4)):
#                 for m in range(len(possible_num5)):
#                     num1, num2, num3, num4, num5 = possible_num1[i], possible_num2[j], possible_num3[k], possible_num4[l], possible_num5[m]
#                     # if check_validity(num1, num2, num3, num4, num5):
#                     #     if check_all_num_used(num1, num2, num3, num4, num5):
#                     #         print(num1, num2, num3, num4, num5)
#                     #         exit(0)
#                     if (num2/num1) == (num3/num2) == (num4/num3) == (num5/num4)!=1:
#                         print(num1, num2, num3, num4, num5)

class ABC:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def increment_age(self):
        self.age+=5
    

adyasha = ABC('adyasha', 20)
kamaljeet = ABC('kamaljeet', 21)



print(adyasha.age)
adyasha.increment_age()
print(adyasha.age)
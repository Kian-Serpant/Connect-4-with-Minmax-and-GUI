import itertools

def nestedloop(a,b):
    combolist = []
    for thing in a:
        for value in b:
            combolist.append([thing, value])
    return combolist
# works for 2 lists

children = [1,2,3,4,5,6,7]

def childloop(depth, listtoloopthrough, allCombos = []):
    if depth == 0:
        print("Reached end of depth")
        return 0
    for firstval in children:
        allCombos.append(childloop(depth - 1, listtoloopthrough, allCombos))
        return allCombos

allcombos = []
#print(childloop(3, children, allcombos))

# chatgpt:

# Recursive function to generate combinations
def generate_combinations(elements, depth, current_combination=[]):
    if depth == 0:
        yield current_combination
        return

    for i, element in enumerate(elements):
        yield from generate_combinations(elements[i+1:], depth-1, current_combination + [element])

# Example usage
depth = 3  # Define the depth later
#combinations = list(generate_combinations(children, depth))
#print(combinations)


# CHATGPT part 2:
# List of children
children = [1, 2, 3, 4, 5, 6, 7]


# Recursive function to generate permutations
def generate_permutations(elements, depth, current_permutation=[]):
    if depth == 0:
        yield current_permutation
        return

    for i, element in enumerate(elements):
        # Remove the current element from the pool and recurse
        yield from generate_permutations(elements[:i] + elements[i + 1:], depth - 1, current_permutation + [element])


# Example usage
depth = 3  # Define the depth later
permutations = list(generate_permutations(children, depth))
#print(permutations)

#amountdone = 0
#currentamount = []
# for value in permutations:
#     if amountdone == 5:
#         print(currentamount)
#         currentamount = []
#         amountdone = 0
#     else:
#         currentamount.append(value)
#         amountdone += 1

'''
chatgpt 2:
'''
# List of children
children = [1, 2, 3, 4, 5, 6, 7]

# Recursive function to generate combinations with replacement
def generate_combinations_with_replacement(elements, depth, current_combination=[]):
    if depth == 0:
        yield current_combination
        return

    for element in elements:
        yield from generate_combinations_with_replacement(elements, depth-1, current_combination + [element])

# Example usage
depth = 3  # Define the depth later
combinations = list(generate_combinations_with_replacement(children, depth))
#print(combinations)

# amountdone = 0
# currentamount = []
# for value in combinations:
#     if amountdone == 7:
#         print(currentamount)
#         currentamount = []
#         amountdone = 0
#     else:
#         currentamount.append(value)
#         amountdone += 1

'''
ChatGPT attempt 3
'''
# List of children
children = [1, 2, 3, 4, 5, 6, 7]


# Recursive function for ordered combinations with replacement
def generate_ordered_combinations_with_replacement(elements, depth, current_combination=[]):
    if depth == 0:
        yield current_combination
        return

    for element in elements:
        yield from generate_ordered_combinations_with_replacement(elements, depth - 1, current_combination + [element]) # yield continues until the end of the function - this is cool!


# Example usage
depth = 3  # Define the depth
combinations = list(generate_ordered_combinations_with_replacement(children, depth))
# print(combinations)
# amountdone = 0
# currentamount = []
# for value in combinations:
#     if amountdone == 7:
#         print(currentamount)
#         currentamount = []
#         amountdone = 0
#     else:
#         currentamount.append(value)
#         amountdone += 1

'''
GPT attempt 4- this works! try to figure it out and adapt!
'''
# List of children
children = [1, 2, 3, 4, 5, 6, 7]


# Recursive function for ordered combinations with replacement - this works! need to figure it out
def generate_ordered_combinations_with_replacement(elements, depth, current_combination=[]):
    if depth == 0:
        yield current_combination
        return

    for element in elements:
        yield from generate_ordered_combinations_with_replacement(elements, depth - 1, current_combination + [element])


# Example usage
depth = 4  # Define the depth
combinations2 = list(generate_ordered_combinations_with_replacement(children, depth))
#print(combinations2)
# amountdone = 0
# currentamount = []
# firstcharacteramount = 0
# for value in combinations2:
#     if amountdone != 7:
#         currentamount.append(value)
#         amountdone += 1
#     if amountdone == 7:
#         print(currentamount)
#         currentamount = []
#         amountdone = 0
#     firstcharacteramount += 1
#     if firstcharacteramount == 49:
#         print("")
#         firstcharacteramount = 0

'''
my version
'''
# Recursive function for ordered combinations with replacement - this works! need to figure it out
def my_generate_ordered_combinations_with_replacement(elements, depth, current_combination=[], allcombos = None):
    if allcombos == None:
        allcombos = [] # to initialise allcombos, at the first instance the list is run through

    if depth == 0:
        return current_combination

    for element in elements:
        for value in generate_ordered_combinations_with_replacement(elements, depth - 1, current_combination + [element]):
            yield value # this works, but return doesn't for some reason D:
        #yield from generate_ordered_combinations_with_replacement(elements, depth - 1, current_combination + [element])


# Example usage
depth = 4  # Define the depth
# mycombinations = list(my_generate_ordered_combinations_with_replacement(children, depth))
# print(mycombinations)
# amountdone = 0
# currentamount = []
# firstcharacteramount = 0
# for value in mycombinations:
#     if amountdone != 7:
#         currentamount.append(value)
#         amountdone += 1
#     if amountdone == 7:
#         print(currentamount)
#         currentamount = []
#         amountdone = 0
#     firstcharacteramount += 1
#     if firstcharacteramount == 49:
#         print("")
#         firstcharacteramount = 0

'''
ChatGPT without yield
'''


# Recursive function for ordered combinations with replacement (no yield)
def generate_combinations_no_yield(elements, depth, current_combination=None, result=None):
    if result is None:
        result = []  # Initialize the result list
    if current_combination is None:
        current_combination = []  # Initialize the current combination

    if depth == 0:  # Base case: add the current combination to the results
        result.append(current_combination)
        return result

    for element in elements:
        # Recursive call with depth reduced by 1 and element added to combination
        generate_combinations_no_yield(elements, depth - 1, current_combination + [element], result)

    return result


# Example usage
children = [1, 2, 3, 4, 5, 6, 7]
depth = 4
combinations3 = generate_combinations_no_yield(children, depth)
# print(combinations3)
amountdone = 0
currentamount = []
firstcharacteramount = 0
# for value in combinations3:
#     if amountdone != 7:
#         currentamount.append(value)
#         amountdone += 1
#     if amountdone == 7:
#         print(currentamount)
#         currentamount = []
#         amountdone = 0
#     firstcharacteramount += 1
#     if firstcharacteramount == 49:
#         print("")
#         firstcharacteramount = 0



'''
my version
'''

depthcount = [0]

def mygenerate_combinations_no_yield(elements, depth, current_combination=[], result=[]): # sets current combinations and result to be empty lists if first time running through
    if depth == 0:  # Base case: add the current combination to the results, if it has reached lowest depth
        result.append(current_combination)
        depthcount[0] = depthcount[0] + 1
        return result

    for element in elements: # the elements is the list of children. this will go through for each column, and a list of values it could be/
        # Recursive call with depth reduced by 1 and element added to combination
        mygenerate_combinations_no_yield(elements, depth - 1, current_combination + [element], result)

    print("Depth is:", depth)
    print(current_combination)
    if depth != 1:
        print("don't use this value!^^^\n")
    return result


# Example usage
children = [1, 2, 3, 4, 5, 6, 7]
depth = 5
combinations4 = mygenerate_combinations_no_yield(children, depth)
# print(combinations4)
amountdone = 0
currentamount = []
firstcharacteramount = 0
combos = 0
for value in combinations4:
    combos += 1
    if amountdone != 7:
        currentamount.append(value)
        amountdone += 1
    if amountdone == 7:
        print(currentamount)
        currentamount = []
        amountdone = 0
    firstcharacteramount += 1
    if firstcharacteramount == 49:
        print("")
        firstcharacteramount = 0

if combinations4 == combinations3:
    print("Hooray, code has been shortened")
print("Depthcount:", depthcount[0], "\ndivided by 7:", (depthcount[0]/7), "\ndivided by 49:", (depthcount[0]/49), "\ndivided by 343:", (depthcount[0]/343))
print("this amount is equal to 7^4, which is:", 7**4)
print("there are:", combos, "Different combos, or the number of columns to the power of the depth - this could get outta hand REAL quick")
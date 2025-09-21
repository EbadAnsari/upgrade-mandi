from typing import List

"""
number of guests: number_of_guests
boat's weight limit: boat_weight_limit
"""

number_of_guests, boat_weight_limit = map(
    lambda value: int(value.replace(" ", "")), input().split(" ")
)

"""
weight of guests: weight_of_guests
"""

weight_of_guests = list(
    map(lambda value: int(value.replace(" ", "")), input().split(" "))
)


def solution(
    number_of_guests: int, boat_weight_limit: int, weight_of_guests: List[int]
):
    weight_of_guests.sort()
    minimumNumberOfBoatsRequired = 0
    while len(weight_of_guests) > 0:
        selected_index = []
        choosen_weight = weight_of_guests.pop()

        if choosen_weight > boat_weight_limit:
            raise "Guest weight must be less than boat weight"

        reverse_iterator = len(weight_of_guests) - 1

        for i in range(reverse_iterator, -1, -1):
            if choosen_weight + weight_of_guests[i] <= boat_weight_limit:
                selected_index.append(i)
                choosen_weight += weight_of_guests[i]

        for i in selected_index:
            weight_of_guests.pop(i)
        minimumNumberOfBoatsRequired += 1
    return minimumNumberOfBoatsRequired


print(solution(number_of_guests, boat_weight_limit, weight_of_guests))

exit(0)

# testing part
inputList = [
    [6, 100, [30, 70, 30, 60, 40, 40], 3],
    [4, 50, [20, 20, 20, 20], 2],
    [5, 60, [10, 50, 20, 40, 30], 3],
    [3, 100, [90, 80, 70], 3],
    [6, 70, [30, 40, 60, 10, 20, 50], 3],
    [2, 100, [50, 50], 1],
]

outputList = []

# print(number_of_guests, boat_weight_limit, weight_of_guests)

for inputs in inputList:
    output = solution(inputs[0], inputs[1], inputs[2])
    outputList.append(
        {"output": output, "expcted": inputs[-1], "status": output == inputs[-1]}
    )

for i in outputList:
    print(i)
# print(outputList)

""" name: Sayed Abdul Hakim    email: sayedhakim27@gmail.com when anything gets wrong email me
TRAVEL PLANNING Application Using A Star Search Algorithm
developed in PyCharm IDE

# important note should install the following two libraries first to run the code
# pip install pandas
# pip install xlrd
"""
from datetime import datetime
from math import radians, sin, cos, acos

import pandas as pd


# _______________________classes________________________
class City:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = radians(latitude)
        self.longitude = radians(longitude)


class Flight:
    def __init__(self, source, destination, departure, arrival, flight_number, days):
        self.source = source
        self.destination = destination
        self.departure = departure
        self.arrival = arrival
        self.flight_number = flight_number
        self.days = days


class Node:
    def __init__(self, parent_node, node_name, flight, cost, evaluation, has_child):
        self.parent_node = parent_node
        self.node_name = node_name
        self.flight = flight
        self.cost = cost
        self.evaluation = evaluation
        self.has_child = has_child

    def __eq__(self, other):
        if not (isinstance(other, Node)):
            # don't attempt to compare against unrelated types
            return NotImplemented
        if other is None:
            return False
        return self.parent_node == other.parent_node and self.node_name == other.node_name and self.flight == other.flight and self.cost == other.cost and self.evaluation == other.evaluation and self.has_child == other.has_child


# ________________________ helper_functions_________________________
data_file = pd.ExcelFile(r'Travel Agent KB (2 sheets).xlsx')
cities_df = pd.read_excel(data_file, 'Cities')
flights_df = pd.read_excel(data_file, 'Flights')


def load_cities_data():
    my_cities = []
    for index, row in cities_df.iterrows():
        my_cities.append(City(row['City'], row['Latitude'], row['Longitude']))
    return my_cities


def load_flights_data():
    my_flights = []
    for index, row in flights_df.iterrows():
        my_flights.append(
            Flight(row['Source'], row['Destination'], row['Departure Time'], row['Arrival Time'], row['Flight Number'],
                   convert_string_to_list(row['List of Days'])))

    return my_flights


# to convert days at the file from string to be list of days
def convert_string_to_list(days_string):
    # to ignore the braces in the string ex: from [ day,day ,day ,day ] to -> day,day day,day ,
    days_string = days_string[1:-1]
    days_list = []
    for day_ in days_string.split(","):
        # strip to remove space in the string
        days_list.append(day_.strip())
    return days_list


# to check if the needed day is within the day of the flight or not
def check_flight_days(start_day, end_day, available_flight_day_list):
    days_dict = {"sat": 1, "sun": 2, "mon": 3, "tue": 4, "wed": 5, "thu": 6, "fri": 7}
    days_dict.get(start_day)

    for available_flight_day in available_flight_day_list:
        if days_dict.get(available_flight_day) >= days_dict.get(start_day) and days_dict.get(
                available_flight_day) <= days_dict.get(end_day):
            return True
    return False


def _print_flights(flights_to_print):
    step_counter = 1
    if flights_to_print is None or len(flights_to_print) == 0:
        print(
            "----------------------------------------------------------------"
            "-------------------------------------------------------")
        return
    print("the number of flights you should take to reach your wanted city is ", len(flights_to_print))
    for single_flight in flights_to_print:
        print("| Step: ", step_counter, " use ", end="")
        step_counter += 1
        _print_single_flight(single_flight)
    print(
        "----------------------------------------------------------------"
        "-------------------------------------------------------")


def _print_single_flight(single_flight):
    if not (type(single_flight) is Flight):
        print("this is not flight object ")
        return
    print("flight ", single_flight.flight_number, " from ", single_flight.source, " to ", single_flight.destination,
          " . Departure time ", single_flight.departure, " and arrival time ",
          single_flight.arrival, ".")


def _print_node(curr_node):
    print("CITY_NAME:- \"", curr_node.node_name, "\"\tConnected_Parent_Node_Name :- \"",
          curr_node.flight.source, "\"\tTotal_Cost :\" %.2f" % curr_node.cost, "\"\tHAS_CHILD :- \"",
          curr_node.has_child, "\"")


def get_city(city_name):
    for city_ in cities:
        if city_.name.strip() == city_name.strip():
            return city_
    print(city_name, " gets None, sayed")
    return None


def get_elapsed_time(start_time, end_time):
    time_format = '%H:%M:%S'
    time_elapsed = datetime.strptime(end_time.strftime(time_format), time_format) - datetime.strptime(
        start_time.strftime(time_format), time_format)
    return time_elapsed


def calculate_distance(source, destination):
    if source is None or source == destination:
        # print("sayed source :")
        return 0

    if destination is None:
        # print("sayed destination :")
        return 0
    return 6371.01 * acos(
        sin(source.latitude) * sin(destination.latitude) + cos(source.latitude) * cos(destination.latitude) * cos(
            source.longitude - destination.longitude))


def calculate_evaluation(parent_node, current_city_name, goal):
    # f(n) = g(n) + h(n)
    if parent_node is None:
        return calculate_distance(get_city(current_city_name), get_city(goal))

    return parent_node.cost + calculate_distance(get_city(parent_node.node_name),
                                                 get_city(current_city_name)) + calculate_distance(
        get_city(current_city_name), get_city(goal))


def calculate_cost(parent_node, destination):
    return parent_node.cost + calculate_distance(get_city(parent_node.node_name), get_city(destination))


def connect(parent_node, flight, goal):
    return Node(parent_node, flight.destination, flight, calculate_cost(parent_node, flight.destination),
                calculate_evaluation(parent_node, flight.destination,
                                     goal), False)


def expand_node(new_parent_node, goal_city, start_day, end_day):
    for curr_flight in flights:
        if new_parent_node.node_name == curr_flight.source and check_flight_days(start_day, end_day, curr_flight.days):
            new_child_node = connect(new_parent_node, curr_flight, goal_city)
            if new_child_node not in expanded_list:
                expanded_list.append(new_child_node)
            else:
                print("expanded before")
                _print_node(new_child_node)
                return False
    return True


def get_best_node_to_expand(_available_to_expand_list, goal):
    if _available_to_expand_list is None or len(_available_to_expand_list) == 0:
        print("no expanded nodes to select from it")
        return None
    # at first we will assume that first node is the minimum evaluation value
    best_node = _available_to_expand_list[0]
    for node in _available_to_expand_list:
        if node.evaluation < best_node.evaluation:
            # as this node has evaluation function less than the assumed one so we will make it best node till now
            best_node = node

    if best_node.node_name == goal:
        print("---------- the goal node is :", end="")
        _print_node(best_node)

        goal_nodes_list.append(best_node)
        _print_from_source_to_goal_flights(goal_nodes_list)
        return None
    else:
        # to modify the global list of expanded node to make the expanding node has child as it wil be
        index = expanded_list.index(best_node)
        expanded_list[index].has_child = True
    return best_node


def filter_has_no_child_nodes(node_list):
    filtered_list = []
    for node in node_list:
        if not node.has_child:
            # means that this node has no child
            # so its okay to consider it in the selection step of the new expanding node
            filtered_list.append(node)
    return filtered_list


def _print_solution(source, goal, start_day, end_day):
    print("--- YOU WANT TO REACH \"", goal, " FROM \"", source, "\" within days \"", start_day, ", ", end_day, "\"")
    # here is the source node is created and now we will expand it as initial node
    node = Node(parent_node=None, node_name=source, flight=None, cost=0,
                evaluation=calculate_evaluation(None, source, goal),
                has_child=True)
    # here is the source node is created and now we will expand it as initial node
    expand_node(node, goal, start_day, end_day)

    while True:
        temp_node = get_best_node_to_expand(filter_has_no_child_nodes(expanded_list), goal)
        if temp_node is None:
            break
        expand_node(temp_node, goal, start_day, end_day)


def traverse_goal_to_parent(_goal_node):
    my_goal_flights_list = []
    while _goal_node.parent_node is not None:
        my_goal_flights_list.append(_goal_node.flight)
        _goal_node = _goal_node.parent_node
    my_goal_flights_list.reverse()
    return my_goal_flights_list


def _print_from_source_to_goal_flights(_goal_nodes_list):
    options_size = len(_goal_nodes_list)
    if options_size == 0:
        print()
        print("**************************************************************************************************")
        print(
            "----------------------------------------------------------------"
            "-------------------------------------------------------")
        print("no available flights")
        print(
            "you may want to restart program and try again with increasing or decreasing one day to get results!")
        print(
            "----------------------------------------------------------------"
            "-------------------------------------------------------")
        return
    current_option_number = 1
    print(
        "----------------------------------------------------------------"
        "-------------------------------------------------------")
    print("you have ", options_size, " options to reach your goal \"", goal_nodes_list[0].node_name,
          "\" within wanted range of days")

    for goal_node in _goal_nodes_list:
        print()
        print("------------------------ S O L U T I O N    O P T I O N: ", current_option_number,
              "------------------------")
        print("******* ", end=" ")
        _print_flights(traverse_goal_to_parent(goal_node))
        current_option_number += 1


# _______________________________global_variables______________________
cities = load_cities_data()
flights = load_flights_data()
expanded_list = []
goal_nodes_list = []
# _________________________________Main____________________________________
source_input = input("Enter Source City: ")
destination_input = input("Enter destination City: ")
# day name should be like :sat or sun or mon or tue or wed or thu or fri
start_day_input = input("Enter start day of a week : ")
end_day_input = input("Enter end day of a week   : ")

# this function to start the algorithm and print solution
_print_solution(source_input, destination_input, start_day_input, end_day_input)

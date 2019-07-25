school_coaches = {}
weeks = 1


class Coach:

    def __init__(self, times=[1, 2, 3, 4, 5], weeks=1, label=None, filename=None):
        if label: self.label = label
        if len(times) != weeks * 5:
            raise ValueError("There is not enough arrival times given for the number of weeks")
        if label and filename:
            self.arrival_times = self.get_arrival_times_from_file(filename, label)
        elif times and weeks:
            days_list = generate_list_of_days(weeks)
            self.arrival_times = {}
            for i in range(5 * weeks):
                self.arrival_times.update({days_list[i]: times[i]})

    def get_arrival_time(self, day):
        if day not in self.arrival_times.keys():
            raise ValueError("Not a valid day e.g. Mon2")
        else:
            return self.arrival_times[day]

    def set_arrival_time(self, day, time):
        if day not in self.arrival_times.keys():
            raise ValueError("Not a valid day e.g. Mon2")
        elif type(time) != int:
            raise ValueError("Not a valid time must be a number")
        elif time < -120 or time > 120:
            raise ValueError("Not a valid time: must be between -120 and 120 minutes")
        else:
            self.arrival_times[day] = time

    def get_average_arrival(self):
        return sum(self.arrival_times.values()) / len(self.arrival_times)

    def get_average_late_arrival(self):
        lates = [time for time in self.arrival_times.values()]
        return sum(lates) / len(lates)

    def get_number_of_late_arrivals(self):
        lates = [time for time in self.arrival_times.values()]
        return len(lates)

    def save_results(self, filename):
        pass

    def print_coach_arrivals(self):
        for day, arrival in self.arrival_times.items():
            print(f'{day}: {arrival}')

    def get_label(self):
        return str(self.label)


def load_menu():
    """The first menu loaded when the system starts allows them to either enter their own data
     or load a file of data"""
    menu = '''
    ## Welcome to the coach system ##

    Do you wish to load a file or enter your own data?
    1. Enter your own data
    2. Load a file
    '''
    print(menu)
    while True:
        choice = input("\t>>")
        if choice in ("1", "2"):
            break
        else:
            print("Please enter 1 or 2")

    if choice == "1":
        enter_data_manually()
    else:
        load_data()


def generate_list_of_days(weeks):
    days = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri')
    days_list = []
    for i in range(0, 5 * weeks):
        days_list.append(days[i % 5] + str(i // 5 + 1))
    days_list = tuple(days_list)
    return days_list


def input_arrival_times(label):
    global weeks
    print(f'Enter data for coach {label}')
    arrival_times = []
    for day in generate_list_of_days(weeks):
        time = int(input(f'{day}:\t'))
        arrival_times.append(time)
    return arrival_times


def enter_data_manually():
    coach_labels = ("A", "B")
    global school_coaches
    global weeks
    school_coaches = {}
    while True:
        try:
            weeks = int(input("How many weeks will you be entering?"))
            if 0 < weeks < 53:
                break
            else:
                print("You must enter a number between 1 and 52")
        except TypeError:
            print("You must enter a number between 1 and 52")

    for label in coach_labels:
        arrival_times = input_arrival_times(label)
        this_coach = Coach(arrival_times, weeks)
        school_coaches.update({label: this_coach})


def input_coach_label():
    global school_coaches
    labels = school_coaches.keys()
    print("The following coaches are currently loaded:", end="")
    print(",".join(labels))
    while True:
        label = input("Type name of the coach you wish to update an arrival time for")
        if label in labels:
            break
        else:
            print("The coach you selected was not in the list")

    return label


def input_day():
    global weeks
    while True:
        day = input("Enter the day you wish examine:")
        if len(day) != 4:
            print("The day you are looking for must be in the format of Mon3 or Fri2")
        elif not day[3].isdigit():
            print("The 4th character must be an integer eg Mon(4)")
        elif day[:3] not in ["Mon", "Tue", "Wed", "Thu", "Fri"]:
            print("The day must be a three letter day eg Mon/Tue etc")
        elif int(day[3]) < 1 or int(day[3]) > weeks:
            print("The week number must within the number of weeks you set when you entered or uploaded the data")
        else:
            break
    return day


def input_arrival_time():
    print("Enter the number of minutes late / early the bus arrived:")
    print("A minus number reflects the bus has arrived late")
    while True:
        try:
            time = int(input(">>"))
            if -120 < time < 120:
                break
            else:
                print("You must enter a number between -120 and 120")
        except TypeError:
            print("You must enter a whole number / integer")
    return time


def update_arrival_time():
    global school_coaches
    label = input_coach_label()
    choice_day = input_day()
    time = input_arrival_time()
    try:
        school_coaches[label].set_arrival_time(choice_day, time)
    except ValueError:
        print("The value you entered for the day or time was not in the correct format")
    finally:
        print("Coach", label, "'s arrival time on", choice_day, "was updated to ",
              school_coaches[label].get_arrival_time(choice_day))


def print_coach_arrival_times():
    global school_coaches
    label = input_coach_label()
    school_coaches[label].print_coach_arrivals()


def add_new_bus():
    print("Type in a new label for the coach that you wish to add")
    global school_coaches
    global weeks
    labels = school_coaches.keys()
    print("The following coaches are currently loaded:", end="")
    print(",".join(labels))
    while True:
        label = input(">>")
        if label not in labels:
            break
        else:
            print("Label already in use.")
    times = input_arrival_times(label)
    this_coach = Coach(times=times, weeks=weeks)
    school_coaches.update({label: this_coach})


def save_data():
    global school_coaches
    filename = input("Type the name of the that you wish to create / save to:")
    import pickle
    with open(filename, 'ab') as f:
        pickle.dump(school_coaches, f)


def load_data():
    global school_coaches
    filename = input("Type the name of the that you wish to load:")
    import pickle
    with open(filename, 'rb') as f:
        school_coaches = pickle.load(f)


def edit_data_menu():
    global school_coaches
    """Prints the menu that allows users to manipulate the data stored about the
    bus arrival times"""

    menu = """
        Please select an option:
        1. Change an arrival time
        2. Save the current data to a file
        3. Print out data on a specific coach
        4. Load data from a file
        5. Enter data on a new bus
        6. Main Menu
        """
    while True:
        print(menu)
        choice = input("\t>>")
        if choice == "6":
            break
        elif choice == "1":
            update_arrival_time()
        elif choice == "2":
            save_data()
        elif choice == "3":
            print_coach_arrival_times()
        elif choice == "4":
            pass
        elif choice == "5":
            add_new_bus()
        else:
            print("\tPlease enter a value for 1 to 4")


def view_bus_statistics():
    """This function prints the console interface that allows the user to view the statistics for the
    coaches that are currently loaded into the system"""
    global school_coaches

    print("Coach\t", "Lates\t", "Average Arrival Time\t", "Average_Late_Time\t")
    for label, coach in school_coaches.items():
        print(label, end="\t     ")
        print(coach.get_number_of_late_arrivals(), end="\t" * 2 + " ")
        print(coach.get_average_arrival(), end="\t" * 5 + " ")
        print(coach.get_average_late_arrival())


def view_day_statistics():
    global weeks
    global school_coaches
    """This function allows the user to type in a day as a string and the function will print out the statistics
    relating to the coach arrivals on that day"""
    day = input_day()
    late_coaches = []
    for label, coach in school_coaches.items():
        arrival = coach.get_arrival_time(day)
        if arrival < 0:
            late_coaches.append((label, arrival))
    if late_coaches:
        print("On", day, "the following coaches were late:")
        for coach in late_coaches:
            if coach[1] < -1:
                print("Coach", coach[0], ":", coach[1] * -1, "minutes late")
            else:
                print("Coach", coach[0], ":", coach[1] * -1, "minute late")
    else:
        print("There were no late coaches on this day")


def main_menu():
    """Prints the top level menu"""
    menu = """
    Please select an option:
    1. Edit Bus lates data
    2. View Bus Statistics
    3. View Day Statistics
    4. Exit Program
    """

    while True:
        print(menu)
        choice = input("\t>>")
        if choice == "4":
            print('Thank you for using the coach system')
            break
        elif choice == "1":
            edit_data_menu()
        elif choice == "2":
            view_bus_statistics()
        elif choice == "3":
            view_day_statistics()
        else:
            print("\tPlease enter a value for 1 to 4")


if __name__ == "__main__":
    load_menu()
    main_menu()

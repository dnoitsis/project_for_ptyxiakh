import csv
import math
from datetime import datetime, timedelta
from random import random, randint
import pandas as pd
import simpy as sp


class Order:
    # This class is used to define an order object with its necessary attributes.

    def __init__(self, identifier, typ, priority, quantity, ca_code, cc_code, product_code, release_date, due_date,
                 complexity):
        self._identifier = identifier
        self._typ = typ
        self._priority = priority
        self._quantity = quantity
        self._ca_code = ca_code
        self._cc_code = cc_code
        self._product_code = product_code
        self.release_date = release_date
        self._due_date = due_date
        self._complexity = complexity

    def get_identifier(self):
        return self._identifier

    def get_type(self):
        return self._typ

    def get_priority(self):
        return self._priority

    def get_quantity(self):
        return self._quantity

    def get_ca_code(self):
        return self._ca_code

    def get_cc_code(self):
        return self._cc_code

    def get_product_code(self):
        return self._product_code

    def get_releasedate(self):
        return self.release_date

    def get_duedate(self):
        return self._due_date

    def get_complexity(self):
        return self._complexity


class Loom:
    # This class defines the loom with its associated properties.

    def __init__(self, loom_id, loom_speed, performance_index):
        self.loom_id = loom_id
        self.loom_speed = loom_speed
        self.performance_index = performance_index
        self.prev_job = None
        self.current_job = None

    def set_prev_job(self, job):
        self.prev_job = job

    def set_current_job(self, job):
        self.current_job = job

    def get_loom_id(self):
        return self.loom_id

    def get_prev_job(self):
        return self.prev_job

    def get_current_job(self):
        return self.current_job

    def get_loom_speed(self):
        return self.loom_speed

    def get_performance_index(self):
        return self.performance_index

    def get_loom_original_speed(self):
        return self.loom_speed * self.performance_index


all_jobs = list()  # Defining a list to store all jobs
jobs = pd.read_excel("job_details.xlsx")  # Opening the excel file of jobs/orders
jobs.sort_values(by=["priority"], inplace=True)
for j in jobs.iterrows():  # Iterating over jobs in excel file
    job_details = j[1]  # Getting current iterated job
    id, typ, prior = job_details["identifier"], job_details["type"], job_details["priority"]
    cap, ca, cc = job_details["quantity"], job_details["ca_code"], job_details["cc_code"]
    pc, rd, dd = job_details["product_code"], job_details["release_date"], job_details["due_date"]
    complex = job_details["complexity"]

    order = Order(id, typ, prior, cap, ca, cc, pc, rd, dd, complex)  # Defining an order object with job details

    all_jobs.append(order)  # Appending the list of all jobs with order


def random_job(id):
    if int(randint(0, 1)) == 0:
        typ = 'regular'
    else:
        typ = 'sample'

    prior = randint(0, 10)
    if typ == 'sample':
        cap = randint(1, 25)
    else:
        cap = randint(25, 100000)

    ca = 'ca_' + str(randint(0, 10))
    cc = 'cc_' + str(randint(0, 10))
    pc = randint(1000, 9999)
    rd_d = randint(1, 30)
    rd_m = randint(7, 8)
    rd = datetime(2022, rd_m, rd_d)

    dd_d = randint(1, 30)
    dd_m = randint(7, 8)
    dd = datetime(2022, dd_m, dd_d)

    while rd > dd:
        dd_d = randint(1, 30)
        dd_m = randint(7, 8)
        dd = datetime(2022, dd_m, dd_d)

    complex = randint(1, 10)
    return Order('id'+str(id), typ, prior, cap, ca, cc, pc, rd, dd, complex)


def setup_time(ca1, cc1, ca2, cc2):
    # This function will calculate setup_time of loom based on ca and cc codes of fabrics.
    if ca1 == ca2 and cc1 == cc2:
        return 0
    elif ca1 == ca2 and cc1 != cc2:
        return 2
    else:
        return 8


def processing_time(job, loom):
    # This function will calculate the processing time of a job based on its complexity.
    # global loom_working_speed
    comp = job.get_complexity()
    time = job.get_quantity() * comp / loom.get_loom_original_speed()
    return time


def damaged_loom():
    # This function will return True if loom is damaged (event of simulation).
    chance = random()
    if chance > 0.99:
        print("Found a Damaged Loom!")
        return True
    return False


def broken_yarn():
    # This function checks if there is a broken yarn case (event of simulation).
    chance = random()
    if chance > 0.85:
        print("Found Broken Yarn!")
        return True
    return False


def new_job():
    # This function checks if there is a broken yarn case (event of simulation).
    chance = random()
    if chance > 0.7:
        print("New Job!")
        return True
    return False


def jobs_available(jobs, current_day):
    a_jobs = []
    for job in jobs:
        y, m, d = take_datetime_and_make_it_days_month_year(job.get_releasedate())
        s_releasedate = datetime(y, m, d)
        if s_releasedate <= current_day:
            a_jobs.append(job)

    return a_jobs


def selected_job(jobs, prev_job):
    if prev_job is None:
        return jobs[0]

    min_time = 10
    s_job = jobs[0]
    for job in jobs:
        if setup_time(job.get_ca_code(), job.get_cc_code(), prev_job.get_ca_code(), prev_job.get_cc_code()) < min_time:
            min_time = setup_time(job.get_ca_code(), job.get_cc_code(), prev_job.get_ca_code(), prev_job.get_cc_code())
            s_job = job

    return s_job, min_time


def new_jobs(jobs, s_job):
    n_jobs = []
    for job in jobs:
        if job != s_job:
            n_jobs.append(job)

    return n_jobs


def take_datetime_and_make_it_days_month_year(str_date):
    dt = str_date
    return dt.year, dt.month, dt.day


def delete_random_jobs(jobs, original_jobs_total_number):
    n_jobs = []
    for job in jobs:
        num_str = ""
        for m in job.get_identifier():
            if m.isdigit():
                num_str = num_str + m

        if int(num_str) <= original_jobs_total_number:
            n_jobs.append(job)

    return n_jobs


active_time = 0


def weaver2(environment, loom):
    global start_time, active_time, jobs, setup_cost, ending_times, jobs_total_number, all_jobs
    ending_times = dict()
    while len(jobs) > 0:
        # print("loom", loom.get_loom_speed())
        # print("all_jobs len: ",len(jobs))
        # for job in jobs:
        #     print("all_jobs: ", job.get_identifier())

        simulation_start_time = environment.now
        days, hours = simulation_start_time // 8, simulation_start_time % 8
        current_date = start_time + timedelta(days=days, hours=hours)
        a_jobs = jobs_available(jobs, current_date)

        # print("avl_jobs len: ", len(a_jobs))
        # for job in a_jobs:
        #     print("all_jobs: ", job.get_identifier())

        if len(a_jobs) > 0:
            if new_job():
                r_job = random_job(jobs_total_number)
                jobs_total_number += 1
                jobs.append(r_job)
                # for job in a_jobs:
                #     print("all_jobs: ", job.get_identifier(), job.get_priority())
                jobs.sort(key=lambda x: x._priority, reverse=False)
                # for job in a_jobs:
                #     print("all_jobs: ", job.get_identifier(), job.get_priority())
                all_jobs.append(random_job(jobs_total_number))

            if loom.get_prev_job() is None:
                s_job, setup_time = a_jobs[0], 0
            else:
                s_job, setup_time = selected_job(a_jobs, loom.get_prev_job())

            print("Started working on", s_job.get_identifier(), "at", current_date.strftime("%m/%d/%Y"), "at Loom",
                  loom.get_loom_id())  # Print when there is a free loom and a job starts

            loom.set_current_job(s_job)
            jobs = new_jobs(jobs, s_job)
            setup_cost += s_job.get_quantity() * setup_time
            yield env.timeout(setup_time)
            yield env.timeout(processing_time(s_job, loom))
            active_time += processing_time(s_job, loom)
            if damaged_loom():  # If a loom is damaged, repair it, which takes 15 minutes.
                yield env.timeout(0.25)

            if broken_yarn():  # If there is broken yarn found, repair it, which takes 15 minutes.
                yield env.timeout(0.25)

            # if new_job():
            #     jobs.append(random_job(jobs_total_number))
            #     jobs_total_number += 1

            simulation_start_time = environment.now
            days, hours = simulation_start_time // 8, simulation_start_time % 8
            ending_time = start_time + timedelta(days=days, hours=hours)
            print(s_job.get_identifier(), "ended at", ending_time.strftime("%m/%d/%Y"), "at Loom",
                  loom.get_loom_id())  # Printing the ending time of a job
            loom.set_prev_job(s_job)
            ending_times[s_job.get_identifier()] = environment.now

        yield env.timeout(1)


number_of_simulation_runs = 100
# Defing the number of simulations that will run, adjustable

with open("weaving_process_results.csv", "w") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerow(["Run", "Delayed Orders", "Unfinished Orders", "Lost Profit due to Delays", "Total Loss"])
# Creating a file to store the results of each run and write the column headers

original_jobs = all_jobs
original_jobs_total_number = len(all_jobs)
for run in range(number_of_simulation_runs):
    # Run the simulation that many times, storing the results of each run to file
    all_jobs = delete_random_jobs(all_jobs, original_jobs_total_number)
    global ending_times
    env = sp.Environment()
    start_time = datetime(2022, 7, 7)  # The start date of simulation, adjustable
    # We can define more looms, depending on the conditions for each simulation
    L1 = Loom("l1", 200, 0.5)  # First loom characteristics
    L2 = Loom("l2", 300, 0.5)  # Second Loom characteristics
    L3 = Loom("l3", 400, 0.8)  # Third Loom characteristics
    # For each loom, speed and performance index should be defined here
    looms = [L1, L2, L3]
    # Each loom should be added in the looms dictionary

    fixed_energy_cost = 1  # Fixed energy cost of loom while in work, adjustable
    setup_cost = 0  # Setup cost of a loom, initially 0

    jobs = all_jobs
    jobs_total_number = len(original_jobs)+1
    env.process(weaver2(env, looms[0]))
    env.process(weaver2(env, looms[1]))
    env.process(weaver2(env, looms[2]))

    days_to_simulate = 29  # Number of days the simulation is running, adjustable
    env.run(until=days_to_simulate * 8)  # Running the environment for number of days based on 8 hours of work/day

    lost_profit_from_delays = dict()  # Defining a dictionary object to store the penalty loss of orders
    # Calculating Profit Loss
    print()

    count_delayed_orders = 0
    count_unfinished_orders = 0
    for j in all_jobs:  # Iterating over jobs to calculate penalties for late orders
        # print(j.get_identifier())
        try:
            id = j.get_identifier()
            delivered_on = ending_times[id]
            days, hours = delivered_on // 8, delivered_on % 8
            delivered_on = start_time + timedelta(days=days, hours=hours)
            delay = delivered_on - j.get_duedate()
            if delay.days > 0:
                fine = delay.days * j.get_quantity()
                lost_profit_from_delays[id] = fine
                count_delayed_orders = count_delayed_orders + 1
        except:
            print("Unfinished Order:", j.get_identifier())
            # Some jobs might remain unfinished at the end of simulation, print them
            count_unfinished_orders = count_unfinished_orders + 1

    print("Amount of unfinished orders:", count_unfinished_orders)
    print()
    print("Total Fine per delayed job: ")
    for j, f in lost_profit_from_delays.items():  # Iterating over lost profit and printing
        print(j, f)
    total_lost_profit_from_delays = sum(lost_profit_from_delays.values())
    print("Total Lost Profit at the end due to delays:", total_lost_profit_from_delays)
    fixed_energy_cost = fixed_energy_cost * active_time
    total_loss = int(total_lost_profit_from_delays + fixed_energy_cost + setup_cost)
    print("Total Loss after including setup fees and active time fees:", round(total_loss))
    # Printing the total fine taking under consideration setup and loom active time fee

    list_to_write = [run, count_delayed_orders, count_unfinished_orders, total_lost_profit_from_delays, total_loss]
    # Set up list to write to file

    with open("weaving_process_results.csv", "a") as f:
        # Write list in file
        writer = csv.writer(f, delimiter=",")

        writer.writerow(list_to_write)

# Reading weaving_process_results file as a dataframe and calculating means
results = pd.read_csv("weaving_process_results.csv")
mean_count_delayed_orders = results["Delayed Orders"].mean()
mean_count_unfinished_orders = results["Unfinished Orders"].mean()
mean_total_lost_profit_from_delays = results["Lost Profit due to Delays"].mean()
mean_total_loss = results["Total Loss"].mean()

# Printing the means and rounding them up
print("Calculated Means for 100 performed Simulations:")
print("Mean of Delayed Orders:", math.ceil(mean_count_delayed_orders))
print("Mean of Unfinished Orders:", math.ceil(mean_count_unfinished_orders))
print("Mean of Total Lost Profit due to Delays:", math.ceil(mean_total_lost_profit_from_delays))
print("Mean of Total Loss:", math.ceil(mean_total_loss))


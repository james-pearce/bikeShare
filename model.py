from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid, SingleGrid
from mesa.datacollection import DataCollector
import numpy as np
import random

class BikeRider(Agent):
    """A bike rider who can be registered or casual.

    Attributes:
        unique_id: unique integer
        x, y: grid coordinates [location??]
        aware: does the rider know about the bike share scheme?
        destination: where is the rider going?
        currently_riding: is the rider currently riding at the moment?
        threshold: if probability of riding > threshold, then ride
        rider_type: registered or casual
        ride_probability: probability of riding at this time

    """
    # def __init__(self, unique_id, model, pos, aware, destination, currently_riding, threshold, rider_type,
    #              ride_probability, ride_duration):



    def __init__(self, unique_id, model, threshold):
        super().__init__(unique_id, model)
        self.type = 'rider'
        # self.pos = pos
        # self.aware = True # true for now; need to introduce dispersion
        self.destination = None
        self.currently_riding = False
        self.threshold = threshold
        # self.rider_type = rider_type
        # self.ride_probability = 0.8
        self.ride_probability = None
        # self.ride_duration = ride_duration
        # Needs to be configuration driven rather than code

    def step(self):
        """

        Will rider go for a ride?

        """
        print ("Id: " + str(self.unique_id) + " ; " + str(self.type) + " ; " + str(self.currently_riding))
        if self.currently_riding:
            print ("At destination " + str(self.destination.pos) + " for " + str(self.unique_id))

            # check there is capacity at the station
            this_station = self.destination
            if this_station.n_bikes < this_station.capacity:
                this_station.n_bikes += 1

                self.currently_riding = False

                self.model.grid.place_agent(self, self.destination.pos)

                self.destination = None
            else:
                # ride to the nearest station
                print("* station " + str(this_station.unique_id) + " has " + str(this_station.n_bikes))
                nearby_stations = self.model.grid_stations.get_neighbors(this_station.pos, moore=True,
                                                                         include_center=False, radius=self.model.radius)

                new_destination = random.choice(nearby_stations)

                self.destination = new_destination
                print("Diverting ... " + str(self.unique_id) + " from " + str(this_station.pos) + " to " + str(new_destination))



        else:
            self.ride_probability = np.random.uniform(size=1)
            # print(str(self.ride_probability) + " > " + str(self.threshold))
            if self.ride_probability >  self.threshold:
                self.move()


    def move(self):
        # possible_destinations = self.model.grid.get_neighborhood(
        #     self.pos,
        #     moore = True,
        #     include_center = False
        # )
        # new_destination = random.choice(possible_destinations)
        # self.model.grid.move_agent(self, new_destination)

        # get the destination

        # is there a station here?
        if self.model.grid_stations.is_cell_empty(self.pos):
            # move to adjacent cell
            print(" Wants to ride but not at a station.")
            # random choice of destination
            possible_destinations = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False,
                                                                     radius=1)
            new_destination = random.choice(possible_destinations)
            self.model.grid.move_agent(self, new_destination)
        else:
            # at a station
            this_station = self.model.grid_stations.get_neighbors(self.pos, 0, True)[0]

            # take a bike
            ## TODO: bikes could be agents??
            if this_station.n_bikes == 0:
                print ('Warning: no bikes at station')
            else:
                this_station.n_bikes -= 1
                possible_destinations = self.model.grid_stations.get_neighbors(
                    self.pos,
                    moore=True,
                    include_center=False,
                    radius=self.model.radius
                )
                new_destination = random.choice(possible_destinations)
                self.destination = new_destination
                self.currently_riding = True
                print("Riding ... " + str(self.unique_id) + " from " + str(self.pos) + " to " + str(new_destination))

                self.model.grid.remove_agent(self)


class BikeStation(Agent):
    """
    A station with a fixed number of bikes available.

    Not all locations have a station.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.n_bikes = 10 # don't hardcode this in
        self.capacity = 12
        self.type = 'station'

    def __str__(self):
        return "id: " + str(self.unique_id) + " pos: " + str(self.pos) + "\n" + "n_bikes: " + str(self.n_bikes)

class BikeShare(Model):
    """A model with some number of potential riders."""
    global hours_per_day
    hours_per_day = 24

    def __init__(self, N, M, width, height):
        # self.running = True
        self.num_agents = N
        # self.grid = MultiGrid(width, height, True)

        self.num_stations = M
        self.radius = np.int(np.sqrt(width * height))
        self.grid = MultiGrid(width, height, True)
        self.grid_stations = SingleGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.timestamp = 0 # use to find days
        self.datestamp = 0

        threshold = 0.8

        # create agents
        for i in range(self.num_agents):
            a = BikeRider(i, self, threshold)
            self.schedule.add(a)

            # add the agent to a random grid cell
            x = np.random.randint(self.grid.width)
            y = np.random.randint(self.grid.height)
            self.grid.place_agent(a, (x, y))


        for i in range(self.num_stations):
            s = BikeStation(i, self)
            self.schedule.add(s)

            # add the station to a random grid cell
            # x = np.random.randint(self.grid_stations.width)
            # y = np.random.randint(self.grid_stations.height)
            self.grid_stations.position_agent(s) # ensures one station max
            # self.grid.place_agent(s, s.pos)
            print ("Station " + str(s.unique_id) + "; " + str(s.pos))

        # self.datacollector = DataCollector(
        #     model_reporters={"Gini": compute_gini},
        #     agent_reporters={"Wealth": lambda a: a.wealth}
        # )


    def step(self):
        '''Advance the model by 1 step: arbitrary unit of time. '''
        # self.datacollector.collect(self)
        # print ("Step the schedule ...")
        # print (str(self.timestamp))
        self.timestamp += 1
        if self.timestamp % hours_per_day == 0:
            print ("\n**** new day " + str(self.datestamp))
            self.datestamp += 1
            self.timestamp = 0
        self.schedule.step()


import json
import pandas
import requests
from bs4 import BeautifulSoup
from datetime import datetime


class nextSpaceFlight:
    def __init__(self):
        self.number_of_pages_for_next_flight = 11
        # next space flight links
        self.next_space_flight_link = "https://nextspaceflight.com/launches/?search="
        self.past_space_flight_link = 'https://nextspaceflight.com/launches/past/?search='
        self.soup = None
        # store data for space flights
        self.space_craft_name_list = []
        self.card_header_list = []
        self.next_space_fight_time_list = []
        self.launching_location_list = []
        self.page_number = 1
        self.extracting_link = None
        self.directory = "upcoming_space_flight_data"
        # create file name with today's date
        self.file_name = f"upcoming_space_flight_{str(datetime.now()).split()[0]}"
        # column names or keys
        self.COLUMNS = ["spacecraft", "headline", "launching_location", "time_for_next_space_flight"]

    # creating soup for each page
    def create_soup(self):
        # updating link for each page based on upcoming or past
        if 'past' in self.extracting_link:
            updated_link = f'{"/".join(self.extracting_link.split("/")[:5])}/?page={self.page_number}&search='
        else:
            updated_link = f'{"/".join(self.extracting_link.split("/")[:4])}/?page={self.page_number}&search='
        # making soup of page
        self.soup = BeautifulSoup(requests.get(updated_link).text, 'html.parser')
        # checking if current page is last or not
        bottom_buttons = self.soup.select(".mdc-button--raised")
        last_page = False
        for button in bottom_buttons:
            if button.text.strip().split()[0] == "last":
                last_page = True
        return last_page

    # extract data from each page
    def extract_space_flight_data(self, link):
        self.extracting_link = link
        # update last column/key, file name, directory for past space flight
        if 'past' in link:
            self.COLUMNS[3] = "past_space_flight_time"
            self.file_name = self.file_name.replace('upcoming', 'past')
            self.directory = "past_space_flight_data"
        # this loop will run till last page automatically
        while True:
            last_page = self.create_soup()
            # printing message according to past/upcoming space flights
            print(f"EXTRACTING PAST SPACE FLIGHT DATA FROM PAGE # {self.page_number}") if 'past' in link else \
                print(f"EXTRACTING UPCOMING SPACE FLIGHT DATA FROM PAGE # {self.page_number}")
            self.page_number += 1
            # get spacecraft name
            for spacecraft in self.soup.select('.mdl-card__title-text span'):
                self.space_craft_name_list.append(spacecraft.text.strip())
            # get header for card
            for card_header in self.soup.find_all(name='h5', class_="header-style"):
                self.card_header_list.append(card_header.text.strip())
            # get launch location
            for next_flight in self.soup.select('.mdl-card__supporting-text'):
                self.launching_location_list.append(next_flight.text.strip().split("\n")[-1].strip())
            # get launch time
            for next_flight in self.soup.select('.mdl-card__supporting-text'):
                self.next_space_fight_time_list.append(next_flight.text.strip().split("\n")[0])
            # break if last page
            if not last_page:
                break
        self.upload_data_to_csv_file()
        self.upload_data_to_json_file()

    # uploading data to csv file
    def upload_data_to_csv_file(self):
        print(f"UPLOADING DATA TO {self.directory}/CSV FILE")
        # all flight data in one list to upload data on csv file
        all_flight_data = []
        # loop through each space flight and append it to all_flight_data list
        for i, space_craft_name in enumerate(self.space_craft_name_list):
            all_flight_data.append(self.get_new_space_flight_data(i, space_craft_name))
        # creating pandas dataframe to upload data to csv file
        data_frame = pandas.DataFrame(data=all_flight_data, columns=self.COLUMNS)
        data_frame.to_csv(f"{self.directory}/CSV/{self.file_name}.csv", index=False)

    # upload data to json file
    def upload_data_to_json_file(self):
        print(f"UPLOADING DATA TO {self.directory}/JSON FILE")
        # all flight data in one dictionary to upload JSON file
        all_space_flight = {}
        # creating JSON file
        with open(f"{self.directory}/JSON/{self.file_name}.json", "w") as file:
            # Loop through each space flight for past/upcoming
            for i, space_craft_name in enumerate(self.space_craft_name_list):
                all_space_flight[f"space_flight#{i + 1}"] = self.get_new_space_flight_data(i, space_craft_name)
            # uploading data to JSON file
            json.dump(all_space_flight, file, indent=4)

    # return dictionary of each space flight for upcoming/past flight
    def get_new_space_flight_data(self, i, space_craft_name):
        return {self.COLUMNS[0]: space_craft_name,
                self.COLUMNS[1]: self.card_header_list[i],
                self.COLUMNS[2]: self.launching_location_list[i],
                self.COLUMNS[3]: self.next_space_fight_time_list[i]
                }

    # empty all storage
    def reset_data(self):
        self.page_number = 1
        self.soup = None
        self.space_craft_name_list = []
        self.card_header_list = []
        self.next_space_fight_time_list = []
        self.launching_location_list = []
        self.page_number = 1
        self.extracting_link = None

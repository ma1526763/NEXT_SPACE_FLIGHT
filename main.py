import os
from next_space_flight import nextSpaceFlight
from upload_data_to_google_form import upload_data
from mail_next_space_flight_in_upcoming_days import send_mail

# google form link
UPCOMING_SPACE_FLIGHT_GOOGLE_FROM_URL = os.environ['UPCOMING_SPACE_FLIGHT_GOOGLE_FORM']
PAST_SPACE_FLIGHT_GOOGLE_FROM_URL = os.environ['PAST_SPACE_FLIGHT_GOOGLE_FORM']
# number of days for all flights in next/past days
compare_days = 10

def upcoming_space_flights():
    # extract data from all pages for upcoming space flight
    space_flight.extract_space_flight_data(space_flight.next_space_flight_link)
    # send email for next upcoming flights inn next 10 days
    send_mail("upcoming_space_flight_data", space_flight.file_name, compare_days)
    # uploading upcoming space flight data
    upload_data(space_flight, UPCOMING_SPACE_FLIGHT_GOOGLE_FROM_URL)

def past_space_flights():
    # extract data from all pages for past space flight
    space_flight.extract_space_flight_data(space_flight.past_space_flight_link)
    # send email for next upcoming flights in past 10 or any other  days
    send_mail("past_space_flight_data", space_flight.file_name, compare_days)
    # uploading past space flight data
    upload_data(space_flight, PAST_SPACE_FLIGHT_GOOGLE_FROM_URL)

# program starts here
space_flight = nextSpaceFlight()
upcoming_space_flights()
space_flight.reset_data()
past_space_flights()
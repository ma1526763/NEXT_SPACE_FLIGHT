import os
import pandas
from smtplib import SMTP
from email.message import EmailMessage
from datetime import datetime, timedelta

def get_message(i, space_flight_data, file_name):
    return f"SPACECRAFT: {space_flight_data[i]['spacecraft']}\nHEADLINE : {space_flight_data[i]['headline']}\n" \
                                      f"LAUNCHINF LOCATION: {space_flight_data[i]['launching_location']}\n" \
                                      f"SPACE FLIGHT TIME: {space_flight_data[i]['time_for_next_space_flight' if 'upcoming' in file_name else 'past_space_flight_time']}\n\n"

# NET means no earlier than
def space_flight_in_certain_days(file_directory, file_name, compare_days):
    message_to_send = ""
    # adding number of days that we want to set as comparing days for past space flights it will negate days instead of adding
    comparing_date = (datetime.now() + timedelta(days=compare_days if 'upcoming' in file_name else compare_days * -1)).strftime("%b-%d-%Y")
    # changing data type of time from str to datetime
    comparing_date = datetime.strptime(comparing_date, "%b-%d-%Y")
    # opening required CSV file using pandas and converting it into
    space_flight_data = pandas.read_csv(f"{file_directory}/CSV/{file_name}").to_dict(orient="records")
    # loop through each space flight
    for i, one_space_data in enumerate(space_flight_data):
        # getting time to fly for upcoming/past space flight
        time_to_fly = one_space_data['time_for_next_space_flight' if 'upcoming' in file_name else 'past_space_flight_time'].split()[1:-2]
        # some flights have NET which means they are not good as their date is not confirmed
        if len(time_to_fly) >= 3:
            # making the time to fly in my own zone to compare with compare date
            time_to_fly[1] = time_to_fly[1].split(",")[0]
            time_to_fly = "-".join(time_to_fly)
            save_date = time_to_fly
            time_to_fly = datetime.strptime(time_to_fly, "%b-%d-%Y")
            if 'upcoming' in file_name:
                if time_to_fly <= comparing_date:
                    message_to_send += get_message(i, space_flight_data, file_name)
            else:
                if time_to_fly >= comparing_date:
                    message_to_send += get_message(i, space_flight_data, file_name)
    return message_to_send

def send_mail(f_directory, f_name, c_days):
    print("Please wait while mail is being sent!")
    # this function will open upcoming/past CSV file from given  directory and will create a message based on specific day
    msg_to_send = space_flight_in_certain_days(f_directory, f_name, c_days)

    # creating subject/body for mail to send
    message = EmailMessage()
    message['Subject'] = "UPCOMING SPACE FLIGHT" if 'upcoming' in f_name else "PAST SPACE FLIGHTS"
    message['From'] = os.environ['SENDER_MAIL']
    message['To'] = os.environ['RECEIVER_MAIL']
    message.set_content(msg_to_send[:-2])

    # sending email through gmail server
    with SMTP("smtp.gmail.com") as connection:
        connection.starttls()  # start connection
        connection.login(user=os.environ['SENDER_MAIL'], password=os.environ['PASSWORD'])  # login to mail
        connection.send_message(message)  # sending mail
    print("mail has been sent successfully!!")

# send_mail("past_space_flight_data", "past_space_flight_2023-02-23", 10)

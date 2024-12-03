import time
import sys
import pandas as pd
import numpy as np

#Global variables
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
              
MONTH_DICT = {'all': 0, 'january': 1, 'february': 2, 'march': 3,
              'april': 4, 'may': 5, 'june': 6, 'july': 7,
              'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12}
              
DAY_DICT= {'all':0, 'monday':1, 'tuesday':2, 'wednesday':3, 'thursday':4, 'friday':5, 'saturday':6, 'sunday':7}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    #Get user input for city (chicago, new york city, washington)
    CITY_DICT = {'chicago': 1, 'new york city': 2, 'washington': 3 }
    while True:
        city = input('Would you like to see data for Chicago(1), New York City(2) or Washington(3)?\n' 
                     '- Or \'exit\' to close\n')
        #Check if city is in the dict
        if (city.lower() in CITY_DATA):
            city = city.lower()
            print('\n')
            break
        #catch new york as short for new york city
        elif city.lower()=='new york':
            city = 'new york city'
            print('\n')
            break
        #close the application if user want to
        elif city.lower() == 'exit':
            sys.exit()
        else:
            #check if user choose the city by number
            try:
                city = int(city)
                if (city >=1 and city <=3):
                    city = list(CITY_DICT.keys())[list(CITY_DICT.values()).index(city)]
                    print('You choose', city.title())
                    print('\n')
                    break
                else:
                    print('Unknown city. Please type one of the mentioned options or \"exit\" to close')
            except:
                print('Unknown city. Please type one of the mentioned options or \"exit\" to close')

        
    #Get user input for month (all, january, february, ... , june)
    while True:
        month = input('Please choose a month to analyze (e.g. January(1), February(2), ..., December(12))\n' 
                     '- Or \'all\'(0) to skip filtering of months\n' 
                     '- Or \'exit\' to close\n' )
        #Check if month is in the dict
        if (month.lower() in MONTH_DICT):
            month = month.lower()
            print('\n')
            break
        #close the application if user want to
        elif month.lower() == 'exit':
            sys.exit()
        else:
            #check if user choose the month by number
            try:
                month = int(month)
                if (month >=0 and month <=12):
                    month = list(MONTH_DICT.keys())[list(MONTH_DICT.values()).index(month)]
                    print('You choose', month.title())
                    print('\n')
                    break
                else:
                    print('Unknown month. Please type one of the mentioned options or \"exit\" to close')
            except:
                print('Unknown month. Please type one of the mentioned options or \"exit\" to close')

    #Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Please choose a day to analyze (e.g. Monday(1), Tuesday(2), ..., Sunday(7))\n' 
                    '- Or \'all\'(0) to skip filtering of days\n' 
                    '- Or \'exit\' to close\n' )
        #Check if day is in the dict
        if (day.lower() in DAY_DICT):
            day = day.lower()
            print('\n')
            break
        #close the application if user want to
        elif day.lower() == 'exit':
            sys.exit()
        else:
            #check if user choose the day by number
            try:
                day=int(day)
                if (day>=0 and day <=7):
                    day = list(DAY_DICT.keys())[list(DAY_DICT.values()).index(day)]
                    print('You choose', day.title())
                    print('\n')
                    break
                else:
                    print('Unknown day. Please type one of the mentioned options or \"exit\" to close')
            except:
                print('Unknown day. Please type one of the mentioned options or \"exit\" to close')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = list(MONTH_DICT.keys())
        month = months.index(month)
    
        # filter by month to create the new dataframe
        df_temp = df[df['month'] == month]
        if(df_temp.size==0):
            print('!'*40)
            print('Unfortunately there is no data for {}. Month-filter is set to \'All\''.format(months[month].title()))
            print('!'*40)
            month = 0
        else:
            df = df[df['month'] == month]
            
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    
    Args:
        (DataFrame) df
    Returns: 
        ---
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Display the most common month
    if(df['month'].value_counts().size > 1):            #No filter by month if size of value_counts > 1
        #Find th emost popular month
        popular_month = df['month'].mode()[0]
        number_rentals = df['month'].value_counts().values[0]
        month_name = list(MONTH_DICT.keys())[list(MONTH_DICT.values()).index(popular_month)]
        print('The most popular month for renting a bike is {} with {} of {} rentals'.format(month_name.upper(),number_rentals,df['month'].count()))
       
    #Display the most common day of week
    if(df['day_of_week'].value_counts().size > 1):      #No filter by day if size of value_counts > 1
        #Find th emost popular day of week
        popular_day = df['day_of_week'].mode()[0]
        number_rentals = df['day_of_week'].value_counts().values[0]
        print('The most popular day for renting a bike is {} with {} of {} rentals'.format(popular_day.upper(),number_rentals,df['day_of_week'].count()))


    #Display the most common start hour
    df_startTimeHour = df['Start Time'].dt.hour
    popular_startTime = df_startTimeHour.mode()[0]
    number_rentals = df_startTimeHour.value_counts().values[0]
    print('The most popular start time for renting a bike is {} o\'clock with {} of {} rentals'.format(popular_startTime,number_rentals,df['Start Time'].count()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    
    Args:
        (DataFrame) df
    Returns: 
        ---
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Display most commonly used start station
    popular_startStation = df['Start Station'].mode()[0]
    number_rentals = df['Start Station'].value_counts().values[0]
    print('The most popular start station for renting a bike is {} with {} of {} rentals'.format(popular_startStation,number_rentals,df['Start Station'].count()))
    
    #Display most commonly used end station
    popular_endStation = df['End Station'].mode()[0]
    number_rentals = df['End Station'].value_counts().values[0]
    print('The most popular end station for renting a bike is {} with {} of {} rentals'.format(popular_endStation,number_rentals,df['End Station'].count()))

    #Display most frequent combination of start station and end station trip
    df_startAndEndStation = df['Start Station'] + ' --> ' + df['End Station']
    popular_combinationStations = df_startAndEndStation.mode()[0]
    number_rentals = df_startAndEndStation.value_counts().values[0]
    print('The most popular start-end-combination is {} with {} of {} rentals'.format(popular_combinationStations,number_rentals,df_startAndEndStation.count()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    
    Args:
        (DataFrame) df
    Returns: 
        ---
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Display total travel time
    trip_duration_sum = df['Trip Duration'].sum()       #result is in seconds
    hours = trip_duration_sum // 3600                   #calculate hours from value in seconds
    minutes = (trip_duration_sum % 3600) // 60          #calculate remaining minutes from value in seconds
    seconds = (trip_duration_sum % 3600) % 60           #calculate remaining hours from value in seconds
    print('The total trip duration is {} hours, {} minutes and {} seconds'.format(hours,minutes,seconds))

    #Display mean travel time
    trip_duration_mean = df['Trip Duration'].mean()       #in seconds
    print('The mean trip duration is {} seconds'.format(trip_duration_mean))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    
    Args:
        (DataFrame) df
    Returns: 
        ---
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    if ('User Type' in df.keys()):
        no_userType = df['User Type'].value_counts()
        print('There are {} rentals from {} and {} from {}'.format(no_userType[0],no_userType.keys()[0],no_userType[1],no_userType.keys()[1]))
    else:
        print('Your choosen city has no data about the user type')

    #Display counts of gender
    if ('Gender' in df.keys()):
        no_gender = df['Gender'].value_counts()
        print('There are {} rentals from {} and {} from {}'.format(no_gender[0],no_gender.keys()[0],no_gender[1],no_gender.keys()[1]))
    else:
        print('Your choosen city has no data about the gender')

    #Display earliest, most recent, and most common year of birth
    if ('Birth Year' in df.keys()):
        print('The earliest birthday of a subscriber/customer is {}'.format(int(df['Birth Year'].min())))
        print('The most recent birthday of a subscriber/customer is {}'.format(int(df['Birth Year'].max())))
        print('The most common year of birth of subscriber/customer is {}'.format(int(df['Birth Year'].mode()[0])))
    else:
        print('Your choosen city has no data about the birth year')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def show_raw_data(df):
    """
    Display the filtered raw data. Filter is set by the user in function get_filters(). 
    
    Args:
        (DataFrame) df
    Returns: 
        ---
    """
    
    show_data = input('Do you want to see raw data (5 lines per iteration)? yes/no:\n')
    if show_data.lower()=='yes':
        start=0
        stop=min(5,df.count()[0])
        while True:
            if (stop>=df.count()[0]):
                print(df[start:df.count()[0]])
                break
            else:
                print(df[start:stop])
                more_data = input('Show 5 more lines? yes/no:\n')
                if (more_data.lower() !='yes'):
                    break                
            start+=5
            stop+=5
            
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

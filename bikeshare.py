import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # these virables are used over many function, so it's important to global them rather than code dublecation
    global months,month
    global days,day
    global city
    
    # this list is widely used to define month filter and select data and test analyze availability 
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    
    # this list is widely used to define day filter and select data and test analyze availability
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
    
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        # asking user for city name
        city = input("\nEnter a name of the city to analyze, you can enter 'Chicago' or 'New York City' or 'Washington': ").lower()
        # if city name is valid then go ask for next filter
        if CITY_DATA.get(city) :
            break
        # if city name is not valid then print a massage and keep in loop
        else:
            print("\n[Not valid name] - City '{}' has no data to analyze".format(city))

    # TO DO: get user input for month (all, january, february, ... , june)

    # asking user for month name
    while True:
        month = input("\nEnter a month name to analyze it's data, you can enter {} or 'all' to select all monthes: ".format(months)).lower().strip(" ")
        # if month name is valid then go ask for next filter
        if month in months or month == "all":
             break
        # if month name is not valid then print a massage and keep in loop
        else:
            print("\n[Not valid name] - Month '{}' has no data to analyze".format(month))

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    # asking user for day of week name
    while True:
        day = input("\nEnter a day of week to analyze it's data, you can enter {} or 'all' to select all days: ".format(days)).lower().strip(" ")         # if day name is valid then go ask for next filter
        if day in days or day == "all":
            break
        # if day name is not valid then print a massage and keep in loop
        else:
            print("\n[Not valid name] - Day '{}' has no data to analyze".format(day))


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
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day = days.index(day) + 1
        df = df[df['day_of_week'] == day]


    return (df)


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month

    # find and print the most popular month
    if month == 'all':
        popular_month = df['month'].mode()[0]
        print('\nMost Popular Start Month: ', months[popular_month-1].title())

    # TO DO: display the most common day of week
    
    # find and print the most common day of week
    if day == 'all':
        popular_day = df['day_of_week'].mode()[0]
        print('\nMost Popular Start Day:', days[popular_day-1].title())

    # TO DO: display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most most common start hour
    popular_hour = df['hour'].mode()[0]
    print('\nMost common Start Hour:', popular_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    # calculate and print the mode for 'Start Station' selected column
    most_popular_start_station = df['Start Station'].mode()[0]
    print('\nThe most commonly used start station: ', most_popular_start_station)
    print('-'*40)
    # extract  and print the The top 5 commonly used Start Station from selected column
    popular_start_station = df['Start Station'].value_counts()[:5]
    print('The top 5 commonly used Start Station: \n\n', popular_start_station)
    print('-'*40)

    # TO DO: display most commonly used end station
    # calculate and print the mode for 'End Station' selected column
    most_popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', most_popular_end_station)
    print('-'*40)
    # extract  and print the The top 5 commonly used End Station from selected column
    popular_end_station = df['End Station'].value_counts()[:5]
    print('The top 5 commonly used End Station: \n\n', popular_end_station)
    print('-'*40)
    
    # TO DO: display most frequent combination of start station and end station trip
    # extract new column 'trip' from 'Start Station' and 'End Station' to store paths
    df['trip'] = 'From: ['+df['Start Station']+"] to ["+df['End Station']+']'
    # calculate and print the mode for 'trip' column
    print('Most frequent trips: ',df['trip'].mode()[0])
    print('-'*40)
    # extract  and print the The top 5 most frequent combination of start station and end station trip
    popular_trips = df['trip'].value_counts()[:5]
    print('The top 5 frequent trips: \n\n', popular_trips)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    # calculate and print total travel time by sum values in 'Trip Duration' column
    total_duration = sum(df['Trip Duration'])
    print('Total travel time: ',total_duration)

    # TO DO: display mean travel time
    # calculate and print Mean travel time by finding mean value in 'Trip Duration' column
    duration_mean = df['Trip Duration'].mean()
    print('Mean travel time: ',duration_mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    # count of all unique values for the column user types
    counts_of_user_types = df['User Type'].value_counts()
    print(counts_of_user_types)
  
    # TO DO: Display counts of gender
    # since washington.csv dosn't has 'Gender' data, this if statement is here to ensure that city is not Washington
    if city != 'washington':
        # count of all unique values for the column 'Gender'
        counts_of_gender = df['Gender'].value_counts()
        # print counts of gender
        print(counts_of_gender)
        print('-'*40)

    # TO DO: Display earliest, most recent, and most common year of birth
        # ignore blank elements in 'Birth Year' column
        df['Birth Year'] = df['Birth Year'].dropna()
        # calculate and print earliest birth year by find the minimum value in 'Birth Year' column
        earliest_birth_year = df['Birth Year'].min()
        print('\nEarliest birth year: ',int(earliest_birth_year)) 
        # calculate and print most recent birth year by find the maximum value in 'Birth Year' column
        recent_birth_year = df['Birth Year'].max()
        print('\nMost recent birth year: ',int(recent_birth_year))
        # calculate and print most common birth year by find the mode value in 'Birth Year' column
        common_birth_year = df['Birth Year'].mode()
        print('\nMost common birth year: ',int(common_birth_year))
        
        print("\nThis took %s seconds." % (time.time() - start_time))
        
    print('-'*40)
    
    # Display random simple of data
    # while loop for asking user if he want to see a rondom simple of data
    while True:
        message = input('\nWould you like to see a simple of random data? Enter yes or no.\n').lower()
        if message != 'yes':
            break
        else:
            print(df.sample(10))
            print("\nThis took %s seconds." % (time.time() - start_time))
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

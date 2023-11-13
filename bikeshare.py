import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york city', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Getting user input for city (chicago, new york city, washington) 
    # Making entries case-insensitive and use small letters when assigning city name
    while True:
        city = input("Data from which city would you like to explore? " +
                     "You can choose: Chicago, New York City or Washington.\n\n").lower()            
        # Handling with invalid input for the city
        if city in cities:
            break
        else:
            print('Please enter a valid city name.')

    # Getting user input for month and day (all, january, february, ... , june)
    # Making entries case-insensitive and use small letters when choosing a month
    while True:
        month = input("Which month would you like to analyze for " + city.title() +
                      "? You can choose: January, February, March, " +
                      "April, May and June, or type all if you do not wish "+
                      "to specify a month.\n\n").lower()
                     
        # Handling with invalid input for the month
        if month in months:
            break
        else:
            print("Please enter a valid month.")

    # Getting user input for day of week (all, monday, tuesday, ... sunday)
    # Making entries case-insensitive and use small letters when choosing a day
    while True:
        day = input("Ok, we got it. Now it's time to pick a day. " +
                    "You can choose: Monday, Tuesday, Wednesday," +
                    "Thursday, Friday, Saturday or Sunday, or type all if " +
                    "you do not wish to specify a day.\n\n").lower()
                     
        # Handling with invalid input for the day
        if day in days:
            break
        else:
            print("Please enter a valid month.")
                     
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
    # Loading data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # Converting Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Creating new columns: month and day of a week to filter
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # Filtering the dataset
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # Filtering by month to create a new dataframe
        df = df[df['month'] == month]
        
    if day != 'all':
        # Filtering by day of week to create a new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Displaying the most common month
    popular_month = df['month'].mode()[0]
    
    # Change number to months
    if popular_month == 1:
        popular_month = "January"
    elif popular_month == 2:
        popular_month = "February"
    elif popular_month == 3:
        popular_month = "March"
    elif popular_month == 4:
        popular_month = "April"
    elif popular_month == 5:
        popular_month = "May"
    elif popular_month == 6:
        popular_month = "June"
    
    print("The most common month is", popular_month, ".")

    # Displaying the most common day of week
    print("The most common day of week is", df['day_of_week'].mode()[0], ".")

    # Displaying the most common start hour
    # Creating new column with a start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    # Taking into account the time of day
    if popular_hour < 12:
        print("The most common start hour", popular_hour, "AM.")
    elif popular_hour >= 12:
        if popular_hour > 12:
            popular_hour -= 12
        print("The most common start hour is", popular_hour, "PM.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displaying most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("The most common Start Station is", popular_start_station, ".")

    # Displaying most commonly used end station
    popular_end_station = df['Start Station'].mode()[0]
    print("The most common End Station is", popular_end_station, ".")

    # Display most frequent combination of start station and end station trip
    station_combination = df['Start Station'] + " to " + df['End Station']
    popular_station_combination = station_combination.mode()[0]
    print("The most common Start to End Station combination is:\n {}".format(popular_station_combination))

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Displaying total travel time
    total_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print("Total Travel time is {} Hours, {} Minutes and {} Seconds.".format(hour, minute, second))

    # Displaying mean travel time
    avg_duration = round(df['Trip Duration'].mean())
    minute, second = divmod(avg_duration, 60)
    if minute > 60:
        hour, minute = divmod(minute, 60)
        print("Average Travel Time is {} Hours, {} Minutes and {} Seconds.".format(hour, minute, second))
    else:
        print("Average Travel Time is {} Minutes and {} Seconds.".format(minute, second))
          
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displaying counts of user types
    user_types = df['User Type'].value_counts()
    
    print("Counts of user types:\n", user_types)
 
   
    # Displaying counts of gender 
    # remembering, that we don't have gender information for Washington
    try:
        gender = df['Gender'].value_counts()
        print("\nCounts of gender type:\n", gender)
    except:
        print("Sorry! Information about gender is not available for Washington.")
        #print("Sorry! Information about gender is not available for {}."format(city.title()))
    
    # Displaying earliest, most recent, and most common birth year 
    # remembering, that we don't have birth year information for Washington
    try:
        earliers_by = df['Birth Year'].min()
        most_recent_by = df['Birth Year'].max()
        most_common_by = df['Birth Year'].mode()[0]
        
        print("\nThe earliest year of birth is", int(earliers_by), ".")
        print("The most recent year of birth is", int(most_recent_by), ".")
        print("The most common year of birth is", int(most_common_by), ".\n")
        
    except:
        print("Sorry! Information about birth year is not available for Washington.")
        #print("Sorry! Information about birth year is not available for {}."format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    # Displaying raw data on request
    x = 1
    while True:
        raw_data = input("\nWould you like to see some raw data? Answer yes or no.\n")
        if raw_data.lower() == 'yes':
            print(df[x: x + 5])
            x = x + 5
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

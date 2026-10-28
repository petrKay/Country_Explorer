import os
import subprocess

import requests


def clear_terminal():
    if os.name == "nt":
        subprocess.run('cls', shell=True)
    else:
        subprocess.run('clear', shell=True)


def read_menu_choice():
    invalid_choice=False

    while True:
        clear_terminal()

        print("Main Menu\n")
        print("1. Get country information.")
        print("2. Compare two countries.\n")
  
        if invalid_choice:
            if not user_choice:
                print("Error: Choice can't be empty")
            else: 
                print('Error: Invalid choice. Use only "1","2" or "exit"')

        user_choice = input('Enter "1" or "2". Type "exit" to quit: ').casefold().strip()

        if user_choice == "1" or user_choice == "2":
            return user_choice
        elif user_choice == "exit":
            return None
        else:
            invalid_choice = True


def select_country(country_list):
    '''Lets user select one from all matching the request countries. '''

    list_length = len(country_list)
    if  list_length == 1:
        return country_list[0]

    while True:
        clear_terminal()

        for i,country in enumerate(country_list, start = 1):
            print(f'{i}.', country['name'])

        user_choice = input(f'Enter a number from 1 to {list_length} or type "exit" to go back to Main Menu: ').casefold().strip()
        print()

        if user_choice == "exit":
            return None

        try:
            num = int(user_choice)
        except ValueError:
            print(f"The provided input is not a valid whole number between 1 and {list_length}. ")
            input('Press "Enter" to continue. ')
        else:
            if 1 <= num <= list_length:
                return country_list[num-1]
            else:
                input(f'The number you entered is out of range. Press "Enter" to continue. ')
   
  
def try_again(in_string = None):
    '''Prints 'Would you like to try again (y/n):' by default. Or in_string (str) is specified" 
    returns True or False'''

    if in_string == None:
        output_string = "Would you like to try again (y/n): "
    else:
        output_string = str(in_string)

    while True:
        answer = input(output_string).casefold().strip()

        clear_terminal()

        if answer == "y":
            return True 
        elif answer == "n":
            return False


def fetch_countries(country_query):
    '''In: string. Out: Full list of countries matches string'''

    URL = 'https://countries.dev/name/'

    while True:
        try:
            data = requests.get(URL + country_query, timeout=10)
            data.raise_for_status()
            country_list = data.json()

        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 404:
                print('Nothing matches your request. ')
                return None
            else:
                print('An HTTP error occurred. ')
                if try_again():
                    continue
                else:
                    return None

        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError):
            print('A сonnection or timeout error occurred while trying to connect to the remote server. ')

            if try_again():
                continue
            else:
                return None

        except ValueError:
            input('Error: Could not process the server response. Press "Enter" to continue. ')
            return None
            
        else:
            if not isinstance(country_list, list):
                input('Error: Expected to receive a list of countries. Press "Enter" to continue. ')
                return None
            
            if not country_list:
                input('Nothing matches your request. Press "Enter" to continue. ')
                return None
            
            for country in country_list:
                if not isinstance(country, dict):
                    input('Error: Expected to receive a country dict. Press "Enter" to continue. ')
                    return None

                if not country:
                    input('Error: received an empty dict. Press "Enter" to continue. ')
                    return None

                if "name" not in country:
                    input('Error: Key "name" is missing. Press "Enter" to continue. ')
                    return None

                value = country["name"]
                if  value is not None and str(value).strip() != "": 
                    continue
                else:
                    input('Error: Received an invalid or empty country name. Press "Enter" to continue. ')
                    return None 
                
            return country_list 
              

def read_country_query(country_num = None):
    '''User's country name keyboard input'''

    if country_num is None:
        country_num=""

    user_country_input = None

    while True:
        clear_terminal()

        user_country_input = input(f'Enter {country_num} country name or "exit" to go back to Main Menu: ').casefold().strip()
        print()

        if user_country_input == "":
            input('Error: Country name can\'t be empty. Press "Enter" to continue. ')
        elif user_country_input == "exit":
            return None
        else:
            return user_country_input      


def output_to_display(countries):
    '''Output as a table: Name, Capital, Population, Area'''
    clear_terminal()

    if not isinstance(countries, list):
        input('Error: Expected to receive a list of countries to display. Press "Enter" to continue. ')
        return

    COLUMN_HEADERS = {"name": "Country",
                      "capital": "Capital",
                      "population": "Population",
                      "area": "Area"}

    col_widths = {}
    # looking for a max width for each column and store it in col_widths
    for col, header_text in COLUMN_HEADERS.items():
        col_values = [str(row.get(col,'Not available')) for row in countries]
        all_texts = col_values + [header_text]
        max_width = max([len(text) for text in all_texts])
        col_widths[col] = max_width + 2

    # print header of the table
    header_row = ""
    for col, header_text in COLUMN_HEADERS.items():
        width = col_widths[col]
        header_row += f"{header_text:<{width}}"
    print(header_row)

    # print body of the table
    for country in countries:
        body_row=""
        for key in COLUMN_HEADERS.keys():
            width = col_widths[key]
            value = country.get(key, 'Not available')

            if isinstance(value, int):
                 country_info = f"{value:,}"
            else:
                country_info = str(value)
                
            body_row+=f"{country_info:<{width}}"
        print(body_row)

    input('\nPress "Enter" to return to Main Menu.')  


def find_and_select_country(country_count = None):
    ''' Fetches all matching countries and lets user select one.
        country_count (int) How many countries need to be searched'''

    if not isinstance(country_count, int) and country_count is not None:
        input('Error: Expected an integer value for the country count.\nPress "Enter" to continue. ')
        return
    elif country_count is None:
        NUM_OF_COUNTRIES = 1
    elif country_count <= 0:
        input('Error: Expected a positive integer value more than zero for the country count.\nPress "Enter" to continue. ')
        return None
    else:
        NUM_OF_COUNTRIES = country_count
   
    country_list_to_display= []

    while (len(country_list_to_display) + 1) <= NUM_OF_COUNTRIES:
        if country_count is None:
            country_query = read_country_query()
        else:
            country_query = read_country_query(len(country_list_to_display) + 1)

        if country_query is None:
            return None
       
        t_country_list = fetch_countries(country_query)   # temp list

        if t_country_list is None:
            if try_again("Do you want to search for another country name? (y/n): "):
                continue
            else:
                return None
            
        t_country_to_display = select_country(t_country_list)

        if t_country_to_display is None:
            return None
        
        if t_country_to_display in country_list_to_display:
            input('The country you choose is already in the comparison list.\n' 
                'Press "Enter" to choose a different country. ')
            continue
        else:
            country_list_to_display.append(t_country_to_display)  # final country list that goes to the output function
    
    return country_list_to_display

 

def run_country_search():
    clear_terminal()

    country_list = find_and_select_country()

    if country_list is None:
        return
    
    output_to_display(country_list)


def run_country_comparison():
    clear_terminal()

    NUM_OF_COUNTRIES_TO_COMPARE = 2

    country_list = find_and_select_country(NUM_OF_COUNTRIES_TO_COMPARE)
    if country_list is None:
        return
        
    output_to_display(country_list)
    
           
def main():
    while True:
        match read_menu_choice():
            case "1": 
                run_country_search()
            case "2": 
                run_country_comparison()
            case None:
                break

       
main()

    
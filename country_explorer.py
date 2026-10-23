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
            invalid_choice = True

        user_choice = input('Enter "1" or "2". Type "exit" to quit: ').casefold().strip()

        if user_choice == "1" or user_choice == "2":
            return user_choice
        elif user_choice == "exit":
            return None
        else:
            invalid_choice = True


def select_coutry(country_list):
    list_length = len(country_list)
    if  list_length == 1:
        return country_list

    while True:
        clear_terminal()

        for i,country in enumerate(country_list,start=1):
            print(f'{i}.', country['name'])

        user_choice = input(f"Enter a number from 1 to {list_length}: ")

        try:
            num = int(user_choice)

            if 1 <= num <= list_length:
                return country_list[num-1]
            else:
                input(f"The number you entered is out of range. ")

        except:
            input(f"Provided input is not a valid whole number within the range. ")
   

   
def try_again():
    answer = ""

    while answer != "y" or answer != "n":
        answer = input("Would you like to try again (y/n): ").casefold().strip()

        clear_terminal()

        if answer == "y":
            return True
        elif answer == "n":
            return False


def fetch_countries(country_query):
    URL = 'https://countries.dev/name/'

    while True:
        try:
            data = requests.get(URL + country_query, timeout=10)
            data.raise_for_status()
            country_list = data.json()

        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 404:
                input('Nothing matches your request. Press "Enter" to continue. ')
            else:
                input('An HTTP error occurred. Press "Enter" to continue. ')

        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError):
            print('A сonnection or timeout error occured while trying to connect to the remote server. ')
            if try_again():
                continue 
            else:
                break 
    
        except ValueError:
            input('Error. Inappropriate argument value (of correct type). Press "Enter" to continue. ')
            
        else:
            return country_list

        break


def read_country_query():
    user_country_input = None

    while True:
        clear_terminal()

        user_country_input = input('Enter country name or "exit" to go back to Main Menu: ').casefold().strip()

        if user_country_input == "":
            input('Error: Country name can\'t be empty. Press "Enter" to continue. ')

        if user_country_input == 'exit':
            return None
        elif user_country_input == "":
            continue
        else:
            return user_country_input      


def output_to_display(country):
    clear_terminal()

    if country:
        for c in country:
            print("Country: ", c['name']) 

        input('Press "Enter" to return to Main Menu.')
        
    return  


def find_and_select_country(country_num = None):
    county_list_to_display=[]

    while True:
        country_query = read_country_query()

        if country_query is None:
            return

        t_county_list = fetch_countries(country_query)

        if isinstance(t_county_list, list):
            t_country_to_display = select_coutry(t_county_list)
            
            if isinstance(t_country_to_display, dict) and t_country_to_display is not None:
                county_list_to_display.append(t_country_to_display)
                break
            else:
                input('Error. Expected to recieve a country dict. Press "Enter" to continue. ')
                
        elif t_county_list is None:
                continue
        else:
            input('Error. Expected to recieve a list of countries. Press "Enter" to continue. ')

    if isinstance(county_list_to_display, list) and county_list_to_display is not None:
            output_to_display(county_list_to_display)
    else:
            input('Error. Expected to recieve a list of countries to display. Press "Enter" to continue. ')
    #input(f'Debug: find_and_select_country(). returned: {country_query}')


def run_country_search():
    clear_terminal()

    country_list = find_and_select_country()
    # input(f'\nDebug: End of run_country_search(). {type(country_list)}')



def run_country_comparison():
    clear_terminal()

    #input('Debug: End of run_country_comparison()')

           
def main():
    while True:
        match read_menu_choice():
            case "1": 
                run_country_search()
            case "2": 
                run_country_comparison()
            case None:
                break

    # input('Press "Enter" to continue...')
       
main()

    
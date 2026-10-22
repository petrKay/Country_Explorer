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


def try_again():
    answer = ""
    while answer == "y" or answer == "n":
        answer = input("Would you like to try again (y/n): ").casefold().strip()
        clear_terminal()

    if answer == "y":
        return True
    elif answer == "n":
        return False


def fetch_countries(country_query):
    URL = 'https://countries.dev/name/'

    try:
        data = requests.get(URL + country_query, timeout=10)
        data.raise_for_status()
        country_list = data.json()

    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 404:
            input('Nothing matches your request. Press "Enter" to continue. ')
        
        else:
            input('An HTTP error occurred. Press "Enter" to continue. ')

    except (requests.exceptions.Timeout or 
            requests.exceptions.ConnectionError):
        print('A сonnection or timeout error occured while trying to connect to the remote server.  Press "Enter" to continue. ')
        ''' if try_again():
            input('y')  # continue
        else:
            input('n')  # break'''
 
    except ValueError:
        input('Error. Inappropriate argument value (of correct type). Press "Enter" to continue. ')
        
    else:
        return country_list


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
    

def find_and_select_country():
    while True:
        country_query = read_country_query()

        if not country_query:
            return

        country_list = fetch_countries(country_query)

        if isinstance(country_list, list):
            return country_list
            '''# debug output
            if country_list:
                for c in country_list:
                    print("Country: ", c['name'])   
                input('Debug: Enter to continue')
                break;
            '''

         
    #input(f'Debug: find_and_select_country(). returned: {country_query}')


def run_country_search():
    clear_terminal()
    find_and_select_country()

    # input('\nDebug: End of run_country_search()')
    return


def run_country_comparison():
    clear_terminal()

    #input('Debug: End of run_country_comparison()')
    return

           
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

    
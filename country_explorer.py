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

        if user_choice == "1" or user_choice == "2" or user_choice == "exit"  :
            return user_choice
        else:
            invalid_choice = True


def find_and_select_country():
    return


def run_country_search():
    clear_terminal()
    find_and_select_country()

    # input('Debug: run_country_search()')
    return


def run_country_comparison():
    clear_terminal()

    # input('Debug: run_country_comparison()')
    return

           
def main():
    match read_menu_choice():
        case "1": 
            run_country_search()
        case "2": 
            run_country_comparison()

    # input('Press "Enter" to continue...')
    
    
main()

    
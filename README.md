# Country Explorer

This is a Python console application that shows information about countries.
You can search for one country or compare two countries.
The program shows the country name, capital, population, and area.

## API

I used the countries.dev API to get country information:

https://countries.dev/name/{country_name}

The program uses the requests library to get the data.
You need an internet connection to use it.

## How to run

You need Python 3.10 or newer.

1. Download the project.
2. Open a terminal in the project folder.
3. Install the required library.

   On Linux or macOS:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

   On Windows:

   ```powershell
   py -m pip install -r requirements.txt
   ```

4. Run the program.

   On Linux or macOS:

   ```bash
   python3 main.py
   ```

   On Windows:

   ```powershell
   py main.py
   ```

## How to use

- Enter 1 to search for a country.
- Enter 2 to compare two countries.
- Enter a country name.
- If there is more than one result, choose a country from the list.
- Type exit in the main menu to close the program.
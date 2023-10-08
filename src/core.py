import random
import re

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from time import sleep

def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode (without GUI)
    options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration (often used with headless)
    options.add_argument('--no-sandbox')  # Bypass OS-level security, sometimes necessary in certain environments
    options.add_argument('--log-level=3')  # Suppress info/debug logs

    while True:
        driver_headless = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
        driver_headless.get('https://trapeza.iep.edu.gr/public/subjects.php')
        sleep(2)

        # Select value 3 in #schooltype dropdown
        select_schooltype = Select(driver_headless.find_element_by_id('schooltype'))
        select_schooltype.select_by_value('3')
        sleep(1)  # Give some time for the next dropdown to populate if it's dynamically loaded

        # Select value 3 in #class dropdown
        select_class = Select(driver_headless.find_element_by_id('class'))
        select_class.select_by_value('3')
        sleep(1)  # Give some time for the next dropdown to populate if it's dynamically loaded

        # Select value 182 in #lesson dropdown
        select_lesson = Select(driver_headless.find_element_by_id('lesson'))
        select_lesson.select_by_value('182')
        sleep(1)  # Wait for the #content-select dropdown to be visible

        # List all options in #content-select dropdown in a window
        select_content = Select(driver_headless.find_element_by_id('content-select'))
        formatted_options = [
            "{} - {}".format(option.get_attribute("value"), option.text)
            for option in select_content.options if not option.text.startswith("ΚΕΦΑΛΑΙΟ")
        ]
        print("\n".join(formatted_options))
    
        values_to_select = input("\nEnter values to select (comma separated based on shown value): ").split(",")

        # Set the entered values to the multi-select dropdown
        for value in values_to_select:
            select_content.select_by_value(value.strip())

        # Click the button with id 'view-button-id'
        driver_headless.find_element_by_id('view-button-id').click()
        sleep(2)

        # Locate the tbody element within the table
        tbody = driver_headless.find_element_by_css_selector('#subjects tbody')

        # Fetch all rows from the tbody
        rows = tbody.find_elements_by_tag_name('tr')

        # Randomly select a row
        random_row = random.choice(rows)

        # Get the fourth column from the randomly selected row
        fourth_column = random_row.find_elements_by_tag_name('td')[3]

        # Find the first link within the fourth column
        first_link = fourth_column.find_element_by_tag_name('a')

        # Extract the onclick value from the link
        onclick_value = first_link.get_attribute('onclick')

        # Parse the first parameter using a regular expression
        match = re.search(r'viewFile\((\d+),', onclick_value)

        if match:
            driver_headless.quit()  # Close the headless driver

            driver_visible = webdriver.Chrome(executable_path=ChromeDriverManager().install())

            file_id = match.group(1)
            
            # Construct the desired URL and open it in a new browser tab
            url = f'https://trapeza.iep.edu.gr/public/viewfile.php?id={file_id}&type=subject'
            driver_visible.get(url)

            # Ask the user to press Enter
            input("Press Enter to view the solution...")

            # Use JavaScript to open a new tab
            driver_visible.execute_script("window.open('', '_blank');")

            # Switch to the new window
            driver_visible.switch_to.window(driver_visible.window_handles[1])

            # Construct the desired URL and open it in a new browser window or tab
            url = f'https://trapeza.iep.edu.gr/public/viewfile.php?id={file_id}&type=solution'
            driver_visible.get(url)

            # Here you can introduce a wait or a prompt for user input, ensuring that they have time to see the solution
            input("\nPress Enter once you've seen the solution...")

            # Close the visible driver
            driver_visible.quit()

        # Optionally: Ask the user if they want to continue
        cont = input("\nDo you want to continue? (yes/no): ")
        if cont.strip().lower() != 'yes':
            break

if __name__ == "__main__":
    main()
from time import sleep
from selenium import webdriver
from datetime import datetime

OLD_FOLLOWER_BACKUP_FILENAME = "config/followersBackup.txt"
LOG_FILENAME = "config/log.txt"


class IGBot:
    def __init__(self):
        self.driver = webdriver.Firefox(executable_path="config/geckodriver.exe")

    # login into Instagram
    def login(self, user_name, password):
        # it opens Instagram login web page
        self.driver.get("https://www.instagram.com/" + user_name)

        sleep(1)

        #cookies
        self.driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div[2]/button[1]").click()

        # login operation
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a").click()
        # it inserts username
        self.driver.find_element_by_xpath(
            "/html/body/div[5]/div[2]/div/div[2]/div/div/div[1]/div/form/div[1]/div[1]/div/label/input").send_keys(
            user_name)
        # it inserts password
        self.driver.find_element_by_xpath(
            "/html/body/div[5]/div[2]/div/div[2]/div/div/div[1]/div/form/div[1]/div[2]/div/label/input").send_keys(password)
        # it presses the login button
        self.driver.find_element_by_xpath(
            "/html/body/div[5]/div[2]/div/div[2]/div/div/div[1]/div/form/div[1]/div[3]/button").click()
        sleep(4)

        try:
            self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button").click()
        except Exception:
            pass



        sleep(4)

    # logout from Instagram
    def logout(self):
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/div/button").click()
        sleep(1)
        self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div/button[9]").click()
        sleep(1)

    # it closes the WebDriver connection
    def close(self):
        self.logout()
        self.driver.quit()

    # it returns the followers' list
    def get_follower_list(self):
        return self.get_username_list("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a")

    # it returns the followings' list
    def get_following_list(self):
        return self.get_username_list("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")

    # it opens the whole list of usernames
    def open_the_whole_list(self, xpath):
        self.driver.find_element_by_xpath(xpath).click()
        sleep(1)
        # find the scroll box
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
        # saves the initial scroll box's height
        last_height = self.driver.execute_script("return arguments[0].scrollHeight;", scroll_box)

        sleep(1)
        condition = True
        # it scrolls the box to the end
        while condition:
            # it scrolls the box to the (loaded) end
            self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scroll_box)
            sleep(0.6)
            # it saves the scroll bar's height after scrolling
            new_height = self.driver.execute_script("return arguments[0].scrollHeight;", scroll_box)
            # it compares the two heights in order to understand if the scroll box's end has been reached
            if new_height == last_height:
                condition = False

            last_height = new_height

    # it returns a list of usernames
    def get_username_list(self, xpath):
        # it opens the whole list by a scrolling operation
        self.open_the_whole_list(xpath)

        # it initializes a list of web elements that have a particular class name
        web_elements_list = self.driver.find_elements_by_class_name("FPmhX")
        username_list = []
        # it saves the textual content of every web element into another list
        for user_name in web_elements_list:
            username_list.append(user_name.text + "\n")
        # closes the scrollbox
        self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button").click()

        return username_list


def print_separation_line():
    print("------------------------------------------------------------------------"
          "---------------------------------------")


# this method returns the differences between list1 and list2
# i.e. differences_between_lists(following, followers) -> people you follow who don't follow you back
def differences_between_lists(list1, list2):
    return list(set(list1) - set(list2))


# this method opens a file and updates it with a new list of lines
def update_file(file_name_to_update, new_list):
    file = open(file_name_to_update, "w")
    file.writelines(new_list)
    file.close()


# this method is used to print a message when a FileNotFoundException occurs
def print_when_file_not_found(filename):
    print("File " + "\"" + filename + "\"" + " not found, so I can't tell you who unfollowed/started following "
                                             "you!")
    print("Don't worry, if it's the first time you run this program, it's absolutely normal :)")
    print("Just re run it!")
    print_separation_line()
    sleep(2)


# this method opens a file and handles the FileNotFoundException
def open_file(filename):
    try:
        file = open(filename, "r")
        return file
    except FileNotFoundError:
        print_when_file_not_found(filename)
        return False


# this method checks the condition and then prints the right message
def print_conditioned_message(condition, msg_true, msg_false):
    if condition:
        print(msg_true)
    else:
        print(msg_false)


# this method prints a list element by element
def print_list(list_to_print):
    for element in list_to_print:
        print(element, end='')


# this method prints a list with a message at the end
# if the list is empty, it prints another message
def print_list_with_messages(list_to_print, msg_after_list, msg_after_empty_list):
    print_conditioned_message(list_to_print, msg_after_list, msg_after_empty_list)
    print_list(list_to_print)
    print_separation_line()


# it returns a string that contains the current date and time
def time_stamp():
    dt = datetime.now()
    return dt.strftime("%d-%b-%Y %H:%M:%S")


# it saves in a log file all the unfollowers and new followers and also the saving's date and time
def log_routine(unfollowers_list, new_followers_list):
    try:
        log_file = open(LOG_FILENAME, "a")
    except FileNotFoundError:
        log_file = open(LOG_FILENAME, "w")

    line = "-----------------------------------------------------------------\n"
    log_file.write(line)
    log_file.write(time_stamp() + "\n")

    if unfollower_list:
        log_file.writelines(unfollower_list)
        log_file.write("UNFOLLOWED YOU!\n")
        log_file.write(line)
    if new_followers_list:
        log_file.writelines(new_follower_list)
        log_file.write("STARTED FOLLOWING YOU!\n")
        log_file.write(line)

    log_file.close()


# the beginning of the program

# username and psw are requested
username = input("Insert your Instagram username, phone number or e-mail: ")
psw = input("Insert your Instagram password: ")

print_separation_line()
print("Just wait, I'm working for you!")
print_separation_line()

# an IGBot object is created
ig_bot = IGBot()

# login into Istagram
ig_bot.login(username, psw)

# the lists of followers and following are automatically generated, taking the data directly from Instagram's web page
follower_list = ig_bot.get_follower_list()
following_list = ig_bot.get_following_list()

# it closes the web page
ig_bot.close()

# the file that contains the followers backup is opened
old_follower_backup_file = open_file(OLD_FOLLOWER_BACKUP_FILENAME)

unfollower_list = []
new_follower_list = []

# if the backup file exists, the program finds: the unfollowers' list, the new followers' list and
# all the people who don't follow you back
# if the backup file doesn't exist, the program finds only the people who don't follow you back
if old_follower_backup_file:
    old_follower_backup_list = old_follower_backup_file.readlines()

    unfollower_list = differences_between_lists(old_follower_backup_list, follower_list)
    print_list_with_messages(unfollower_list, "ACCOUNTS THAT UNFOLLOWED YOU:", "NO ONE UNFOLLOWED YOU!")

    new_follower_list = differences_between_lists(follower_list, old_follower_backup_list)
    print_list_with_messages(new_follower_list, "ACCOUNTS THAT STARTED FOLLOWING YOU:", "YOU HAVEN'T NEW FOLLOWERS!")

    old_follower_backup_file.close()

no_follow_back = differences_between_lists(following_list, follower_list)
print_list_with_messages(no_follow_back, "ACCOUNTS THAT DON'T FOLLOW YOU BACK:", "ALL THE PEOPLE THAT YOU ARE FOLLOWING FOLLOW "
                                                                   "YOU BACK!")

# if there are: new followers or unfollowers the log routine is executed
# if the backup file is created in this execution, the log file isn't filled
if old_follower_backup_file and (unfollower_list or new_follower_list):
    log_routine(unfollower_list, new_follower_list)

# if there are: no new followers, no unfollowers or the backup file doesn't exists
# then the backup file is updated/filled
if (not old_follower_backup_file) or unfollower_list or new_follower_list:
    print("Updating the followers' backup file....")
    update_file(OLD_FOLLOWER_BACKUP_FILENAME, follower_list)
    print("DONE!")
    print_separation_line()

input("Press any key to exit!")

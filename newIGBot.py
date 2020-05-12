from time import sleep
from selenium import webdriver


class IGBot:
    def __init__(self):
        self.driver = webdriver.Firefox(executable_path="config/geckodriver.exe")

    # login into Instagram
    def login(self, user_name, password):
        # it opens Instagram login web page
        self.driver.get("https://www.instagram.com/" + user_name)

        sleep(1)

        # login operation
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a").click()
        # it inserts username
        self.driver.find_element_by_xpath(
            "/html/body/div[5]/div/div[2]/div[2]/div/div/div[1]/div/form/div[2]/div/label/input").send_keys(
            user_name)
        # it inserts password
        self.driver.find_element_by_xpath(
            "/html/body/div[5]/div/div[2]/div[2]/div/div/div[1]/div/form/div[3]/div/label/input").send_keys(password)
        # it presses the login button
        self.driver.find_element_by_xpath(
            "/html/body/div[5]/div/div[2]/div[2]/div/div/div[1]/div/form/div[4]/button/div").click()

        sleep(4)

    # logout from Instagram
    def logout(self):
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/div/button").click()
        sleep(1)
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div/button[9]").click()
        sleep(1)

    # it closes the WebDriver connection
    def close(self):
        self.logout()
        self.driver.quit()

    def get_follower_list(self):
        return self.get_username_list("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a")

    def get_following_list(self):
        return self.get_username_list("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")

    # it opens the whole list of usernames
    def open_the_whole_list(self, xpath):
        self.driver.find_element_by_xpath(xpath).click()

        sleep(1)

        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")

        last_height = self.driver.execute_script("return arguments[0].scrollHeight;", scroll_box)
        sleep(1)
        condition = True
        while condition:
            self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scroll_box)
            sleep(0.6)
            new_height = self.driver.execute_script("return arguments[0].scrollHeight;", scroll_box)

            if new_height == last_height:
                condition = False

            last_height = new_height

    # it returns a list of usernames
    def get_username_list(self, xpath):

        self.open_the_whole_list(xpath)

        # it initializes a list of web elements that have a particular class name
        names_links_list = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]").find_elements_by_class_name("FPmhX")


        print(names_links_list)
        username_list = []
        # it saves the textual content of every web element into another list
        for user_name in names_links_list:
            username_list.append(user_name.text + "\n")

        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click()
        print(username_list)
        return username_list


def print_list(list_to_print):
    for element in list_to_print:
        print(element, end='')


ig_bot = IGBot()
ig_bot.login(USERNAME, PSW)

ulist = ig_bot.get_follower_list()
blist = ig_bot.get_following_list()
print_list(ulist)
print("----------------------------------------------------------")
print_list(blist)

ig_bot.close()

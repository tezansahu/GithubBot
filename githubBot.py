from dotenv import load_dotenv
import os
from selenium import webdriver
import time


class GithubBot:
    def __init__(self):
        # dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        dotenv_path = './.env'
        load_dotenv(dotenv_path)
        self.driver = webdriver.Chrome()

        self.login()


    def login(self):
        print("Logging you in...", end="\r", flush=True)
        self.driver.get("https://github.com/login")
        time.sleep(1)
        
        username_input = self.driver.find_element_by_xpath('//*[@id="login_field"]')
        username_input.send_keys(os.environ["GITHUB_USERNAME"])
        pass_input = self.driver.find_element_by_xpath('//*[@id="password"]')
        pass_input.send_keys(os.environ["GITHUB_PASS"])

        signin_btn = self.driver.find_element_by_xpath('//*[@id="login"]/form/div[4]/input[9]')
        signin_btn.click()
        time.sleep(2)

        print("Logged in successfully!")

    def createRepo(self, repo_name, descr=None, readme=False, origin_type="https"):
        print("Creating repository...", end="\r", flush=True)
        new_repo_btn = self.driver.find_element_by_xpath('/html/body/div[4]/div/aside[1]/div[2]/div[1]/div/h2/a')
        new_repo_btn.click()
        time.sleep(2)

        repo_name_input = self.driver.find_element_by_xpath('//*[@id="repository_name"]')
        repo_name_input.send_keys(repo_name)

        if descr != None:
            descr_input = self.driver.find_element_by_xpath('//*[@id="repository_description"]')
            descr_input.send_keys(descr)
        
        if readme:
            readme_check = self.driver.find_element_by_xpath('//*[@id="repository_auto_init"]')
            readme_check.click()
        
        time.sleep(2)

        create_repo_btn = self.driver.find_element_by_xpath('//*[@id="new_repository"]/div[3]/button')
        create_repo_btn.click()

        time.sleep(2)

        if readme:
            clone_btn = self.driver.find_element_by_xpath('//*[@id="js-repo-pjax-container"]/div[2]/div/div[3]/span/get-repo-controller/details/summary')
            clone_btn.click()
            if origin_type == "https":
                url_holder = self.driver.find_element_by_xpath('//*[@id="js-repo-pjax-container"]/div[2]/div/div[3]/span/get-repo-controller/details/div/div/div[1]/div[1]/div/input')
            elif origin_type == "ssh":
                url_holder = self.driver.find_element_by_xpath('//*[@id="js-repo-pjax-container"]/div[2]/div/div[3]/span/get-repo-controller/details/div/div/div[1]/div[2]/div/input')
            
            origin_url = url_holder.get_attribute("value")

        
        else:
            if origin_type == "https":
                https_btn = self.driver.find_element_by_xpath('//*[@id="js-repo-pjax-container"]/div[2]/div/git-clone-help-controller/div[1]/div/div[3]/div/span/form[1]/button')
                https_btn.click()
            elif origin_type == "ssh":
                ssh_btn = self.driver.find_element_by_xpath('//*[@id="js-repo-pjax-container"]/div[2]/div/git-clone-help-controller/div[1]/div/div[3]/div/span/form[2]/button')
                ssh_btn.click()
            
            origin_url = self.driver.find_element_by_xpath('//*[@id="empty-setup-clone-url"]').get_attribute("value")
        
        print("Repository created successfully!")
        
        return origin_url


    def deleteRepo(self, repo_name):
        print("Deleting repository...", end="\r", flush=True)

        self.driver.get("https://github.com/" + os.environ["GITHUB_USERNAME"] + "/" + repo_name)
        time.sleep(2)

        setting_btn = self.driver.find_element_by_xpath('//*[@id="js-repo-pjax-container"]/div[1]/nav/a[5]')
        setting_btn.click()
        time.sleep(2)

        delete_repo_btn = self.driver.find_element_by_xpath('//*[@id="options_bucket"]/div[8]/ul/li[4]/details/summary')
        delete_repo_btn.click()

        delete_repo_inp = self.driver.find_element_by_xpath('//*[@id="options_bucket"]/div[8]/ul/li[4]/details/details-dialog/div[3]/form/p/input')
        delete_repo_inp.send_keys(os.environ["GITHUB_USERNAME"] + "/" + repo_name)

        confirm_delete_btn = self.driver.find_element_by_xpath('//*[@id="options_bucket"]/div[8]/ul/li[4]/details/details-dialog/div[3]/form/button')
        confirm_delete_btn.click()

        time.sleep(2)

        print("Repository deleted successfully!")



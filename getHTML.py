from selenium import webdriver
from time import sleep
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import secrets
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import termcolor
import os
import coloredlogs, logging

def start():
     coloredlogs.install()
     os.system('color')
     logging.info('start')
     options = Options()
     options.add_argument('--headless')
     options.add_argument('--disable-gpu')
     options.add_experimental_option("excludeSwitches", ["enable-logging"])
     options.add_argument('no-sandbox')

      
    
        # import the chrome webdriver
     driver = webdriver.Chrome(executable_path=r'C:\Users\barm\Downloads\chromedriver101\chromedriver', options=options)
     wait = WebDriverWait(driver, 100000000)
        # Open bronto
     driver.get('https://app.bronto.com/mail/message_browser/messages/')
     
     timeout = 10000000
         # Insert UserName
     uname = driver.find_element(By.ID,'Login_username')
     uname.send_keys(secrets.uname)
     logging.info('Entering Username')

        # Insert Password
     password = driver.find_element(By.ID,'Login_password')
     password.send_keys(secrets.password)
     logging.info('Entering Password')

        # Click Login
     login_btn = driver.find_element(By.ID,'Login_submit')
     login_btn.click()
     logging.info('Logging In')

        # Insert security question
     Q = driver.find_element(By.ID, 'Login_VerifySecurityQuestion_answer')
     Q.send_keys(secrets.q)
     logging.info('Entering Security Question')

        # Click Login
     q_btn = driver.find_element(By.ID,'Login_VerifySecurityQuestion_ok')
     q_btn.click()
     logging.info('Logging In')

        # Close the info page
     save_for_later = driver.find_element(By.XPATH, '//*[@id="continue_buttons_block"]/a')
     save_for_later.click()
     logging.info('Closing Info Page')

     runum = 1
     emailNum = 1
     retryNum = 0
     global has_html_code
     has_html_code = False
        # Loop through the messages
     while True:
        try:
            if runum <= 100:
                retryNum = 1
                logging.info('Number of email in page: ' + str(runum))
                logging.info('Number of emails downloaded: ' + str(emailNum))

                
              
                loading =  WebDriverWait(driver, 25).until(EC.invisibility_of_element_located((By.CLASS_NAME,'br_loading')))
               
                # Get the message last edit date
                date = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="flexigrid_0"]/div[2]/div[2]/table/tbody/tr['+str(runum)+']/td[3]/div/div/span'))).text                                       
                logging.info('Date: ' + date)

                # Click the message
                message_link = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="flexigrid_0"]/div[2]/div[2]/table/tbody/tr['+str(runum)+']/td[2]/div/div/a'))).get_attribute('href')
                driver.execute_script("window.open('');")
                                                                             
                logging.info('Clicking Message')

                # Move to new tab
             
                driver.switch_to.window(driver.window_handles[1])
                driver.get(message_link)
                logging.info('Moving to new tab')
                # Assign the message name to a variable
                email_name = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'message_name'))).text
                logging.info('Getting Email Name: ' + email_name)
              

                # Click the edit HTML button
                edit_html = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, 'Edit HTML Version')))
                edit_html.click()
                logging.info('Clicking Edit HTML')

                # Get HTML Code
                has_html_code = True
                html_code = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Mail_MessageEditor_html_body_raw'))).text
                has_html_code = False
                logging.info('Getting HTML Code')

                # Save the HTML Code to file
                with open( 'C:\\Users\\barm\Desktop\Code\BrontoHTML\\' + email_name + '.html', 'w', encoding="utf-8") as f:
                 f.write(html_code)
                f.close()
                logging.info('Saving HTML Code')
                emailNum += 1


                # Go back to the message list
                
                
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                logging.info('Switched to old window')

                # driver.execute_script("window.history.go(-1)")
                # sleep(5)
                # driver.execute_script("window.history.go(-1)")
                # logging.info('Going Back to Message List')
                # sleep(60)
                runum += 1
                logging.info('=========================== Done ===========================')
            else:
            # Moving to next page
            
                WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME,'br_loading')))
                next_btn = WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="flexigrid_0"]/div[2]/div[1]/div[2]/div[3]/a[2]')))
                next_btn.click()
               
                logging.info('Moving to next page')

                runum = 1
                sleep(10)
        

        except NoSuchWindowException as err:
            logging.error(err)
            driver.switch_to.window(window_name=driver.window_handles[0])
            sleep(20)
            continue

        except TimeoutException:
           
            if has_html_code == True:
                logging.error('TimeoutException')
                logging.error('No HTML Skipping')
                runum += 1
                driver.close()
                driver.switch_to.window(window_name=driver.window_handles[0])
               
                continue
            else:
                logging.error('TimeoutException')
                logging.error('Retry Number: ' + str(retryNum))
                driver.refresh()
                WebDriverWait(driver, 80).until(EC.invisibility_of_element_located((By.CLASS_NAME,'br_loading')))
                retryNum += 1
                
                if retryNum >= 5:
                    sleep(20)
                    driver.switch_to.window(window_name=driver.window_handles[1])
                    driver.close()
                    logging.error('Too Many Retries Skipping')
                    retryNum = 1
                    runum += 1
                    sleep(10)
                    continue
                elif NoSuchWindowException:
                    logging.error('NoSuchWindowException')
                    driver.switch_to.window(window_name=driver.window_handles[0])
                    retryNum += 1
                    runum += 1
                    sleep(10)
                    continue
                else:
                    continue
            
        except IndexError as err:
            logging.error(err)
            sleep(20)
            driver.switch_to.window(window_name=driver.window_handles[1])
            driver.close()
            continue

        except UnicodeEncodeError as err:
            logging.error(err)
            sleep(20)
            driver.switch_to.window(window_name=driver.window_handles[1])
            driver.close()
            continue




        except WebDriverException as err:
            logging.error(err)
            sleep(20)
            driver.switch_to.window(window_name=driver.window_handles[1])
            driver.close()
            continue
        

        except FileNotFoundError as err:
            sleep(20)
            driver.switch_to.window(window_name=driver.window_handles[1])
            driver.close()
            logging.error(err)
            retryNum = 1
            runum += 1
            sleep(10)
            continue

        except Exception as err:
          logging.error(err)
          sleep(20)
          driver.switch_to.window(window_name=driver.window_handles[1])
          driver.close()
          continue


       
start()

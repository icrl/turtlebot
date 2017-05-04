from selenium import webdriver  # allows connection to a web browser
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys # allows key input

# Launch the webdriver.  IF CHROMEDRIVER IS MOVED CHANGE THIS PATH
driver = webdriver.Chrome('/home/caitlin/Downloads/chromedriver')
driver.get('http://www.speech.cs.cmu.edu/tools/lmtool-new.html')

# 'Click' the button to upload the .word
driver.find_element_by_name('corpus').click()
driver.find_element_by_css_selector("input[type=\"file\"]").clear()
# Type the path to the .word file. IF THE PATH TO GRAMMAR.WORD IS CHANGED UPDATE THIS PATH
driver.find_element_by_css_selector("input[type=\"file\"]").send_keys("/opt/ros/indigo/share/pocketsphinx/demo/Ourstuff/delivery_dialogue/grammar.word")
# 'Click' the button to submit the .word
driver.find_element_by_css_selector("input[type=\"submit\"]").click()

# Click the link to the .dic
(driver.find_elements_by_partial_link_text('.dic'))[0].click()

# Copy the text of the .dic
text = driver.find_element_by_xpath("/html/body/pre").text;
driver.close()

# Write the new dictionary to turtlebot_dic.dic
dic = open("turtlebot_dic.dic", "w")
dic.write(text)
dic.close()

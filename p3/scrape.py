# project: p3
# submitter: mhashemineja
# partner: none
# hours: 10
import os, zipfile
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

class GraphScraper:
    def __init__(self):
        self.visited = set()
        self.BFSorder = []
        self.DFSorder = []    

    def go(self, node):
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        if node in self.visited:
            return False
        self.visited.add(node)
        for child in self.go(node):
            if self.dfs_search(child):
                return True
        return False
        

    def bfs_search(self, node):
        todo = [node]
        visited_bfs = set()
        visited_bfs.add(node)
        while len(todo) > 0:
            curr = todo.pop(0)
            for child in self.go(curr):
                if not child in visited_bfs:
                    todo.append(child) # add to end
                    visited_bfs.add(child)
        pass

class FileScraper(GraphScraper):

    def go(self, node):
        file = open("file_nodes/"+node+".txt","r").read()
        global indices_new_lines
        indices_new_lines = []
        for i in range(len(file)-1):
            if file[i] == "\n":
                indices_new_lines.append(i)
                
        self.BFSorder.append(file[indices_new_lines[2]-1])
        self.DFSorder.append(file[indices_new_lines[2]+6]) 
        
        children_string = file[indices_new_lines[0]+1:indices_new_lines[1]]
        children = []
        for i in children_string:
            if i != " ":
                children.append(i)
        return children

class WebScraper(GraphScraper):
    def __init__(self, driver=None):
        super().__init__()
        self.driver = driver
        
    def go(self, url):
        self.driver.get(url)
        
        hlinks = []
        for link in self.driver.find_elements_by_tag_name("a"):
            hlinks.append(link.get_attribute("href"))
        
        dfs_button = self.driver.find_element_by_class_name('button-dfs')
        dfs_button.click()
        self.DFSorder.append(dfs_button.text)
        
        bfs_button = self.driver.find_element_by_class_name('button-bfs')
        bfs_button.click()
        self.BFSorder.append(bfs_button.text)
        
        return hlinks
    
    def dfs_pass(self, start_url):
        self.visited.clear()
        self.DFSorder.clear()
        super().dfs_search(start_url)
        
        dfs_password = ''
        for num in self.DFSorder:
            dfs_password += num
            
        return dfs_password
    
    def bfs_pass(self, start_url):
        self.BFSorder.clear()
        self.visited.clear()
        super().bfs_search(start_url)
        
        bfs_password = ''
        for num in self.BFSorder:
            bfs_password += num
            
        return bfs_password
    def protected_df(self, url, password):
        self.driver.get(url)
        for num in range(len(password)):            
            correct_button = self.driver.find_elements_by_tag_name("div")[0].find_elements_by_tag_name("button")[int(password[num])-1]
            correct_button.click()
        prev=self.driver.page_source   
        go_button = self.driver.find_elements_by_tag_name("div")[0].find_elements_by_tag_name("button")[10]
        go_button.click()
        for _ in range(20):
            curr=self.driver.page_source
            time.sleep(1)
            if curr != prev:
                break
        
        prev = self.driver.page_source
        self.driver.find_elements_by_tag_name("button")[0].click()
        time.sleep(3)
        curr = self.driver.page_source
        while prev != curr:
            prev = self.driver.page_source
            self.driver.find_elements_by_tag_name("button")[0].click()
            time.sleep(3)
            curr = self.driver.page_source
        
        return pd.read_html(self.driver.page_source)[0]
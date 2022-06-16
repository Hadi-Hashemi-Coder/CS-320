{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "ba12d312",
   "metadata": {},
   "outputs": [],
   "source": [
    "import os, zipfile\n",
    "import pandas as pd\n",
    "import re\n",
    "\n",
    "class GraphScraper:\n",
    "    def __init__(self):\n",
    "        self.visited = set()\n",
    "\n",
    "    \n",
    "\n",
    "    def go(self, node):\n",
    "        raise Exception(\"must be overridden in sub classes -- don't change me here!\")\n",
    "\n",
    "    def dfs_search(self, node):\n",
    "        if node in self.visited:\n",
    "            return False\n",
    "        self.visited.add(node)\n",
    "        for child in self.go(node):\n",
    "            if self.dfs_search(child):\n",
    "                return True\n",
    "        return False\n",
    "        \n",
    "\n",
    "    def bfs_search(self, node):\n",
    "        todo = [node]\n",
    "        while len(todo) > 0:\n",
    "            curr = todo.pop(0)\n",
    "            print(\"The curr is: \" + curr)\n",
    "            for child in self.go(curr):\n",
    "                print(child)\n",
    "                if not child in self.visited:\n",
    "                    todo.append(child) # add to end\n",
    "                    self.visited.add(child)\n",
    "        pass\n",
    "\n",
    "class FileScraper(GraphScraper):\n",
    "    def __init__(self):\n",
    "        super().__init__()\n",
    "        self.BFSorder = []\n",
    "        self.DFSorder = []\n",
    "        self.nodes = {}\n",
    "        for i in range(7):\n",
    "            self.nodes[str(i+1)]=open(\"file_nodes/\"+str(i+1)+\".txt\", \"r\")\n",
    "\n",
    "        \n",
    "    def go(self, node):\n",
    "        file = str(self.nodes[node].read())\n",
    "        global indices_new_lines\n",
    "        indices_new_lines = []\n",
    "        for i in range(len(file)-1):\n",
    "            if (file[i] + file[i+1]) == file[3:5]:\n",
    "                indices_new_lines.append(i)\n",
    "                \n",
    "        print(\"file looks like this: \" + file)\n",
    "#         self.BFSorder.append(file[indices_new_lines[2]-1])\n",
    "#         self.DFSorder.append(file[indices_new_lines[3]-1]) \n",
    "        \n",
    "        children_string = file[indices_new_lines[0]+2:indices_new_lines[1]]\n",
    "        children = []\n",
    "        for i in children_string:\n",
    "            if i != \" \":\n",
    "                children.append(i)\n",
    "        return children"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
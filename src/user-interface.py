"""
This file will create the user interface for the predictive
analysis engine
"""
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd
import subprocess
import csv
import time
import os
import yfinance as yf
import importlib as il
stockFetcher = il.import_module("stock-fetcher")

class LabeledPredictiveAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Predictive Analysis Engine")
        self.root.geometry("800x550")

        ## Main Layout

        # Left Panel for inputs
        leftPanel = tk.Frame(self.root, bd=1, relief="solid")
        leftPanel.place(relx=0.05, rely=0.1, relwidth=0.4, relheight=0.8)

        # Right Panel for graph placeholder
        self.rightPanel = tk.Frame(self.root, bd=1, relief="solid")
        self.rightPanel.place(relx=0.5, rely=0.1, relwidth=0.45, relheight=0.8)

        ## Left panel

        # Stock Search Label and Input
        stockLabel = tk.Label(leftPanel, text="Stock Search (e.g. AMZN, AAPL, GOOG)")
        stockLabel.place(relx=0.1, rely=0.10)
        
        searchFrame = tk.Frame(leftPanel)
        searchFrame.place(relx=0.1, rely=0.15, relwidth=0.8, height=30)
        
        self.searchEntry = tk.Entry(searchFrame)
        self.searchEntry.pack(side="left", fill="both", expand=True)
        
        self.searchButton = tk.Button(searchFrame, text="🔎", command=self.searchStock) # not vibecoded i swear
        self.searchButton.pack(side="right", fill="y")

        # Lag Order Label and Input
        lagLabel = tk.Label(leftPanel, text="Lag Order (>=0, recommended 3-7)")
        lagLabel.place(relx=0.1, rely=0.30)

        self.lagEntry = tk.Entry(leftPanel)
        self.lagEntry.place(relx=0.1, rely=0.35, relwidth=0.8, height=30)

        # Price History Label and Input
        historyLabel = tk.Label(leftPanel, text="Price History (days)")
        historyLabel.place(relx=0.1, rely=0.50)

        self.historyEntry = tk.Entry(leftPanel)
        self.historyEntry.place(relx=0.1, rely=0.55, relwidth=0.8, height=30)

        # Action Button
        runButton = tk.Button(leftPanel, text="Run Analysis", command=self.runSimulation)
        runButton.place(relx=0.1, rely=0.75, relwidth=0.8, height=50)

        ## Right panel
        self.fig = Figure(figsize=(5,4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        ## Add canvas for graph
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.rightPanel)
        canvasWidget = self.canvas.get_tk_widget()
        canvasWidget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        ## Add toolbar to allow zooming (lots of datapoints so required for this project)
        toolbar = NavigationToolbar2Tk(self.canvas, self.rightPanel)
        toolbar.update()
        toolbar.pack(side=tk.TOP, fill=tk.BOTH, expand=False)


    def searchStock(self):
        ## Get stock name
        stockName = str(self.searchEntry.get())

        valid = stockFetcher.checkStockValidity(stockName)
        print(valid)

        ## Check validity
        if valid:
            self.searchButton.config(text="Valid")
        else:
            self.searchButton.config(text="Invalid")

        self.root.after(1000, lambda: self.searchButton.config(text="🔎"))

    def runSimulation(self):
        ## Get variables from entry boxes
        self.stockSearch = str(self.searchEntry.get())
        self.lagOrder = str(self.lagEntry.get())
        self.priceHistory = str(self.historyEntry.get())

        ## Validation
        try:
            if int(self.lagOrder) < 1:
                raise ValueError("Lag order must be greater than or equal to 1")
                return 0
        except:
            raise TypeError("Lag order must be an integer")
            return 0

        try:
            if int(self.priceHistory) < 2:
                raise ValueError("Price history must be greater than or equal to 2")
                return 0
        except:
            raise TypeError("Price history must be an integer")
            return 0

        if int(self.priceHistory) <= 2*int(self.lagOrder):
            raise Exception("Price history must be more than 2x larger than lag order")
            return 0
        

        ## Fetch the stock and pack into CSV
        stockFetcher.fetchStockData(self.stockSearch, self.priceHistory)
        
        ## get directory path for data.csv
        srcDir = os.path.dirname(os.path.abspath(__file__)) # get the path for the src file
        rootDir = os.path.dirname(srcDir)                   # go up to root directory
        dataDir = os.path.join(rootDir, "data")             # drop down into data folder
        self.dataCSVPath = os.path.join(dataDir, "data.csv")

        ## Get last actual value for C++ predictive engine parameters
        with open(self.dataCSVPath, "r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            self.lastActualPrice = rows[-1]["close"]
        
        with open(self.dataCSVPath, "r") as file:
            reader = csv.DictReader(file)
            self.pricesArr = [float(row['close']) for row in reader] # Also grab all closing prices for later
        
        self.exeFile = os.path.join(srcDir, "predictive-analysis-engine.exe")

        result = subprocess.run(
            [self.exeFile, self.lagOrder, self.dataCSVPath, self.lastActualPrice],
            capture_output=True,
            text=True,
            check=True
        )
        
        self.predictionsArray = result.stdout.strip().split("y")[1].split("\n")[1:-1]
        self.predictionsArr = []
        for price in self.predictionsArray:
            self.predictionsArr.append(float(price))


        self.fullPricesArr = self.pricesArr + self.predictionsArr
        print(self.fullPricesArr)

        self.xarr = []
        for i in range(len(self.fullPricesArr)):
            self.xarr.append(i)

        splitIndex = -5

        self.fig.delaxes(self.ax)
        self.ax = self.fig.add_subplot(111)

        self.ax.plot(self.xarr[:splitIndex+1], self.fullPricesArr[:splitIndex+1], color="black", linestyle="-")
        self.ax.plot(self.xarr[splitIndex:], self.fullPricesArr[splitIndex:], color="blue", linestyle=":")
        self.ax.set_title(str(yf.Ticker(self.stockSearch).info.get("longName")))
       
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = LabeledPredictiveAnalysisApp(root)
    root.mainloop()
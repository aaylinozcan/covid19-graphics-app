import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
import pandas as pd
import numpy as np
import requests
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import json
import os.path
from os import path
from operator import itemgetter



countries = requests.get("https://api.covid19api.com/countries")
datacountries = countries.json()
with open("Countries.json","w+") as fp:
    json.dump(datacountries,fp)

countrylist = list(map(itemgetter('Country'), datacountries))



class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(side=LEFT)
        self.create_widgets()
        self.createDataList()

    def create_widgets(self):
        self.search_var = StringVar()
        self.search_var.trace("w", lambda name, index, mode: self.update_country_listbox())
        self.entry = Entry(self, textvariable=self.search_var, width=30)
        self.lbox = Listbox(self, width=30, height=15,exportselection=0)
        self.lbox2 = Listbox(self, width=30, height=8,exportselection=0 )
        self.L1 = Label(self, text="Search")
        self.L2 = Label(self, text="Countries")
        self.L3 = Label(self, text="Data Types")
        self.button1 = Button(self, text="Draw", command=self.getCurseSelection)

        self.fig = Figure(figsize=(10, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        toolbar = NavigationToolbar2Tk(self.canvas, root)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=1)

        self.entry.grid(row=1, column=1, )
        self.lbox.grid(row=2, column=1, )
        self.L1.grid(row=1, column=0,)
        self.L2.grid(row=0, column=1,)
        self.L3.grid(row=3, column=1,)
        self.lbox2.grid(row=4, column=1,)
        self.button1.grid(row=5, column=1,)

        self.update_country_listbox()

    def update_country_listbox(self):

        search_term = self.search_var.get()
        countrylist.sort()
        self.lbox.delete(0, END)
        for item in countrylist:
            if search_term.lower() in item.lower():
                self.lbox.insert(END, item)

    def createDataList(self):
        datalist = ["Confirmed", "Deaths", "Recovered", "Active", "Confirmed-Daily", "Deaths-Daily",
                    "Recovered-Daily", "Active-Daily"]
        for item in datalist:
             self.lbox2.insert(END, item)

    def getCurseSelection(self):
        fp1 = open("Countries.json","r")
        datacountries = json.load(fp1)
        a = self.lbox.get(ANCHOR)
        b = self.lbox2.get(ANCHOR)
        c = (datacountries[next((i for i, item in enumerate(datacountries) if item["Country"] == a), None)]['Slug'])
        d = b.split('-')[0]
        self.getData(c)
        if len(b) == len(d):
            self.drawChart(b,c)
        else:
            self.drawBarChart(d,c)

    def drawChart(self,datatype, country):
        fout = open('{}.json'.format(country), 'r')
        a = json.load(fout)
        totaldata = list(map(itemgetter(datatype), a))
        dates = list(map(itemgetter('Date'), a))
        self.fig.add_subplot(111).plot(dates, totaldata)
        self.canvas.draw()
        self.fig.clf()

    def drawBarChart(self,datatype, country):
        dailydata=[]
        fout = open('{}.json'.format(country), 'r')
        a = json.load(fout)
        totaldata = list(map(itemgetter(datatype), a))
        dailydata.append(totaldata[0])
        for i in range(len(totaldata)):
            if i < (len(totaldata)-1):
                dailydata.append((totaldata[i+1])-totaldata[i])
        dates = list(map(itemgetter('Date'), a))

        self.fig.add_subplot(111).bar(dates,dailydata)
        self.canvas.draw()
        self.fig.clf()


    def getData(self,x):
        newData = requests.get(modifyURL(x))

        if (path.exists('{}.json'.format(x))):
            with open('{}(2).json'.format(x),'w+') as fout2:
                json.dump(newData.json(), fout2)
                fout2.close()
            fout2 = open('{}(2).json'.format(x), 'r')
            fout = open('{}.json'.format(x), 'r')
            a = json.load(fout)
            b = json.load(fout2)
            if (len(a) == len(b)):
                fout2.close()
                os.remove('{}(2).json'.format(x))
                fout.close()
                print("Data Güncel")
            else:
                fout.close()
                fout2.close()
                os.remove('{}.json'.format(x))
                os.rename('{}(2).json'.format(x),'{}.json'.format(x))
                print("Data Güncellendi")
        else:
            with open('{}.json'.format(x),"w+") as fout3:
                json.dump(newData.json(), fout3)

def modifyURL(country):
    url = ("https://api.covid19api.com/dayone/country/{}".format(country))
    return url


root = Tk()

root.title('Cov19 Chart Maker')
app = Application(master=root)

app.mainloop()
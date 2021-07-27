# BikeDashboardPlus

## Description

Over my spring break in April 2021, I made a bike dashboard ([Project description](https://create.arduino.cc/projecthub/jonathanhliu21/a-dashboard-for-a-bike-unfinished-6dc0cb), [Github Repo](https://github.com/jonyboi396825/BikeDashboard)) using an Arduino Nano, an LCD screen, and a GPS. That design had many problems. I could not put that many features on it because the Nano did not have much memory. It was slow and updated every 2 seconds. The LCD screen was very big and captured attention, which may have gotten my bike stolen. Because of these problems, I wanted a new design.

This design includes a Raspberry Pi Zero connected to an Arduino Nano, which should fix the memory issues. The slowness can be solved by getting the data in a separate thread, so it wouldn't slow down the program. I replaced the big LCD with a 128x64 OLED and a LED matrix that will be hidden (I have not made a case for this yet), making it more inconspicuous. Lastly, I made a website that plots the tracked route on a map.

## How it works

## Problems I run into 

## Problems that still occur

## Upgrade ideas

## Making this project yourself

[Go here](docs/pages/make_yourself.md)

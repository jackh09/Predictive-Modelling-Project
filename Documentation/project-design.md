# Design
## Introduction
This document will be the planning phase of this project, allowing me to sketch out some of the algorithms and elements of the project.

## Top-down Structure Diagram
I have created a top down structure diagram to allow me to see the whole program at a glance:

![Top-down structure diagram](/Documentation/Assets/predictive-modelling-project-top-down-flowchart.png)

I have split the program into 3 main sections:
1. The Python function that fetches and formats the stock data
2. The Python user interface that allows the user to interact with the program and view the results
3. The C++ predictive analysis engine

## UI Design
I have designed the UI in a simple and intuitive way as there isn't really much user input needed:

![UI design](/Documentation/Assets/predictive-modelling-project-ui-design.png)

As you can see, the search function, lag order, price history length and run button are on the left and the graph will go on the right.

## Variables, Data Structures and Validation

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

## Variables
I will define my key variables here. I will provide the data type that it satisfies and a short description of what the variable does.

### Fetching and Formatting Stock Data
| Name              | Data Type        | Function                            |
| ----------------- | ---------------- | ----------------------------------- |
| stockTicker       | yfinance.ticker  | allows stock data to be fetched     |

### User Interface

| Name              | Data Type        | Function                            |
| ----------------- | ---------------- | ----------------------------------- |
| searchQuery       | string           | supplies ticker with valid stock    |
| lagOrder          | int              | specifies lag order for AR model    |
| historyLength     | int              | how many days back data is found    |

### Predictive Analysis Engine
| Name              | Data Type        | Function                            |
| ----------------- | ---------------- | ----------------------------------- |
| prediction        | double           | holds the result of the AR model    |

## Data Structures
I will define my key data structures here. Because C++ data structures can only hold one type of data, I will also define the data type to be stored in each structure. I will also include the structure type and a short description of what the data structure does.

### Fetching and Formatting Stock Data
| Name              | Data Type        | Structure Type        | Function                                        |
| ----------------- | ---------------- | --------------------- | ----------------------------------------------- |
| df                | float            | pandas dataframe      | stores stock prices and returns in known format |
| data.csv          | float            | csv file              | stores formatted df in csv file and format      |

### User Interface
There are no data structures that need to be defined here

### Predictive Analysis Engine
| Name              | Data Type              | Structure Type        | Function                                                 |
| ----------------- | ---------------------- | --------------------- | -------------------------------------------------------- |
| returns           | double                 | std::vector           | stores returns in a c++ compatible format                |
| X                 | double                 | std::vector           | stores autocorrelation matrix                            |
| y                 | double                 | std::vector           | stores target vector                                     |
| tempCSV           | double                 | csv file              | stores historic + prediction data for subsequent AR sims |

## Validation
I will plan out some validation here to avoid fatal program errors.

### Fetching and Formatting Stock Data
| Problem                                         | Action                                           | Implementation                           |
| ----------------------------------------------- | ------------------------------------------------ | ---------------------------------------- |
| Searching for invalid stocks could cause errors | Check that the searchQuery matches a known stock | yfinance.search                          |
| Asset price of 0 causes $\frac{x}{0}$ error     | Ensure division by 0 is unable to take place     | wrap daily returns section in try:except |

### User Interface
| Problem                                          | Action                                             | Implementation                           |
| ------------------------------------------------ | -------------------------------------------------- | ---------------------------------------- |
| Attempts to start sim with incomplete parameters | Ensure user completes all fields before continuing | check if all boxes have valid values     |

### Predictive Analysis Engine
| Problem                                          | Action                                             | Implementation                              |
| ------------------------------------------------ | -------------------------------------------------- | ------------------------------------------- |
| Attempts to invert a singular matrix             | Check determinant != 0                             | calculate determinant: if == 0 return error |

## Testing Plan
To evaluate the program, I will test the inputs of the software using the test table below:
Test ID | Testing Category | Description / Purpose | Input Data | Expected Result | Pass/Fail |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1-1** | Normal | Fetch a valid stock ticker. | `stockTicker = "AAPL"` | Downloads history and creates `data.csv`. | |
| **1-3** | Erroneous | Search for invalid ticker string. | `stockTicker = "XYZ_INVALID"` | Halts process and shows "Ticker not found" error. | |
| **2-1** | Normal | Generate daily returns. | Standard price data series. | Pandas populates `dailyReturn` column accurately. | |
| **2-3** | Erroneous | Handle zero price change day. | Today: 150.00, Yesterday: 150.00 | Calculates `0.00` return without math crashes. | |
| **3-1** | Normal | Parse CSV data in C++. | Properly formatted `data.csv`. | C++ stream loads data into `std::vector` cleanly. | |
| **4-2** | Boundary | Test minimal AR lag limit ($p=1$). | `lagOrder = 1` | Engine builds 1D matrix and solves 1 coefficient. | |
| **5-2** | Boundary | Test maximal AR lag limit ($p=7$). | `lagOrder = 7` | Engine builds $7 \times 7$ matrix and solves 7 weights. | |
| **5-3** | Erroneous | Input negative or zero lag order. | `lagOrder = -3` or `0` | UI blocks submission with validation message. | |
| **6-1** | Normal | Invert matrix via OLS algebra. | Non-singular matrix $X$. | Gauss-Jordan algorithm solves $(X^T X)^{-1}$. | |
| **6-3** | Erroneous | Attempt singular matrix inversion. | Linearly dependent inputs. | Engine catches zero determinant and exits safely. | |
| **7-1** | Normal | Execute 5-day iterative forecast. | Valid weights and data vector. | Engine outputs 5 sequential predicted returns. | |
| **8-1** | Normal | Convert returns back to prices. | Last Price: 100, Predicted Return: 0.02 | Outputs price scalar of `102.00` to `tempCSV`. | |
| **9-1** | Normal | Verify engine execution speed. | Benchmark dataset run. | Algorithm processing completes in `< 50ms`. | |
| **9-3** | Erroneous | Run sim with missing fields. | Empty input fields. | Run button locks or alerts user to fill fields. | |
## Final Note
With that, the project design stage is complete. The next phase of development can be found in [project-development.md](/Documentation/project-development.md), which is my devlog.

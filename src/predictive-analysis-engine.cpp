#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <iomanip>

std::vector<double> readCSVReturns(const std::string &filePath) // Takes a file path as an input
{
    std::vector<double> returns;  // Create returns vector
    std::ifstream file(filePath); // Open CSV

    // Checks if file can be opened
    if (!file.is_open())
    {
        std::cerr << "Could not open " << filePath << "\n";
        return returns;
    }

    std::string line; // Temp variable to read each line in CSV

    // Remove first line (headers)
    if (std::getline(file, line))
    {
    }

    // Read each line in the file
    while (std::getline(file, line))
    { // While there is still data

        std::stringstream ss(line);               // Allows us to read each line as a string
        std::string dateStr, closeStr, returnStr; // Temp variables to hold each value in the row

        if ( // Read off all values and assign them to temp vars
            std::getline(ss, dateStr, ',') &&
            std::getline(ss, closeStr, ',') &&
            std::getline(ss, returnStr, ','))
        {
            // Convert returnStr to double - could cause crashing so wrapped in try:catch
            try
            {
                double returnValue = std::stod(returnStr); // String to double
                returns.push_back(returnValue);            // Add to vector
            }
            catch (const std::exception &e)
            {
                std::cerr << "Data error. Closing file.\n";

                file.close();
                return std::vector<double>(); // Return empty vector
            }
        }
    }

    file.close(); // Prevent memory leaks
    return returns;
}

std::vector<std::vector<double>> transposeMatrix(const std::vector<std::vector<double>> &matrix)
{
    if (matrix.empty())
    {
        return {};
    }

    // Define size of matrix
    size_t rows = matrix.size();
    size_t cols = matrix[0].size();

    // Create an empty transposed matrix
    std::vector<std::vector<double>> transposed(cols, std::vector<double>(rows, 0.0));

    // Flip along leading diagonal
    for (size_t i = 0; i < rows; ++i)
    {
        for (size_t j = 0; j < cols; ++j)
        {
            transposed[j][i] = matrix[i][j]; // Flip values
        }
    }
    return transposed;
}

void outputMatrix(const std::vector<std::vector<double>> &matrix)
{
    if (matrix.empty())
    {
        std::cout << "Matrix empty";
        return;
    }

    size_t rows = matrix.size();
    size_t cols = matrix[0].size();

    for (size_t i = 0; i < rows; ++i)
    {
        for (size_t j = 0; j < cols; ++j)
        {
            std::cout << matrix[i][j] << " ";
        }
        std::cout << "\n";
    }
}

// Invert an n x n matrix using Gauss-Jordan elimination (Turn [A|I] into [I|A^-1])
std::vector<std::vector<double>> invertMatrix(const std::vector<std::vector<double>> &matrix)
{
    // Return empty matrix back if empty
    if (matrix.empty())
    {
        return {};
    }

    // Calculate size of matrix
    size_t n = matrix.size();

    // Create augmented matrix
    std::vector<std::vector<double>> aug(n, std::vector<double>(2 * n, 0.0));
    for (size_t i = 0; i < n; ++i)
    { // Loop through rows
        for (size_t j = 0; j < n; ++j)
        { // Loop through columns
            aug[i][j] = matrix[i][j];
        }
        aug[i][i + n] = 1.0;
    }

    // Apply Gauss-Jordan elimination to turn A into I
    for (size_t i = 0; i < n; ++i)
    {
        double pivot = aug[i][i];
        if (std::abs(pivot) < 1e-9)
        {
            std::cerr << "Matrix is singular and cannot be inverted" << std::endl;
            return {};
        }
        for (size_t j = 0; j < 2 * n; ++j)
        {
            aug[i][j] /= pivot; // Loop through columns and divide by pivot (get closer to identity matrix)
        }
        for (size_t k = 0; k < n; ++k)
        {
            if (k != i)
            {                              // Skip pivot row
                double factor = aug[k][i]; // Find which value needs to be 0
                for (size_t j = 0; j < 2 * n; ++j)
                { // Subtract appropriate values to produce identity matrix
                    aug[k][j] -= aug[i][j] * factor;
                }
            }
        }
    }
    std::vector<std::vector<double>> inverse(n, std::vector<double>(n, 0.0)); // Create n x n matrix to fill out inverted values
    for (size_t i = 0; i < n; ++i)
    {
        for (size_t j = 0; j < n; ++j)
        {
            inverse[i][j] = aug[i][j + n]; // Get values from right side of matrix (A^-1)
        }
    }
    return inverse;
}

// Multiply an i x j matrix by a j x k matrix
std::vector<std::vector<double>> multiplyMatrices(const std::vector<std::vector<double>> &matrixA, const std::vector<std::vector<double>> &matrixB)
{
    size_t rowsA = matrixA.size();
    size_t colsA = matrixA[0].size();
    size_t colsB = matrixB[0].size();

    std::vector<std::vector<double>> result(rowsA, std::vector<double>(colsB, 0.0));

    for (size_t i = 0; i < rowsA; ++i)
    {
        for (size_t j = 0; j < colsB; ++j)
        {
            for (size_t k = 0; k < colsA; ++k)
            {
                result[i][j] += matrixA[i][k] * matrixB[k][j];
            }
        }
    }
    return result;
}

int main(int argcount, char *argvals[])
{
    // Get lag order
    if (argcount < 3)
    {
        std::cerr << "Missing arguments";
        return 1;
    }

    int lagOrder = std::stoi(argvals[1]);
    std::string dataCSVPath = argvals[2];

    // Create returns vector from CSV
    std::vector<double> returns = readCSVReturns(dataCSVPath);

    // Output returns for debugging
    std::cout << "Returns from CSV:" << std::endl;
    for (size_t i = 0; i < std::min(returns.size(), static_cast<size_t>(3)); ++i)
    {
        std::cout << returns[i] << std::endl;
    }

    // Create autocorrelation and target matrices
    std::vector<double> yMatrix;
    std::vector<std::vector<double>> X;

    for (size_t i = lagOrder; i < returns.size(); i++)
    {                                  // Start from lag order (base off y matrix)
        yMatrix.push_back(returns[i]); // Start at i+2

        std::vector<double> row; // Create a row for X matrix

        for (int j = lagOrder; j >= 1; j--)
        { // Add indexes i to i+lagOrder
            row.push_back(returns[i - j]);
        }

        X.push_back(row); // Add the row to matrix X
    }

    // Convert y from 1D list to 2D matrix (n x 1) for multiplicative purposes
    std::vector<std::vector<double>> y;
    for (double val : yMatrix)
    { // Loops through all values in yMatrix
        y.push_back(std::vector<double>({val}));
    }

    // Plug in and calculate PHI = (XT*X)^-1 * (XT * Y)
    std::vector<std::vector<double>> XT = transposeMatrix(X);

    // (XT * X)
    std::vector<std::vector<double>> XTX = multiplyMatrices(XT, X);

    // (XTX)^-1
    std::vector<std::vector<double>> XTXInverse = invertMatrix(XTX);

    // (XT * Y)
    std::vector<std::vector<double>> XTy = multiplyMatrices(XT, y);

    // Full equation
    std::vector<std::vector<double>> equationResult = multiplyMatrices(XTXInverse, XTy);

    // Output final weights for debugging
    std::cout << "Prediction Weights (Phi):" << std::endl;
    for (size_t i = 0; i < equationResult.size(); ++i)
    {
        std::cout << "Phi " << (i + 1) << ": " << std::fixed << std::setprecision(8) << equationResult[i][0] << std::endl;
    }

    return 0;
}

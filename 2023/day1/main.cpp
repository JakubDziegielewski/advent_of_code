#include <iostream>
#include <fstream>
#include <string>

int main()
{
    std::ifstream input("input.txt");
    int result = 0;
    std::string line;
    while (input.good())
    {
        try
        {
            getline(input, line, '\n');
            char first_digit = ' ';
            char last_digit = ' ';
            for (size_t i = 0; i < line.length(); i++)
            {
                if (first_digit == ' ' && isdigit(line[i]))
                {
                    first_digit = line[i];
                }
                if (last_digit == ' ' && isdigit(line[line.length() - 1 - i]))
                {
                    last_digit = line[line.length() - 1 - i];
                }
                if (first_digit != ' ' && last_digit != ' ')
                {
                    break;
                }
            }
            std::string s;
            s += first_digit;
            s += last_digit;
            int number = stoi(s);
            result += number;
        }
        catch (const std::exception &e)
        {
            std::cerr << "Invalid data" << '\n';
            std::cerr << e.what() << '\n';
        }
    }
    std::cout << result << std::endl;
}
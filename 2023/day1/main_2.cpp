#include <iostream>
#include <fstream>
#include <string>

int main()
{
    std::string digits[10] = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};
    char d[10] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'};
    std::ifstream input("input.txt");
    int result = 0;
    std::string line;
    size_t counter = 0;
    while (input.good())
    {
        try
        {
            getline(input, line, '\n');
            char first_digit = ' ';
            char last_digit = ' ';
            for (size_t i = 0; i < line.length(); i++)
            {
                if (isdigit(line[i]))
                {
                    if (first_digit == ' ')
                    {
                        first_digit = line[i];
                    }
                    last_digit = line[i];
                }
                else
                {
                    for (size_t j = 0; j < 10; j++)
                    {
                        if (i + digits[j].length() <= line.length())
                        {
                            std::string sub = line.substr(i, digits[j].length());
                            if(sub == digits[j])
                            {
                                if (first_digit == ' ')
                                {
                                    first_digit = d[j];
                                }
                                last_digit = d[j];
                            }
                        }
                    }
                }
            }
            std::string s;

            s += first_digit;
            s += last_digit;
            std::cout << s << std::endl;
            int number = stoi(s);
            result += number;
        }
        catch (const std::exception &e)
        {
            std::cout << counter << std::endl;
            std::cerr << "Invalid data" << '\n';
            std::cerr << e.what() << '\n';
            exit(1);
        }
        counter++;
    }
    std::cout << result << std::endl;
}
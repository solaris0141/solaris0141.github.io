#include <string>
#include <ctime>
#include <algorithm>
#include <iostream>
using namespace std;

// Function to randomize the order of elements in the array
void randomizeArray(int arr[], int size) {
    srand(time(0)); // Seed for random number generator
    random_shuffle(arr, arr + size); // Shuffle the array
}

string Ciao(string input, int n[6]){
    int code;
    int nsize=6;
    string output;
    for (int i = 0; i < input.size();i++)
    {
        if(input[i]==' '){output+=' ';continue;}
        code = input[i]-'a';
        for (int j = 0; j < nsize;j++)
        {
            code = (code + n[j]) % 26;
        }

        if(code%2==0)   code++;else code--;  // Reflector: if even, add 1; if odd, subtract 1.

        for (int j = nsize-1; j >=0;j--)
        {
            code = code - n[j];
            if(code<0)code=26+code;
        }

        n[0]++;
        for (int j = 0; j < nsize-1; j++)
        {
            if (n[j]>=26)
            {
                n[j + 1]++;
                n[j] = 0;
            }
        }
        n[nsize-1] = n[nsize-1] % 26;
        output += code+'a';
    }
    return output;
}

int main()
{
    string secret="justexample";
    string flag="IBOH24{"+secret +"}";
    // Define 6 rotors from german 
    // hint: 1 - 26 
    int n[6] = {1, 2, 3, 4, 5, 6 }; // just example  
    randomizeArray(n, 6);
    string cipher=Ciao(secret,n);
    cout <<"cipher:"<< cipher<< endl;
    cout << "flag:"<<flag<<endl;
    return 0;
}

//  cipher:sijrknpjtmjjfdmhhlb
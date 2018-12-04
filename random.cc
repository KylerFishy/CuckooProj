#include <ctime>
#include <cstdlib>
#include <iostream>
#include <fstream>
using namespace std;

int main() {
  ofstream myfile;
  srand(time(NULL));
  myfile.open ("keys2.txt");
  for(int i=0; i<10;i++) myfile <<rand() <<endl;
  myfile.close();

   return 0;
}

#include <iostream>
#include <fstream>
#include <string>
#include <regex>
#include <cmath>

#include "AVLTree.h"
#include "Vector.h"

using namespace std;

const std::regex re(R"([\s|,|;|(|)]+)");

string filename = "code.cpp";
string outputFile = "halstead.txt";

int n1;
int n2;
int N1;
int N2;

bool isComment[100000];

void initialize (){
	n1 = 0;
	n2 = 0;
	N1 = 0;
	N2 = 0;
}

int countComment (){
	string lineTemp;
	int lineNum = 0;
	int index = 0;
	int numOfComment = 0;
	bool multiLineComment =false;

	ifstream fin;
	fin.open(filename);
	if (!fin)
    {
       std::cout << "Can't open the input file successfully." << endl;
       return 1;
    }

    getline(fin, lineTemp);

	while (!fin.eof())
    {
    	isComment[lineNum] = false;
    	//std::cout<<endl<<lineNum<<endl;

    	for (index=0; index < lineTemp.size(); index++)
    	{
    		if(multiLineComment == false && lineTemp[index]!='/' && lineTemp[index]!=' '){
    			isComment[lineNum] = false;
    			break;
    		}
    		else if(multiLineComment == true && lineTemp[index]=='*' && lineTemp[index+1]=='/'){
    			isComment[lineNum] = true;
    			multiLineComment = false;
    			break;
    		}
    		else if (lineTemp[index]=='/' && lineTemp[index+1]=='*')
    		{
    			isComment[lineNum] = true;
    			multiLineComment = true;
    			break;
    		}
    		else if (multiLineComment == true){
    			isComment[lineNum] = true;
    		}
    		else if (lineTemp[index]=='/' && lineTemp[index+1]=='/')
    		{
    			isComment[lineNum] = true;
    			break;	
    		}
    		else{

    		}

    	}

    	lineNum ++;
    	getline(fin, lineTemp);
    }

    for (index = 0; index < lineNum; index++)
    {
    	if (isComment[index]){
    		numOfComment++;
    		//std::cout<<index+1<<" ";
    	}
    }

    //std::cout<<"\n Number of Line: " << lineNum << "\n Number of Comment: " << numOfComment << endl;


    fin.close();
	return 0;
}

std::vector<std::string> tokenize( 
                     const std::string str, 
                          const std::regex re) 
{ 
    std::sregex_token_iterator it{ str.begin(),  
                             str.end(), re, -1 }; 
    std::vector<std::string> tokenized{ it, {} }; 
  
    // Additional check to remove empty strings 
    tokenized.erase( 
        std::remove_if(tokenized.begin(),  
                            tokenized.end(), 
                       [](std::string const& s) { 
                           return s.size() == 0; 
                       }), 
        tokenized.end()); 
  
    return tokenized; 
}

int findOperands(){
	ifstream fin;
	fin.open(filename);
	if (!fin)
    {
       std::cout << "Can't open the input file successfully." << endl;
       return 1;
    }

	string searchPattern = "(bool[* ]*)([a-zA-Z0-9_]+)|(int[* ]*)([a-zA-Z0-9_]+)|(float[* ]*)([a-zA-Z0-9_]+)|(char[* ]*)([a-zA-Z0-9_]+)|(double[* ]*)([a-zA-Z0-9_]+)|long|short|signed|unsigned|void";

	smatch m;
	regex reg1(searchPattern);

	string lineTemp;
	int lineNum = 0;

	AvlTree<string> uniqueOperands;
	int numUniqueOperands = 0;
	int numTotalOperands = 0;
	Vector<int> operandLocations;

	getline(fin, lineTemp);

	while (!fin.eof())
    {
        while (regex_search(lineTemp, m, reg1) && !isComment[lineNum])
        {
            bool found = false;
            int iTemp = 0;

            for (int i = 1; i < m.size();i ++)
            {
                if (m[i] != "")
                {
                    operandLocations.add(lineNum);
                    found = true;
                    iTemp = i;
                    break;
                }
            }

            if (found)
            {
            	//std::cout<<endl<<lineTemp;
            	const std::vector<std::string> tokenized =  
                           tokenize(lineTemp, re); 
    
    			for (std::string token : tokenized){
    				numTotalOperands++;

    				int pos = token.find('=',0);
    				if (pos==0) continue;
    				if(pos>0)token=token.substr(0,pos); 
    				//std::cout << token << std::endl;
    				if (!uniqueOperands.contains(token))
                	{
                    	uniqueOperands.insert(token);
                    	numUniqueOperands++;
                	}
    			}

                

                /*if (!uniqueOperands.contains(m[iTemp+1]))
                {
                    uniqueOperands.insert(m[iTemp+1]);
                    std::cout<<endl<<m[iTemp+1];
                    numUniqueOperands++;
                }*/
                
            }

            lineTemp = m.suffix().str();
        }
        getline(fin, lineTemp);
        lineNum++;
    }


    n2 = numUniqueOperands;
    N2 = numTotalOperands;

	fin.close();
	return 0;
}


int findOperators(){
	ifstream fin;
	fin.open(filename);
	if (!fin)
    {
       std::cout << "Can't open the input file successfully." << endl;
       return 1;
    }

	string searchPattern = "auto|extern|register|static|typedef|virtual|mutable|inline|const|friend|volatile|final|break|case|continue|default|do|if|else|enum|for|goto|if|new|return|asm|operator|private|protected|public|sizeof|struct|switch|union|while|this|namespace|using|try|catch|throw|abstract|concrete|const_cast|static_cast|dynamic_cast|reinterpret_cast|typeid|template|explicit|true|false|typename|[=][=]|[=][&]|[=]|[!][=]|[!]|[%][=]|[%]|[&][&]|[&][=]|[&]|[|][|]|[|][=]|[|]|[(]|[)]|[{]|[}]|[[]|[\\]]|[*][=]|[*]|[+][=]|[+][+]|[+]|[,]|[-][-]|[-][=]|[-][>]|[-]|[.][.][.]|[.]|[/][=]|[/]|[:][:]|[:]|[<][<][=]|[>][>][=]|[<][<]|[<][=]|[<]|[=]|[>][=]|[>][>]|[>]|[?]|[\\^][=]|[\\^]|[~]|[;]|[#][#]|[\']|[\"]|[#][#]|[#]";

	smatch m;
    regex reg1(searchPattern);

    string lineTemp;
    int lineNum = 0;

    AvlTree<string> uniqueOperators;
    int numUniqueOperators = 0;
    Vector<int> operatorLocations;

	getline(fin, lineTemp);

	while (!fin.eof())
    {
        while (regex_search(lineTemp, m, reg1)&& !isComment[lineNum])
        {
            if (!uniqueOperators.contains(m[0]))
            {
                uniqueOperators.insert(m[0]);
                //std::cout<<m[0]<<endl;
                numUniqueOperators++;
            }
            operatorLocations.add(lineNum);
            lineTemp = m.suffix().str();
        }
        getline(fin, lineTemp);
        lineNum++;
    }

    n1 = numUniqueOperators;
    N1 = operatorLocations.size();

	fin.close();
	return 0;
}
int main (){

	initialize();
	countComment();
	findOperands();
	findOperators();

	//std:: cout<< endl <<"n1: "<< n1 <<endl<< "N1: "<<N1 << endl << "n2: " <<n2 <<endl<< "N2: " <<N2 << endl;
	ofstream myfile;
  	myfile.open (outputFile);
  	myfile << n1 << " " << n2 << " " << N1 << " " << N2 << endl;
  	myfile.close();
	return 0;
}


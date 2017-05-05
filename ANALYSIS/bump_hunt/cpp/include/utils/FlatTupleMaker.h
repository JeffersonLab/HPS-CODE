/*
 * @file FlatTupleMaker.h
 * @brief Utility used to create ROOT ntuples. 
 * @author Omar Moreno, SLAC National Accelerator Laboratory
 */

#ifndef __FLAT_TUPLE_MAKER_H__
#define __FLAT_TUPLE_MAKER_H__

//----------------//   
//   C++ StdLib   //
//----------------//   
#include <string>
#include <map>
#include <iostream>

//----------//
//   ROOT   //
//----------//
#include <TFile.h>
#include <TTree.h>

class FlatTupleMaker {

    public:

        /** Constructor */
        FlatTupleMaker(std::string file_name, std::string tree_name);

        /** Destructor */
        ~FlatTupleMaker();

        /** */
        void addVariable(std::string variable_name);

        /** */
        void addVector(std::string vector_name); 

        /** */
        void setVariableValue(std::string variable_name, double value) { variables[variable_name] = value; }; 

        /** */
        void addToVector(std::string variable_name, double value); 

        /** */
        bool hasVariable(std::string variable_name); 

        /** */
        void close(); 

        /** */
        void fill();

    private: 
    
        /** ROOT file to write ntuple to. */
        TFile* file;

        /** ROOT Tree. */
        TTree* tree; 

        /** Map containing ntuple variables */
        std::map <std::string, double> variables; 

        std::map <std::string, std::vector<double>> vectors; 
        

}; // FlatTupleMaker

#endif // __FLAT_TUPLE_MAKER_H__

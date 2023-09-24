#include "PluginManager.h"
#include <stdio.h>
#include <stdlib.h>
#include "TMAlignPlugin.h"

void TMAlignPlugin::input(std::string file) {
 inputfile = file;
/*std::ifstream ifile(inputfile.c_str(), std::ios::in);
 while (!ifile.eof()) {
   std::string key, value;
   ifile >> key;
   ifile >> value;
   parameters[key] = value;
 }*/
}

void TMAlignPlugin::run() {

}


void TMAlignPlugin::output(std::string file) {
   std::string command = "export OLDPATH=${PYTHONPATH}; ";
   command += "export PYTHONPATH=/usr/local/lib64/python3.9/site-packages/:${PYTHONPATH}; ";
   command += "python3.9 plugins/TMAlign/runTMAlign.py ";
   command +=  inputfile + "; ";
   command += "export PYTHONPATH=${OLDPATH}";
 std::cout << command << std::endl;

 system(command.c_str());
}

PluginProxy<TMAlignPlugin> TMAlignPluginProxy = PluginProxy<TMAlignPlugin>("TMAlign", PluginManager::getInstance());

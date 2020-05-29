# dredd_playground

# Dredd Installation
## Installing Dredd:
'''sh
npm install dredd --global
'''

#Install Python Dredd hooks
'''sh
pip install dredd_hooks
'''

##To run
>>cd dredd_playground
>>./runDredd.sh

#Directory structure
- configs: location of Dredd config files of individual services
- samples: sample files of the same scripts (OpenAPI description document which will be tested)
- dredd_utils: re-usable scripts go here (for example, to create API requests)

#Shell script
## runDredd.sh
This shell script is used to execute Dredd. 
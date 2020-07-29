#!/bin/sh

#dredd --config configs/sample-dredd.yml --output reports/dredd_report_samples.html -l debug 

#dredd --config configs/sample-dredd.yml --names

dredd samples/darwin_upload.yaml https://amb-qa-api.sparkcognition.com/v1/ --names
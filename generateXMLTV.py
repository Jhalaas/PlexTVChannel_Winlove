import os
import time
from datetime import datetime, timedelta
import temp_variables

def generateGuideData(myTvDirectory, myBackup, myShowDurations):
    showCounter = 0
    print("Generating Guide Data...This will take a few seconds")

    # Replace time in xmltv files
    ## Need to do this after execution b/c script takes long to execute
    with open(os.path.join(myTvDirectory, 'temp_xmltv.xml'), 'r') as f1:
        out_file = 'xmltv.xml' if not myBackup else 'xmltv1.xml'
        with open(os.path.join(myTvDirectory, out_file), 'w') as f2:

            # Wait for script to run on the minute (0 seconds)
            timeObject = datetime.now()
            myCurrentTime = int(timeObject.strftime("%S"))
            while (myCurrentTime / 60) != 0:
                timeObject = datetime.now()
                myCurrentTime = int(timeObject.strftime("%S"))
                continue

            for line in f1:
                # Replace & with correct escape
                line = line.replace('&', '&amp;')

                if '{tempStartTime}' in line:
                    showLength = myShowDurations[showCounter]
                    print ("Show length: " + str(showLength))
                    currentTime = timeObject.strftime("%Y%m%d%H%M%S")
                    line = line.replace('{tempStartTime}', str(currentTime))
                    timeObject += timedelta(seconds=showLength)
                    currentTime = timeObject.strftime("%Y%m%d%H%M%S")
                    line = line.replace('{tempEndTime}', str(currentTime))

                    # Increase show counter
                    showCounter += 1

                f2.write(line)

# Call the function
generateGuideData(temp_variables.tvDirectory, temp_variables.backup, list(temp_variables.showDurations))

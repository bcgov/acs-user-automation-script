## ACS MISO Automation Script

### Issue that trying to solve

On acs dashboard, deployments and images are on seperate page. On Deployments page it will only shows you the status/check result for deployment but not providing any information about which image this deployment is using. Find a way to merge two scan report from two page into one csv file would be helpful.

This script will get risk image in the namespace that you want to scan

### Usage

This script can satisfied the above requirement. It will get deployment and image scan result from ACS API endpoint and merge those information into one CSV file that is easy to look at.

This script now include fields for vulnerable image :

- image id
- singleImageCVESummary
- singleImageCVE
- singleImageComponentName
- singleImageCurrentComponent
- singleImageFixedComponent
- singleImageCVSS

You can add/find more available filed in ACS api (documentation)[https://acs-lab.developer.gov.bc.ca/main/apidocs#operation/ImageService_ListImages]

### How to use

To use this script you will need to provide 3 parameter into config.py file. Replace config.py.example with config.py.

- `NAMESPACE` that you have access and you want to get report for.
- `API_URL` for you AC instance, for example: `https://acs-instance.com/v1`
- `API_TOKEN` with your Miso Access that allows you to get namespace infomation for you ministry

Then to run the script you will need to

#### 1. Clone the repo and change into its directory.

```
git clone git@github.com:bcgov/acs-user-automation-script.git

cd acs-user-automation-script
```

#### 2. Run the script

##### Pre-request:

You will need to have python3 to run this script.
And in this script, there are two library is requred.
To install them, you will need to run:

```
python3 pip install --upgrade pip
sudo pip3 install requests pandas
```

After upon command successed. We can now run script by:

```
python3 acs-vulnerable-image-report.py
```

The output file will then being generated in your current directory in a formate "yournamespace-today's-date.csv"
You can change your desire output location at the last line of the acs-miso-automation.py.

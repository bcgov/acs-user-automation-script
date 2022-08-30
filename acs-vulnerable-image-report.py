import requests
import json
import pandas as pd
from datetime import datetime
import config


##
# 1. get all the deployments and filter by external namespace (6 character)
# 1.1 for all dev, test, tools, prod
# 2. return the deployment-ids based on external namespace
# 3. deployment ID lookup to return imageID
# 4. lookup single imageID for cve and component
##




def make_API_call(apiEndPoint):
    header = { "Authorization": f"Bearer {config.API_TOKEN}" }
    return requests.get(f"{config.API_URL}/{apiEndPoint}", headers=header).json()

singleImageResults =[]
singleImageCVESummary =[]
singleImageCVE =[]
singleImageCurrentComponent =[]
singleImageFixedComponent =[]
singleImageComponentName =[]
singleImageImageID =[]
singleImageCVSS =[]

# 1. get all the deployments and filter by external namespace (6 character)
Namespacevalue = config.NAMESPACE
response = make_API_call('deployments')
#returns 1000 deployments

result=len(response['deployments'])
print("Count total deployments :",result)



singleDeployments =[]
    
    
for x in response['deployments']:
	if (x['namespace'] == Namespacevalue):
		print(f"Value: "+x['namespace'])
		print(x['id'])
		singleDeployments.append(x['id'])
	#else:
	#	print(f"No, Value found")



resultDeployments=len(singleDeployments)
print("Count image items:",resultDeployments)
#returns deployments that match the namespace
#for each deployment, need to return the imageID if any

singleDeploymentID = []
SingleImageID = []
for x in range(resultDeployments):
	# responseSingleDeployments = requests.get(f"{config.API_URL}/deployments/"+singleDeployments[x],headers=header).json()
	responseSingleDeployments = make_API_call(f"/deployments/"+singleDeployments[x])
	singleDeploymentID.append(responseSingleDeployments)
	SingleImageID.append(singleDeploymentID[x]['containers'][0]['image']['id'])
	if (len(singleDeploymentID)) != 36:
		print ("not 36")

else:
		## start else
		for a in range(len(SingleImageID)):
			responseSingleImage = make_API_call(f"/images/"+SingleImageID[a])
			print("Count Image items:",len(responseSingleImage))
			print("Count Image Scan items:",len(responseSingleImage['scan']))
			print("Count Image Component items:",len(responseSingleImage['scan']['components']))
			print("Count Image fixable CVES:",responseSingleImage['fixableCves'])


			for y in range(len(responseSingleImage['scan']['components'])):

				if (len(responseSingleImage['scan']['components'][y]['fixedBy']) != 0):
					if (len(responseSingleImage['scan']['components'][y]['vulns'])!=0):
						singleImageImageID.append(responseSingleImage['name']['fullName'])
						singleImageCVE.append(responseSingleImage['scan']['components'][y]['vulns'][0]['cve'])
						#singleImageResults.append(responseSingleImage['scan']['components'][y]['vulns'][0]['summary'])
						singleImageCVSS.append(responseSingleImage['scan']['components'][y]['vulns'][0]['cvss'])
						#singleImageResults.append(responseSingleImage['scan']['components'][y]['vulns'])
						singleImageCVESummary.append(responseSingleImage['scan']['components'][y]['vulns'][0]['summary'])

					singleImageComponentName.append(responseSingleImage['scan']['components'][y]['name'])

					singleImageCurrentComponent.append(responseSingleImage['scan']['components'][y]['version'])
					print("fixed version:"+responseSingleImage['scan']['components'][y]['fixedBy'])
					singleImageFixedComponent.append(responseSingleImage['scan']['components'][y]['fixedBy'])

				# end if

				data1 = {
				'singleImageImageID': singleImageImageID,
				#'singleImageResults':singleImageResults,
				'singleImageCVESummary':singleImageCVESummary,
				#'responseSingleImage':responseSingleImage['scan']['components'],
				'singleImageCVE':singleImageCVE,
				'singleImageComponentName':singleImageComponentName,
				'singleImageCurrentComponent':singleImageCurrentComponent,
				'singleImageFixedComponent':singleImageFixedComponent,
				'singleImageCVSS':singleImageCVSS,
				#'deployments': singleDeployments,
				#'namespace':Namespacevalue,
				 }
				#dict = pd.DataFrame(data1)
				dict = pd.DataFrame.from_dict(data1, orient='index')
				dict = dict.transpose()

				# Getting the current date and time
				dt = datetime.now()

				# getting the timestamp
				ts = datetime.timestamp(dt)


				dateTimeObj = datetime.now()
				timestampStr = dateTimeObj.strftime("%d-%b-%Y")

				## write to csv
				## <<<<File path goes here >>>>>
				dict.to_csv (r'./'+Namespacevalue+'-'+timestampStr+'.csv', index = False, header=True)

		## end else

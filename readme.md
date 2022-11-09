## [Data Ingestion using AWS Lambda Function](https://www.udemy.com/course/data-engineering-using-aws-analytics-services/learn/lecture/28005884#questions/15671946)

### Incremental Load with Bookmark 

* [GH Archive](https://www.gharchive.org/) is a public website that provides records of the public GitHub timeline. the records are available as files, each file provides an hourly view of the activity of users across the globe. 
* Files are available in url `https://data.gharchive.org/{file_name}`. Example `https://data.gharchive.org/2015-01-01-15.json.gz` would provide activity details for Activity for `1/1/2015 @ 3PM UTC` 
* Our Lambda Function incrementally reads the files from [gharchive](https://data.gharchive.org/) and downloads these file to a folder within a s3 bucket while maintaining a bookmark of the last downloaded file.
* The function starts reading from the next file after the bookmark and puts it in the s3 location, if bookmark is available. Then it updates saves the last saved file name in the 'bookmark' file. The bookmark file should have the name of the last read file which has been downloaded by the lamda function in the folder of the s3 bucket.
* Incase bookmark is not available, the lamda function starts downloading the files from after the baseline file.
* The bucket name, prefix, baseline, environment are supplied as Environment to the lambda function. While testing the code locally along with the other environment variables we need to specify the AWS profile information as well in another environment variables. Sample environment variables:

        ENVIRON=DEV; // Set to 'DEV' for testing locally, while deploying to AWS set to 'PROD' 
        BUCKET_NAME=gh-archive-files; // Name of the bucket to save the files
        BOOKMARK_FILE=bookmark; // Name of the bookmark file
        BASELINE_FILE=2022-11-08-0.json.gz; // Name of the baseline file
        FILE_PREFIX=sandbox; // The folder prefix within the bucket where we want to save the file
        PROFILE=iam-admin-de // name of the preconfigured aws profile that will be used for testing locally, for deploying in AWS this is not needed as we use Roles for lambda to access s3  
* Refer to code for creating the logic in python
* Create a lambda function in AWS Console, set execution time in 60 secs and memory to 512 MB. Zip the contents of `gh_activity_downloader_lambda` and upload zip to lamda. Verify if all the files after the bookmark or after the baseline(incase bookmark is not available) are downloaded correctly in the S3 bucket.
* Create a rule in Event Bridge to trigger this Lambda function every 1 hour.


### Create folder structure for AWS lambda
* Install python, venv, pip and pycharm.
* Create the project folder as "gh_activity_downloader"
* Create a Python Virtual Environment as "gh_activity_downloader_venv", activate it and install requests & boto3 package in it. 

        mkdir gh_activity_downloader
        cd .\gh_activity_downloader\
        python -m venv gh_activity_downloader_venv
        .\gh_activity_downloader_venv\Scripts\activate
        pip install requests
        pip install boto3

* When we deploy a lambda code in AWS the boto3 library is already available so we don't need to have boto3 installed as a library, so we create a separate library folder "gh_activity_downloader_lambda" and install only `requests` in it.

        pip install requests -t gh_activity_downloader_lambda

* Create the two files: 
  * lambda_function.py -> This has the logic for the lambda code. Modify the lambda_function code to add the logic for incremental load. Add additional files as required.
  * lambda_validate.py -> This has the logic to test the lambda code locally
* Login to AWS Console and create a lambda function.
* Zip the contents(not the folder) inside gh_activity_downloader_lambda as zip file gh_activity_downloader.zip and upload as lambda function
* Upload .\gh_activity_downloader_lambda.zip and test the lambda
* [Files](C:\Users\subhr\digital-ninja\data-engg-with-aws\python-lambdas\gh_activity_downloader)


### References

* [Commenting in Python](https://www.simplilearn.com/tutorials/python-tutorial/comments-in-python#:~:text=Comments%20in%20Python%20are%20identified,a%20multi%2Dline%20comment%20block.)
How to write comments in Python
* [Using Multiline String](https://www.programiz.com/python-programming/examples/multiline-string)
How to define multiline strings in python 
* [Python fStrings](https://realpython.com/python-f-strings/#:~:text=In%20Python%20source%20code%2C%20an,their%20values.%E2%80%9D%20(Source)): 
What are the advantages of using f-Strings should be used over %-formatting and .format() methods
* [strptime()](https://www.geeksforgeeks.org/python-datetime-strptime-function/)
This is used to format timestamps that are in strings to data time object using formatters such as %Y %M %d %H etc
* [timedelta()](https://www.geeksforgeeks.org/python-datetime-timedelta-function/)
Used for calculating time differences, for example to add some delta for example an hour to a datetime object
* [strftime()](https://www.geeksforgeeks.org/python-strftime-function/)
Converts datetime objects to their string representation [Formatter CheatSheet for strftime](https://strftime.org/)


    baseline_file = '2022-11-07-0.json.gz'
  
    // baseline_file is a string so it's split and the first part is stored in date_part_str
    date_part_str = baseline_file.split('.')[0]
    print(date_part_str)
  
    // date_part_str is parsed to datetime using datetime.strptime()
    date_part_parsed_to_datetime = datetime.strptime(date_part_str, '%Y-%M-%d-%H')
    print(date_part_parsed_to_datetime)
  
    // add 1 hour of timedelta to date_part_parsed_to_datetime and stores it in date_time_incremented that is of time datetime
    date_time_incremented = date_part_parsed_to_datetime + timedelta(hours=1)
    print(date_time_incremented)
  
    // converts the datetime to string and stores in date_time_incremented_formatted_to_string
    date_time_incremented_formatted_to_string = datetime.strftime(date_time_incremented, '%Y-%M-%d-%H')
    print(date_time_incremented_formatted_to_string)
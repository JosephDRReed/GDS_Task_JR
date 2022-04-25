import numpy as np
import pandas as pd


# Q2 - load data

# import .csv files
df_opening = pd.read_csv("/Users/josephreed/Documents/GitHub/GDS_Task_JR/interview files/zipped-interview-files-for-candidate/GPOpeningTimes.csv", sep='¬', engine='python', encoding='raw_unicode_escape')
df_practices = pd.read_csv("//Users/josephreed/Documents/GitHub/GDS_Task_JR/interview files/zipped-interview-files-for-candidate/GPPractices.csv",  sep='¬', engine='python', encoding='raw_unicode_escape')
df_performance = pd.read_csv("/Users/josephreed/Documents/GitHub/GDS_Task_JR/interview files/zipped-interview-files-for-candidate/TransparencyIndicatorsGPPerformance.csv",  sep='¬', engine='python', encoding='raw_unicode_escape')

# check columns are correct
for col in df_opening.columns:
    print(col)
for col in df_practices.columns:
    print(col)
for col in df_performance.columns:
    print(col)

print(df_opening.head())
print(df_practices.head())
print(df_performance.head())

print(df_opening.head(n=10).to_string(index=False))
print(df_practices.head(n=10).to_string(index=False))
print(df_performance.head(n=10).to_string(index=False))


# # Q3
# select records from df_performance where Antibiotic Prescribing value is greater than 0.5
df_performance_APR = df_performance.query("MetricName == 'Antibiotic Prescribing' & Value > '0.5'")[["OrganisationID", "Value"]]

# remove duplicates
df_performance_APR_unique = df_performance_APR.drop_duplicates()

# join to GP lookup - note it seems not all OrganisationIDs which exist in the performance csv match to the GPPractices lookup. Organisations missing from the lokoup will be excluded.
df_performance_APR_contact = pd.merge(df_practices, df_performance_APR_unique, on='OrganisationID')[["OrganisationName", "Address1", "Address2", "Address3", "City", "County", "Postcode", "Value"]]

# rename value column
df_performance_APR_contact = df_performance_APR_contact.rename(columns={"Value": "Value of antibiotic prescribing rate"})

# check the output
print(df_performance_APR_contact)
print(df_performance_APR_contact.head(n=10).to_string(index=False))

# create .csv
df_performance_APR_contact.to_csv("/Users/josephreed/Documents/GitHub/GDS_Task_JR/interview files/zipped-interview-files-for-candidate/Question3Output.csv", sep='¬', encoding='raw_unicode_escape', index_label='OrganisationID')


# Q4

# create dataframe of org id, opening hour, opening minute, closing hour, closing minute
df_opening_time_minutes = df_opening.query("OpeningTimeType == 'Reception'")[["OrganisationId", "Times"]]

df_opening_time_minutes['OpeningHour']   = df_opening_time_minutes['Times'].str.slice(0,2)
df_opening_time_minutes['OpeningMinute'] = df_opening_time_minutes['Times'].str.slice(3,5)
df_opening_time_minutes['ClosingHour']   = (df_opening_time_minutes['Times'].str.slice(6,8)).replace("00","24")
df_opening_time_minutes['ClosingMinute'] = df_opening_time_minutes['Times'].str.slice(9,11)

# Calculate open minutes per day
df_opening_time_minutes['OpenTotalMinutes'] = ((df_opening_time_minutes['ClosingHour'].astype(int)-df_opening_time_minutes['OpeningHour'].astype(int))*60) + (df_opening_time_minutes['ClosingMinute'].astype(int)-df_opening_time_minutes['OpeningMinute'].astype(int))

# sum up over all days per organisation
df_total_open_minutes_per_week = df_opening_time_minutes.groupby(['OrganisationId']).sum('OpenTotalMinutes')
df_total_open_minutes_per_week = df_total_open_minutes_per_week.rename(columns={"OpenTotalMinutes": "OpenWeeklyTotalMinutes"})

# create a dataframe sorted by open time per week
sorted_df_total_open_minutes_per_week = df_total_open_minutes_per_week.sort_values(by='OpenWeeklyTotalMinutes')
print(sorted_df_total_open_minutes_per_week)

#export to csv
sorted_df_total_open_minutes_per_week.to_csv("/Users/josephreed/Documents/GitHub/GDS_Task_JR/interview files/zipped-interview-files-for-candidate/Question4Output.csv", sep='¬', encoding='raw_unicode_escape', index_label='OrganisationId')


# Question 5
# I found the following online as a starting point but haven't had the time to complete this question:
# run the following in Terminal: pip install --upgrade google-api-python-client
# result = bigquery.jobs().insert(projectId=PROJECT_ID, body={'jobReference': {'jobId': job_id},'configuration': {'load': load_config}}, media_body=upload).execute(num_retries=5)

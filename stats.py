import pandas as pd
import numpy as np
from datetime import datetime

# raw_df = pd.read_csv('chapter-roster-joined-2024.csv')
# df = raw_df[['Volunteer ID', 'Congressional District', 'Date Added to Database']]
# # show total number of new members that joined community in 2024
# print("Total New Joiners 2024: ", df.shape[0])
# print("Attributes per member: ", df.columns)

# # show number of members that joined over time as a bar graph, buckets are months
# df['Date Added to Database'] = pd.to_datetime(df['Date Added to Database'])
# grouped_df = df.groupby(df['Date Added to Database'].dt.month)
# for key, item in grouped_df:
#     # print(grouped_df.get_group(key))
#     print("TOTAL: ", grouped_df.get_group(key).shape[0]) 

# # show number of members that joined by congressional district
# grouped_df = df.groupby(df['Congressional District'])
# for key, item in grouped_df:
#     print(grouped_df.get_group(key))
#     print("TOTAL: ", grouped_df.get_group(key).shape[0])
 

def clean_data(raw_members_df, raw_actions_df):
    members_df = raw_members_df[['Volunteer ID', 'First Name', 'Last Name', 'Congressional District', 'How Active', 'Engagement Segment']]
    actions_df = raw_actions_df[['volunteer id', 'district', 'activity date', 'type', 'category', 'activity name']]
    actions_df['activity date'] = pd.to_datetime(actions_df['activity date'])

    # rename columns
    members_df = members_df.rename(columns={'Volunteer ID': 'volunteer_id', 'Congressional District': 'district'})
    actions_df = actions_df.rename(columns={'volunteer id': 'volunteer_id', 'district': 'district'})

    # filter out null volunteer ids
    members_df = members_df[members_df['volunteer_id'].notnull()]

    # Filter out non-IL districts, and filter out actions from before Jan 1 2024
    members_df = members_df[members_df['district'].str.contains("IL", na=False)]
    actions_df = actions_df[actions_df['district'].str.contains("IL", na=False)]

    return members_df, actions_df


if __name__=="__main__":
    raw_members_df = pd.read_csv('chapter-roster.csv')
    raw_actions_df = pd.read_csv('activity_download_2023-12-09-2024-12-24.csv')

    members_df, actions_df = clean_data(raw_members_df, raw_actions_df)

    # override the 'district' column in actions_df with district from members_df
    id_to_district = members_df.set_index('volunteer_id')['district']
    actions_df['district'] = actions_df['volunteer_id'].map(id_to_district)

    print("TOTAL NUM MEMBERS: ", members_df.shape[0])
    print("TOTAL NUM ACTIONS: ", actions_df.shape[0])

    # Filter the dataframe for actions taken after Jan 1 2024
    actions_df = actions_df[
        (actions_df['activity date'] >= datetime(2024, 1, 1))
    ]

    # Group by district and count the number of volunteers
    volunteers_per_district = (
        members_df.groupby('district')
        .size()
        .reset_index(name='Total Volunteers')
    )

    # Display the result
    print("VOLUNTEERS PER DISTRICT")
    print(volunteers_per_district)

    # Group by district and count the number of actions
    actions_per_district = (
        actions_df.groupby('district')
        .size()
        .reset_index(name='Total Actions')
    )

    # Display the result
    print("ACTIONS PER DISTRICT")
    print(actions_per_district)

    # Group actions_df by 'district' and count unique volunteer_id
    unique_volunteers_per_district = (
        actions_df.groupby('district')['volunteer_id']
        .nunique()
        .reset_index(name='unique_volunteers')
    )

    # Display the result
    print("UNIQUE ACTIVE VOLUNTEERS PER DISTRICT")
    print(unique_volunteers_per_district)

    print("TOTAL NUM UNQIUE VOLUNTEERS IN ACTIONS_DF")
    print(len(pd.unique(actions_df['volunteer_id'])))
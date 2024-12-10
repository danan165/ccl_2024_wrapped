import pandas as pd
import numpy as np
from datetime import datetime
 

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
    actions_df = actions_df[
        (actions_df['activity date'] >= datetime(2024, 1, 1))
    ]

    # override the 'district' column in actions_df with district from members_df
    id_to_district = members_df.set_index('volunteer_id')['district']
    actions_df['district'] = actions_df['volunteer_id'].map(id_to_district)

    return members_df, actions_df


if __name__=="__main__":
    raw_members_df = pd.read_csv('data/chapter-roster.csv')
    raw_actions_df = pd.read_csv('data/activity_download_2023-12-09-2024-12-24.csv')

    members_df, actions_df = clean_data(raw_members_df, raw_actions_df)

    # Group by district and count the number of volunteers
    volunteers_per_district = (
        members_df.groupby('district')
        .size()
        .reset_index(name='Total Volunteers')
    )
    print("# of CCL Chicago Members (per District)")
    print(volunteers_per_district)

    total_num_members = members_df.shape[0]
    print("Total # of CCL Chicago Members: ", total_num_members)

    # TODO gotta eliminate those with a district that is not IL01-IL09
    # allowlist_il_districts = ['IL01', 'IL02', 'IL03', 'IL04', 'IL05', 'IL06', 'IL07', 'IL08', 'IL09']
    # print("Total # of CCL Chicago Members with no District: ", total_num_members - volunteers_per_district['Total Volunteers'].sum())
    print("\n\n")

    # Group actions_df by 'district' and count unique volunteer_id
    unique_volunteers_per_district = (
        actions_df.groupby('district')['volunteer_id']
        .nunique()
        .reset_index(name='unique_volunteers')
    )
    print("# of Members w/ Activity (per District)")
    print(unique_volunteers_per_district)
    
    total_num_members_w_activity = len(pd.unique(actions_df['volunteer_id']))
    print("Total # of Members w/ Activity: ", total_num_members_w_activity)
    print("Total # of Members w/ Activity (but no district): ", total_num_members_w_activity - unique_volunteers_per_district['unique_volunteers'].sum())
    print("\n\n")

    # Group by district and count the number of actions
    actions_per_district = (
        actions_df.groupby('district')
        .size()
        .reset_index(name='Total Actions')
    )
    print("# of Actions (per District)")
    print(actions_per_district)
    print("Total # of Actions: ", actions_df.shape[0])
    print("Total # of Actions w/ no district: ", actions_df.shape[0] - actions_per_district['Total Actions'].sum())
    print("\n\n")
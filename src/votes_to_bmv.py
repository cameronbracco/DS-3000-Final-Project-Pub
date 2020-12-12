# The idea of this file is to take a CSV that is the final votes (columns are id, then one per bill) 
# and turn it into the form of the final dataset

# This will produce a csv with the following columns
# - bill_id
# - member_id
# - vote_position

# Once we have the output of this file we can combine with the totals/ratios and bill metric datasets
# to get the final form. We may also need to do something to get the member party

import pandas as pd
import numpy as np

vote_totals_df = pd.read_csv("data-totals/votes/votes-cast-total.csv")
index_col = "Unnamed: 0.1.1"

final_form_df = pd.DataFrame(columns=["bill_id", "member_id", "vote_position"])


x = vote_totals_df.columns.tolist()[3:]
for col_name in x:
    # Going through specific column
    print("Adding entries for bill:", col_name)
    col = vote_totals_df[col_name]

    new_rows = []
    for i in range(len(col)):
        vote_pos = col[i]
        # Checking to see if we have a value 
        if type(vote_pos) == type("str"):
            print("Found a vote position", vote_pos, type(vote_pos), type(np.nan))
            row_to_add = {
                "bill_id": col_name, 
                "member_id": vote_totals_df[index_col][i],
                "vote_position": vote_pos
            }
            new_rows.append(row_to_add)
    
    final_form_df = final_form_df.append(new_rows, ignore_index=True)

print(final_form_df.head)

final_form_df.to_csv("final-data/bill_member_vote.csv")


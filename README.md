# Classification-of-Codeforce-Programs


## Files Descriptions
1. userinfo.py: collect user information from codeforce (cf_rated_users.json)
2. prog.py: collect source code for a specific contest (for n contests we will get n number of csv files)
3. merge.py: merge source code information and userinformation (for n contests we will get n number of merged csv filse)
4. cleanData.py: only takes those rows which contain c++ program and firsName (one outfut file: cleaned_data.csv)
5. firstName.py: list all the unique firstName and stored on name.json
6. gender.py: identify gender from the list name.json (one output file: gender.json)
7. mergeName.py: Add gender information by merging 'cleaned_data.csv' and 'gender.json' [Add continent information from 'continent.json'] (one output file: final_data.csv)
8. balanceFinalData_gender.py: Balancing Male and Female coder (output files: balanceGender.csv + Individual problem sets)
9. balanceFinalData_region.py: Balancing Region (output files: balanceRegion.csv + Individual problem sets)


## Final Datasets
balanceGender.csv, balanceRegion.csv, final_data.csv, (+Individual problemsets)

## Finally
After completing all above things do the following sequentially:
1. (halstead.py + main.exe): Calculate Halstead using 
2. feature.py: Calculate Cyclometic Complexity

---

### N.B. All balanced data sets have been uploaded in 'Dataset' directory.


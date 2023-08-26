import pandas as pd

# Load data
school_data = pd.read_csv("./Resources/schools_complete.csv")
student_data = pd.read_csv("./Resources/students_complete.csv")

# Combine data into a single dataset
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])

# District Summary
total_schools = school_data["school_name"].nunique()
total_students = school_data_complete["Student ID"].count()
total_budget = school_data["budget"].sum()
average_math_score = school_data_complete["math_score"].mean()
average_reading_score = school_data_complete["reading_score"].mean()

passing_math = school_data_complete[school_data_complete["math_score"] >= 70]
passing_reading = school_data_complete[school_data_complete["reading_score"] >= 70]

percent_passing_math = (passing_math["Student ID"].count() / total_students) * 100
percent_passing_reading = (passing_reading["Student ID"].count() / total_students) * 100

overall_passing_rate = (percent_passing_math + percent_passing_reading) / 2

district_summary = pd.DataFrame({
    "Total Schools": [total_schools],
    "Total Students": [total_students],
    "Total Budget": [total_budget],
    "Average Math Score": [average_math_score],
    "Average Reading Score": [average_reading_score],
    "% Passing Math": [percent_passing_math],
    "% Passing Reading": [percent_passing_reading],
    "% Overall Passing": [overall_passing_rate]
})

# School Summary
school_group = school_data_complete.groupby("school_name")
school_type = school_group["type"].first()
total_students_school = school_group.size()
total_budget_school = school_group["budget"].first()
per_student_budget = total_budget_school / total_students_school

average_math_score_school = school_group["math_score"].mean()
average_reading_score_school = school_group["reading_score"].mean()

passing_math_school = school_data_complete[school_data_complete["math_score"] >= 70].groupby("school_name")["Student ID"].count()
passing_reading_school = school_data_complete[school_data_complete["reading_score"] >= 70].groupby("school_name")["Student ID"].count()

percent_passing_math_school = (passing_math_school / total_students_school) * 100
percent_passing_reading_school = (passing_reading_school / total_students_school) * 100

overall_passing_rate_school = (percent_passing_math_school + percent_passing_reading_school) / 2

school_summary = pd.DataFrame({
    "School Type": school_type,
    "Total Students": total_students_school,
    "Total School Budget": total_budget_school,
    "Per Student Budget": per_student_budget,
    "Average Math Score": average_math_score_school,
    "Average Reading Score": average_reading_score_school,
    "% Passing Math": percent_passing_math_school,
    "% Passing Reading": percent_passing_reading_school,
    "% Overall Passing": overall_passing_rate_school
})

# Highest-Performing Schools
top_schools = school_summary.sort_values(by="% Overall Passing", ascending=False).head()

# Lowest-Performing Schools
bottom_schools = school_summary.sort_values(by="% Overall Passing").head()

# Math Scores by Grade
math_scores_by_grade = pd.pivot_table(school_data_complete, values='math_score', index='school_name', columns='grade', aggfunc='mean', fill_value=0)

# Reading Scores by Grade
reading_scores_by_grade = pd.pivot_table(school_data_complete, values='reading_score', index='school_name', columns='grade', aggfunc='mean', fill_value=0)

# Scores by School Spending
spending_bins = [0, 585, 630, 645, 680]
spending_labels = ["<$585", "$585-630", "$630-645", "$645-680"]

school_summary["Spending Ranges (Per Student)"] = pd.cut(per_student_budget, bins=spending_bins, labels=spending_labels)
spending_summary = school_summary.groupby("Spending Ranges (Per Student)").agg({
    "Average Math Score": "mean",
    "Average Reading Score": "mean",
    "% Passing Math": "mean",
    "% Passing Reading": "mean",
    "% Overall Passing": "mean"
})

# Scores by School Size
size_bins = [0, 1000, 2000, 5000]
size_labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

school_summary["School Size"] = pd.cut(total_students_school, bins=size_bins, labels=size_labels)
size_summary = school_summary.groupby("School Size").agg({
    "Average Math Score": "mean",
    "Average Reading Score": "mean",
    "% Passing Math": "mean",
    "% Passing Reading": "mean",
    "% Overall Passing": "mean"
})

# Scores by School Type
type_summary = school_summary.groupby("School Type").agg({
    "Average Math Score": "mean",
    "Average Reading Score": "mean",
    "% Passing Math": "mean",
    "% Passing Reading": "mean",
    "% Overall Passing": "mean"
})

# Print the DataFrames or save them to CSV as needed
print("District Summary:")
print(district_summary)

print("\nSchool Summary:")
print(school_summary)

print("\nTop Performing Schools:")
print(top_schools)

print("\nBottom Performing Schools:")
print(bottom_schools)

print("\nMath Scores by Grade:")
print(math_scores_by_grade)

print("\nReading Scores by Grade:")
print(reading_scores_by_grade)

print("\nScores by School Spending:")
print(spending_summary)

print("\nScores by School Size:")
print(size_summary)

print("\nScores by School Type:")
print(type_summary)

def run(path): 
    # Import modules here 
    import pandas as pd 

    # Read the data from the given Excel file
    path=r"C:\Users\Admin\Downloads\Data Engineering\Data Engineering\data - sample.xlsx"

    df = pd.read_excel(path)

    df['attendance_date'] = pd.to_datetime(df['attendance_date'])
    
    df.sort_values(by=['student_id', 'attendance_date'], inplace=True)
    results = []

   
    for student_id, group in df.groupby('student_id'):
        group['is_absent'] = (group['status'] == 'Absent').astype(int)
        group['streak_group'] = (group['is_absent'] != group['is_absent'].shift()).cumsum()
        
        absences = group[group['is_absent'] == 1]

        streaks = absences.groupby('streak_group').agg({
            'attendance_date': ['min', 'max', 'count']
        })
        streaks.columns = ['absence_start_date', 'absence_end_date', 'total_absent_days']

        latest_streak = streaks[streaks['total_absent_days'] > 3].tail(1)
        if not latest_streak.empty:
            result = {
                'student_id': student_id,
                'absence_start_date': latest_streak['absence_start_date'].values[0],
                'absence_end_date': latest_streak['absence_end_date'].values[0],
                'total_absent_days': latest_streak['total_absent_days'].values[0]
            }
            results.append(result)

    output_df = pd.DataFrame(results)
    
    if output_df.empty:
        print("No students found with absence streaks longer than three days.")
    else:
        print(output_df)

    print(output_df.head()) 

    # Return the output
    return output_df


   
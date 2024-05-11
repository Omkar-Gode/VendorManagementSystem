def time_diff_in_hours(from_date, to_date):
    diff = to_date -from_date
    return (diff.days*24) + (diff.seconds/60)/60
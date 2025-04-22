def get_month_range(year: int, month: int) -> tuple:
    """
    Returns the start and end date for a specific month.
    
    :param year: The year as an integer.
    :param month: The month as an integer (1-12).
    :return: A tuple with the start and end date of the month.
    """
    start_date = f"{year}-{month:02d}-01"
    if month == 2:
        end_date = f"{year}-{month:02d}-28"
    elif month in [4, 6, 9, 11]:
        end_date = f"{year}-{month:02d}-30"
    else:
        end_date = f"{year}-{month:02d}-31"
    return start_date, end_date
def detect_sim_provider(phone):
    """
    Detect SIM provider based on phone number prefix.
    NOTE: Use real prefix data for production.
    """
    # Example: +919812345678
    prefix = phone[3:5]  # After +91, next 2 digits
    if prefix in ['98', '99']:
        return 'Airtel'
    elif prefix in ['96', '70']:
        return 'Jio'
    elif prefix in ['97']:
        return 'Vi'
    elif prefix in ['94', '95']:
        return 'BSNL'
    else:
        return 'Unknown'
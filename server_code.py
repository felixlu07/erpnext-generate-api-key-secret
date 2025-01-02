@frappe.whitelist()
def generate_keys(user):
    """Generate API key and secret for the user"""
    user_details = frappe.get_doc('User', user)
    api_secret = frappe.generate_hash(length=15)
 
    if not user_details.api_key:
        api_key = frappe.generate_hash(length=15)
        user_details.api_key = api_key
    else:
        api_key = user_details.api_key

    user_details.api_secret = api_secret
    user_details.save()

    return {
        "api_key": api_key,
        "api_secret": api_secret
    }

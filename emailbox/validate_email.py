import re
import dns.resolver


def validator(email):
    res = {
        "is_valid": True,
        "syntax_error_status": None,
        "role_status": None,
        "role": None,
        "disposable_provider": None,
        "disposable_status": None,
        "free_status": None,
        "dns_status": None,
        "domain": None,
        "account": None
    }

    # Syntax Error
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        res["syntax_error_status"] = False
        res["is_valid"] = True
    else:
        res["syntax_error"] = True
        res["is_valid"] = False
        return res

    account, domain = email.split("@")
    res["domain"] = domain
    res["account"] = account

    try:
        dns.resolver.resolve(domain, 'MX')
        res["dns_status"] = True
    except:
        res["dns_status"] = False
        res["is_valid"] = False

    # Role

    match = re.match(r"^(info|admin|sales|support|contact|help)", email)
    if match:
        matched_role = match.group()
        res["role_status"] = True
        res["role"] = matched_role
    else:
        res["role_status"] = False


    match = re.match(r"^[^@]+@(guerrillamail|10minutemail|dispostable|mailinator|getnada)\.", email)
    if match:
        matched_provider = match.group(1)
        res["disposable_status"] = True
        res["is_valid"] = False
        res["disposable_provider"] = matched_provider
    else:
        res["disposable_status"] = False

    # Check if from free email service
    free_email_services = ["gmail.com", "yahoo.com", "hotmail.com"]
    if domain in free_email_services:
        res["free_status"] = True
    else:
        res["free_status"] = False

    return res


# email = "avintraai@gmail.com"
# result = validator(email)
# print(result)
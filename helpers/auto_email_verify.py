from botasaurus import *
from auto_get_user import auto_get_user

def auto_email_verify():
    driver = bt.create_driver()
    user = auto_get_user()
    bt.Profile.set_profile(user)
    email = user["email"]
    link = bt.TempMail.get_email_link_and_delete_mailbox(email)  # Retrieves the Verification Link and Deletes the Mailbox
    driver.get(link)






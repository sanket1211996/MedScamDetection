
# profile_data = {'url': url, 'title': title, 'organiser': organiser, 'organiser_location': organiser_loc,
#                 'content': all_text}

scam_detection_rule = ['similar_pictures, similar_patient_name_different_conditions, similar_medical_info_different_identity']





def analyze_profile(fundData):
    foundScamLinks = []
    # for rule in scam_detection_rule:
    #     foundScamLinks = rule()
    #



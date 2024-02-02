from venv import logger


class DataRetrievalSettings:
    def __init__(self) -> None:
        self.__document_category_settings = {
            "SD1": [
                {
                    "type": "Passport",
                    "fields": [
                        {
                            "key": "passport_number",
                            "value": "DOCUMENT_NUMBER",
                            "type": "text",
                            "required": True,
                            "minimum_confidence": "80",
                        },
                        {
                            "key": "passport_issue_date",
                            "value": "Passport Issue Date",
                            "type": "date",
                            "required": True,
                            "minimum_confidence": "70",
                        },
                        {
                            "key": "passport_expiry_date",
                            "value": "EXPIRATION_DATE",
                            "type": "date",
                            "required": True,
                            "minimum_confidence": "50",
                        },
                        {
                            "key": "first_name",
                            "value": "FIRST_NAME",
                            "type": "text",
                            "required": True,
                            "minimum_confidence": "60",
                        },
                        {
                            "key": "id_type",
                            "value": "ID_TYPE",
                            "type": "text",
                            "required": True,
                            "minimum_confidence": "90",
                        },
                        {
                            "key": "last_name",
                            "value": "LAST_NAME",
                            "type": "text",
                            "required": True,
                            "minimum_confidence": "90",
                        },
                        {
                            "key": "middle_name",
                            "value": "MIDDLE_NAME",
                            "type": "text",
                            "required": True,
                            "minimum_confidence": "90",
                        },
                        {
                            "key": "place_of_birth",
                            "value": "PLACE_OF_BIRTH",
                            "type": "text",
                            "required": True,
                            "minimum_confidence": "90",
                        },
                    ],
                },
                {
                    "type": "DrivingLicense",
                    "fields": [
                        {
                            "key": "driving_license_number",
                            "value": "Driving License Number",
                            "type": "text",
                            "required": True,
                            "minimum_confidence": "70",
                        },
                        {
                            "key": "driving_license_issue_date",
                            "value": "Driving License Issue Date",
                            "type": "date",
                            "required": True,
                            "minimum_confidence": "55",
                        },
                        {
                            "key": "driving_license_expiry_date",
                            "value": "Driving License Expiry Date",
                            "type": "date",
                            "required": True,
                            "minimum_confidence": "40",
                        },
                        {
                            "key": "driving_license_authority",
                            "value": "Driving License Authority",
                            "type": "text",
                            "required": True,
                            "minimum_confidence": "60",
                        },
                    ],
                },
            ],
            "CD1": [
                {
                    "type": "VisaApplication",
                    "fields": [
                        {
                            "key": "visa_application_number",
                            "value": "Visa Application Number",
                            "type": "text",
                            "required": True,
                            "minimum_confidence": "70",
                        },
                        {
                            "key": "visa_application_date",
                            "value": "Visa Application Date",
                            "type": "date",
                            "required": True,
                            "minimum_confidence": "60",
                        },
                        {
                            "key": "visa_application_expiry_date",
                            "value": "Visa Application Expiry Date",
                            "type": "date",
                            "required": True,
                            "minimum_confidence": "50",
                        },
                        {
                            "key": "visa_application_authority",
                            "value": "Visa Application Authority",
                            "type": "text",
                            "required": True,
                            "minimum_confidence": "60",
                        },
                        {
                            "key": "generated",
                            "value": "Generated",
                            "type": "text",
                            "required": True,
                            "minimum_confidence": "60",
                        },
                        {
                            "key": "country_of_birth",
                            "value": "Country of birth",
                            "type": "text",
                            "required": True,
                            "minimum_confidence": "90",
                        },
                        {
                            "key": "country_of_passport",
                            "value": "Country of passport",
                            "type": "text",
                            "required": True,
                            "minimum_confidence": "90",
                        },
                        {
                            "key": "country_of_issue",
                            "value": "Country of issue",
                            "type": "text",
                            "required": True,
                            "minimum_confidence": "80",
                        },
                        {
                            "key": "current_location",
                            "value": "Current location",
                            "type": "text",
                            "required": True,
                            "minimum_confidence": "80",
                        },
                        {
                            "key": "date_of_birth",
                            "value": "Date of birth",
                            "type": "date",
                            "required": True,
                            "minimum_confidence": "90",
                        },
                        {
                            "key": "health_examination",
                            "value": "Health examination",
                            "type": "text",
                            "required": True,
                            "minimum_confidence": "80",
                        },
                    ],
                },
                {
                    "type": "Resume",
                    "fields": [
                        {
                            "key": "resume_name",
                            "value": "Resume Name",
                            "type": "text",
                            "required": True,
                            "minimum_confidence": "70",
                        },
                        {
                            "key": "experience",
                            "value": "Resume Date",
                            "type": "date",
                            "required": True,
                            "minimum_confidence": "60",
                        },
                        {
                            "key": "resume_expiry_date",
                            "value": "Resume Expiry Date",
                            "type": "date",
                            "required": True,
                            "minimum_confidence": "50",
                        },
                        {
                            "key": "resume_authority",
                            "value": "Resume Authority",
                            "type": "text",
                            "required": True,
                            "minimum_confidence": "60",
                        },
                    ],
                },
            ],
        }

    def get_settings_by_top_level_category(self, top_level_category):
        return self.__document_category_settings.get(top_level_category, None)

    def get_settings_by_document_type(self, top_level_category, document_type):
        settings = self.get_settings_by_top_level_category(top_level_category)
        if settings is not None:
            for setting in settings:
                if setting["type"] == document_type:
                    return setting
        return None

    def get_settings_by_document_type_and_key(
        self, top_level_category, document_type, key
    ):
        settings = self.get_settings_by_document_type(top_level_category, document_type)
        if settings is not None:
            for setting in settings["fields"]:
                if setting["key"] == key:
                    return setting
        return None

    def get_field_confidence_threshold(self, top_level_category, document_type, key):
        setting = self.get_settings_by_document_type_and_key(
            top_level_category, document_type, key
        )
        logger.info(f"from data retrieval setting: {setting}")
        if setting is not None:
            min_confidence = setting["minimum_confidence"]
            logger.info(f"min_confidence from data retrieval setting: {min_confidence}")
            return min_confidence
        return None

    def get_required_keys_by_document_type(self, top_level_category, sub_document_type):
        settings = self.get_settings_by_document_type(
            top_level_category, sub_document_type
        )
        if settings is not None:
            return [
                (setting["key"], setting["value"])
                for setting in settings["fields"]
                if setting["required"]
            ]
        return None

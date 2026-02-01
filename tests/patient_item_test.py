"""Test module for patient_item class."""
import unittest
from aws.patient_item import patient_item

class TestPatientItem(unittest.TestCase):
    """Test suite for patient_item class"""

    def test_valid_patient_creation(self):
        """Test creating a valid patient item"""
        patient = patient_item(
            patientID=123456,
            Age=30,
            first_name="John",
            last_name="Doe",
            Gender="Male",
            general_practice="City Medical Center",
            home_address="123 Main St",
            phone_number="+1234567890"
        )
        patient.__post_init__()
        self.assertEqual(patient.patientID, 123456)
        self.assertEqual(patient.Age, 30)
        self.assertEqual(patient.first_name, "John")
        self.assertEqual(patient.last_name, "Doe")

    def test_invalid_patient_id(self):
        with self.assertRaises(ValueError) as e:
            resposne = patient_item(
                patientID=12345,
                Age=30,
                first_name="John",
                last_name="Doe",
                Gender="Male",
                general_practice="City Medical Center",
                home_address="123 Main St",
                phone_number="+1234567890"
            )
            resposne.__post_init__()
        self.assertEqual(e.exception.args[0], 'patientID 12345 is invalid format')

    def test_invalid_age_negative(self):
        with self.assertRaises(ValueError) as e:
            resposne = patient_item(
                patientID=123456,
                Age=-1,
                first_name="John",
                last_name="Doe",
                Gender="Male",
                general_practice="City Medical Center",
                home_address="123 Main St",
                phone_number="+1234567890"
            )
            resposne.__post_init__()
        self.assertEqual(e.exception.args[0], 'Age -1 is invalid not within valid age range')

    def test_invalid_age_too_high(self):
        with self.assertRaises(ValueError) as e:
            resposne = patient_item(
                patientID=123456,
                Age=201,
                first_name="John",
                last_name="Doe",
                Gender="Male",
                general_practice="City Medical Center",
                home_address="123 Main St",
                phone_number="+1234567890"
            )
            resposne.__post_init__()
        self.assertEqual(e.exception.args[0], 'Age 201 is invalid not within valid age range')

    def test_valid_age_boundary(self):
        patient_min = patient_item(
            patientID=123456,
            Age=0,
            first_name="John",
            last_name="Doe",
            Gender="Male",
            general_practice="City Medical Center",
            home_address="123 Main St",
            phone_number="+1234567890"
        )
        self.assertEqual(patient_min.Age, 0)

        patient_max = patient_item(
            patientID=123456,
            Age=200,
            first_name="John",
            last_name="Doe",
            Gender="Male",
            general_practice="City Medical Center",
            home_address="123 Main St",
            phone_number="+1234567890"
        )
        self.assertEqual(patient_max.Age, 200)

    def test_invalid_first_name_with_numbers(self):
        with self.assertRaises(ValueError) as e:
            resposne = patient_item(
                patientID=123456,
                Age=20,
                first_name="John2",
                last_name="Doe",
                Gender="Male",
                general_practice="City Medical Center",
                home_address="123 Main St",
                phone_number="+1234567890"
            )
            resposne.__post_init__()
        self.assertEqual(e.exception.args[0], 'first name John2 is invalid contains numeric characters')

    def test_invalid_last_name_with_numbers(self):
        with self.assertRaises(ValueError) as e:
            resposne = patient_item(
                patientID=123456,
                Age=20,
                first_name="Gamer",
                last_name="Doe7",
                Gender="Male",
                general_practice="City Medical Center",
                home_address="123 Main St",
                phone_number="+1234567890"
            )
            resposne.__post_init__()
        self.assertEqual(e.exception.args[0], 'last name Doe7 is invalid contains numeric characters')

    def test_invalid_gender_too_long(self):
        with self.assertRaises(ValueError) as e:
            resposne = patient_item(
                patientID=123456,
                Age=20,
                first_name="pika",
                last_name="Doe",
                Gender="VeryLongGenderString",
                general_practice="City Medical Center",
                home_address="123 Main St",
                phone_number="+1234567890"
            )
            resposne.__post_init__()
        self.assertEqual(e.exception.args[0], 'Gender VeryLongGenderString is invalid too long')

    def test_invalid_phone_number_without_area_code(self):
        with self.assertRaises(ValueError) as e:
            resposne = patient_item(
                patientID=123456,
                Age=20,
                first_name="pika",
                last_name="Doe",
                Gender="Non Binary",
                general_practice="City Medical Center",
                home_address="123 Main St",
                phone_number="1234567890"
            )
            resposne.__post_init__()
        self.assertEqual(e.exception.args[0], 'Phone number 1234567890 is invalid missing area code')

    def test_invalid_phone_number_with_non_numeric_chars(self):
        with self.assertRaises(ValueError) as e:
            resposne = patient_item(
                patientID=123456,
                Age=20,
                first_name="pika",
                last_name="Doe",
                Gender="Non Binary",
                general_practice="City Medical Center",
                home_address="123 Main St",
                phone_number="+123456abc"
            )
            resposne.__post_init__()
        self.assertEqual(e.exception.args[0], 'Phone number +123456abc contains non numeric chars')

    def test_gp_notes_default(self):
        patient = patient_item(
            patientID=123456,
            Age=30,
            first_name="John",
            last_name="Doe",
            Gender="Male",
            general_practice="City Medical Center",
            home_address="123 Main St",
            phone_number="+1234567890"
        )
        patient.__post_init__()
        self.assertEqual(patient.GP_notes, {})

    def test_gp_notes_with_data(self):
        notes = {"22/05/2001": "Regular checkup", "28/05/2001": "Follow-up"}
        patient = patient_item(
            patientID=123456,
            Age=30,
            first_name="John",
            last_name="Doe",
            Gender="Male",
            general_practice="City Medical Center",
            home_address="123 Main St",
            phone_number="+1234567890",
            GP_notes=notes
        )
        patient.__post_init__()
        self.assertEqual(patient.GP_notes, notes)

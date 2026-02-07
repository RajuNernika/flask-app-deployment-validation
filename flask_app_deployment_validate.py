from result_output import *
import sys
import json
import importlib.util
import requests
from googleapiclient import discovery
from google.oauth2 import service_account
from googleapiclient.errors import HttpError

class Activity():

    # Testcase: Check Cloud Run Service Name
    def testcase_check_cloud_run_service_name(self, test_object, credentials, project_id):
        testcase_description = "Verify flask-app Cloud Run service exists"
        expected_result = "flask-app"
        marks = 10

        try:
            is_present = False
            actual = 'Cloud Run Service name is not ' + expected_result

            # Use Cloud Run API
            run_service = discovery.build('run', 'v1', credentials=credentials)
            region = "us-central1"
            parent = f"projects/{project_id}/locations/{region}"

            try:
                request = run_service.projects().locations().services().list(parent=parent)
                response = request.execute()

                for svc in response.get("items", []):
                    if svc["metadata"]["name"] == expected_result:
                        is_present = True
                        actual = expected_result
                        break
            except HttpError as e:
                is_present = False
                actual = f"HTTP Error: {e.resp.status} - {e._get_reason()}"
            except Exception as e:
                is_present = False
                actual = str(e)

            test_object.update_pre_result(testcase_description, expected_result)
            if is_present:
                test_object.update_result(1, expected_result, actual,
                    "Congrats! You have done it right!", " ", marks)
            else:
                test_object.update_result(0, expected_result, actual,
                    "Check Cloud Run Service name",
                    "https://cloud.google.com/run/docs/quickstarts/deploy-container", marks)
        except Exception as e:
            test_object.update_result(-1, expected_result, "Internal Server error",
                "Please check with Admin", "", marks)
            test_object.eval_message["testcase_check_cloud_run_service_name"] = str(e)

def start_tests(credentials, project_id, args):
    if "result_output" not in sys.modules:
        importlib.import_module("result_output")
    else:
        importlib.reload(sys.modules["result_output"])

    test_object = ResultOutput(args, Activity)
    challenge_test = Activity()

    # Execute all testcases
    challenge_test.testcase_check_cloud_run_service_name(test_object, credentials, project_id)

    json.dumps(test_object.result_final(), indent=4)
    return test_object.result_final()
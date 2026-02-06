from result_output import *
import sys
import json
import importlib.util
from googleapiclient import discovery
from google.oauth2 import service_account
from google.cloud import compute_v1
from googleapiclient.errors import HttpError

class Activity():

    # Testcase 1: Check Cloud Run Service Name
    def testcase_check_cloud_run_service_name(self, test_object, credentials, project_id):
        testcase_description = "Verify flask-app Cloud Run service exists"
        expected_result = "flask-app"
        marks = 10

        try:
            is_present = False
            actual = 'Cloud Run Service name is not ' + expected_result

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
            except Exception as e:
                is_present = False

            test_object.update_pre_result(testcase_description, expected_result)
            if is_present:
                test_object.update_result(1, expected_result, actual,
                    "Congrats! You have done it right!", " ", marks)
            else:
                return test_object.update_result(0, expected_result, actual,
                    "Check Cloud Run Service name",
                    "https://cloud.google.com/run/docs/quickstarts/deploy-container", marks)
        except Exception as e:
            test_object.update_result(-1, expected_result, "Internal Server error",
                "Please check with Admin", "", marks)
            test_object.eval_message["testcase_check_cloud_run_service_name"] = str(e)

    # Testcase 2: Check Cloud Run Region
    def testcase_check_cloud_run_region(self, test_object, credentials, project_id):
        testcase_description = "Verify Cloud Run is in us-central1"
        expected_result = "us-central1"
        marks = 5

        try:
            is_present = False
            actual = 'Cloud Run is not in ' + expected_result

            run_service = discovery.build('run', 'v1', credentials=credentials)
            region = "us-central1"
            parent = f"projects/{project_id}/locations/{region}"

            try:
                request = run_service.projects().locations().services().list(parent=parent)
                response = request.execute()

                if response.get("items", []):
                    is_present = True
                    actual = expected_result
            except Exception as e:
                is_present = False

            test_object.update_pre_result(testcase_description, expected_result)
            if is_present:
                test_object.update_result(1, expected_result, actual,
                    "Congrats! You have done it right!", " ", marks)
            else:
                return test_object.update_result(0, expected_result, actual,
                    "Check Cloud Run Region",
                    "https://cloud.google.com/run/docs/locations", marks)
        except Exception as e:
            test_object.update_result(-1, expected_result, "Internal Server error",
                "Please check with Admin", "", marks)
            test_object.eval_message["testcase_check_cloud_run_region"] = str(e)

    # Testcase 3: Check Artifact Registry
    def testcase_check_artifact_registry(self, test_object, credentials, project_id):
        testcase_description = "Verify my-repo repository exists"
        expected_result = "my-repo"
        marks = 5

        try:
            is_present = False
            actual = 'Artifact Registry repository is not ' + expected_result

            artifact_service = discovery.build('artifactregistry', 'v1', credentials=credentials)
            location = "us-central1"
            parent = f"projects/{project_id}/locations/{location}"

            try:
                request = artifact_service.projects().locations().repositories().list(parent=parent)
                response = request.execute()

                for repo in response.get("repositories", []):
                    repo_name = repo["name"].split('/')[-1]
                    if repo_name == expected_result:
                        is_present = True
                        actual = expected_result
                        break
            except Exception as e:
                is_present = False

            test_object.update_pre_result(testcase_description, expected_result)
            if is_present:
                test_object.update_result(1, expected_result, actual,
                    "Congrats! You have done it right!", " ", marks)
            else:
                return test_object.update_result(0, expected_result, actual,
                    "Check Artifact Registry repository",
                    "https://cloud.google.com/artifact-registry/docs/repositories", marks)
        except Exception as e:
            test_object.update_result(-1, expected_result, "Internal Server error",
                "Please check with Admin", "", marks)
            test_object.eval_message["testcase_check_artifact_registry"] = str(e)

    # Testcase 4: Check VPC Network
    def testcase_check_vpc_network(self, test_object, credentials, project_id):
        testcase_description = "Verify simple-vpc exists"
        expected_result = 'simple-vpc'
        marks = 10

        try:
            is_present = False
            actual = 'VPC name is not ' + expected_result
            compute_client = compute_v1.NetworksClient(credentials=credentials)

            try:
                vpcs = compute_client.list(project=project_id)
                for vpc in vpcs:
                    if vpc.name == expected_result:
                        is_present = True
                        actual = expected_result
                        break
            except Exception as e:
                is_present = False

            test_object.update_pre_result(testcase_description, expected_result)
            if is_present:
                test_object.update_result(1, expected_result, actual,
                    "Congrats! You have done it right!", " ", marks)
            else:
                test_object.update_result(0, expected_result, actual,
                    "Check VPC name",
                    "https://cloud.google.com/vpc/docs/create-modify-vpc-networks", marks)
        except Exception as e:
            test_object.update_result(-1, expected_result, "Internal Server error",
                "Please check with Admin", "", marks)
            test_object.eval_message["testcase_check_vpc_network"] = str(e)

    # Testcase 5: Check VM Instance
    def testcase_check_vm_instance(self, test_object, credentials, project_id):
        testcase_description = "Verify simple-vm exists"
        expected_result = "simple-vm"
        marks = 10

        try:
            is_present = False
            actual = 'VM name is not ' + expected_result
            service = discovery.build('compute', 'v1', credentials=credentials)

            try:
                request = service.instances().list(project=project_id, zone="us-central1-a")
                response = request.execute()

                if 'items' in response:
                    for instance in response['items']:
                        if instance['name'] == expected_result:
                            is_present = True
                            actual = expected_result
                            break
            except Exception as e:
                is_present = False

            test_object.update_pre_result(testcase_description, expected_result)
            if is_present:
                test_object.update_result(1, expected_result, actual,
                    "Congrats! You have done it right!", " ", marks)
            else:
                return test_object.update_result(0, expected_result, actual,
                    "Check VM name",
                    "https://cloud.google.com/compute/docs/instances/create-start-instance", marks)
        except Exception as e:
            test_object.update_result(-1, expected_result, "Internal Server error",
                "Please check with Admin", "", marks)
            test_object.eval_message["testcase_check_vm_instance"] = str(e)

def start_tests(credentials, project_id, args):
    if "result_output" not in sys.modules:
        importlib.import_module("result_output")
    else:
        importlib.reload(sys.modules["result_output"])

    test_object = ResultOutput(args, Activity)
    challenge_test = Activity()

    # Execute all testcases
    challenge_test.testcase_check_cloud_run_service_name(test_object, credentials, project_id)
    challenge_test.testcase_check_cloud_run_region(test_object, credentials, project_id)
    challenge_test.testcase_check_artifact_registry(test_object, credentials, project_id)
    challenge_test.testcase_check_vpc_network(test_object, credentials, project_id)
    challenge_test.testcase_check_vm_instance(test_object, credentials, project_id)

    json.dumps(test_object.result_final(), indent=4)
    return test_object.result_final()
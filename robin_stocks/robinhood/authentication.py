"""
STATELESS ROBINHOOD API - EXACT COPY OF WORKING ORIGINAL LOGIC
"""

from typing import Dict, List, Any, Optional, Union, Callable
import secrets
import time
from .helper import request_get, _make_request
from .urls import login_url


def _generate_device_token() -> str:
    """Generate a one-time device token - EXACT COPY FROM ORIGINAL"""
    rands = [secrets.randbelow(256) for _ in range(16)]
    hexa = [str(hex(i + 256)).lstrip("0x")[1:] for i in range(256)]
    token = ""
    for i, r in enumerate(rands):
        token += hexa[r]
        if i in [3, 5, 7, 9]:
            token += "-"
    return token


def _get_sheriff_id(data):
    """Extracts the sheriff verification ID from the response - EXACT COPY"""
    if "id" in data:
        return data["id"]
    raise Exception("Error: No verification ID returned in user-machine response")


def _validate_sheriff_id(device_token: str, workflow_id: str):
    """EXACT COPY OF WORKING ORIGINAL VALIDATION"""
    print("Starting verification process...")
    pathfinder_url = "https://api.robinhood.com/pathfinder/user_machine/"
    machine_payload = {'device_id': device_token, 'flow': 'suv', 'input': {'workflow_id': workflow_id}}
    machine_data = _make_request('POST', pathfinder_url, json=machine_payload)

    machine_id = _get_sheriff_id(machine_data)
    inquiries_url = f"https://api.robinhood.com/pathfinder/inquiries/{machine_id}/user_view/"

    start_time = time.time()
    
    while time.time() - start_time < 120:  # 2-minute timeout
        time.sleep(5)
        inquiries_response = _make_request('GET', inquiries_url)

        if not inquiries_response:  # Handle case where response is None
            print("Error: No response from Robinhood API. Retrying...")
            continue

        if "context" in inquiries_response and "sheriff_challenge" in inquiries_response["context"]:
            challenge = inquiries_response["context"]["sheriff_challenge"]
            challenge_type = challenge["type"]
            challenge_status = challenge["status"]
            challenge_id = challenge["id"]
            if challenge_type == "prompt":
                print("Check robinhood app for device approvals method...")
                prompt_url = f"https://api.robinhood.com/push/{challenge_id}/get_prompts_status/"
                while True:
                    time.sleep(5)
                    prompt_challenge_status = _make_request('GET', prompt_url)
                    if prompt_challenge_status["challenge_status"] == "validated":
                        break
                break

            if challenge_status == "validated":
                print("Verification successful!")
                break  # Stop polling once verification is complete

            if challenge_type in ["sms", "email"] and challenge_status == "issued":
                user_code = input(f"Enter the {challenge_type} verification code sent to your device: ")
                challenge_url = f"https://api.robinhood.com/challenge/{challenge_id}/respond/"
                challenge_payload = {"response": user_code}
                challenge_response = _make_request('POST', challenge_url, data=challenge_payload)

                if challenge_response.get("status") == "validated":
                    break

    # **Now poll the workflow status to confirm final approval**
    inquiries_url = f"https://api.robinhood.com/pathfinder/inquiries/{machine_id}/user_view/"
    
    retry_attempts = 5  # Allow up to 5 retries in case of 500 errors
    while time.time() - start_time < 120:  # 2-minute timeout 
        try:
            inquiries_payload = {"sequence": 0, "user_input": {"status": "continue"}}
            inquiries_response = _make_request('POST', inquiries_url, json=inquiries_payload)
            if "type_context" in inquiries_response and inquiries_response["type_context"]["result"] == "workflow_status_approved":
                print("Verification successful!")
                return
            else:
                time.sleep(5)  # **Increase delay between requests to prevent rate limits**
        except Exception as e:
            time.sleep(5)
            print(f"API request failed: {e}")
            retry_attempts -= 1
            if retry_attempts == 0:
                raise TimeoutError("Max retries reached. Assuming login approved and proceeding.")
            print("Retrying workflow status check...")
            continue

        if not inquiries_response:  # Handle None response
            time.sleep(5)
            print("Error: No response from Robinhood API. Retrying...")
            retry_attempts -= 1
            if retry_attempts == 0:
                raise TimeoutError("Max retries reached. Assuming login approved and proceeding.")
            continue

        workflow_status = inquiries_response.get("verification_workflow", {}).get("workflow_status")

        if workflow_status == "workflow_status_approved":
            print("Workflow status approved! Proceeding with login...")
            return
        elif workflow_status == "workflow_status_internal_pending":
            print("Still waiting for Robinhood to finalize login approval...")
        else:
            retry_attempts -= 1
            if retry_attempts == 0:
                raise TimeoutError("Max retries reached. Assuming login approved and proceeding.")

    raise TimeoutError("Timeout reached. Assuming login is approved and proceeding.")


def login_and_get_token(username: str, password: str, mfa_code: Optional[str] = None, 
                        challenge_code: Optional[str] = None,
                        challenge_callback: Optional[Callable[[str, str], str]] = None) -> Optional[str]:
    """EXACT COPY OF WORKING ORIGINAL LOGIN LOGIC"""
    print("Starting login process...")
    device_token = _generate_device_token()
    
    # EXACT PAYLOAD FROM WORKING ORIGINAL
    login_payload = {
        'client_id': 'c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS',
        'expires_in': 86400,
        'grant_type': 'password',
        'password': password,
        'scope': 'internal',
        'username': username,
        'device_token': device_token,
        'try_passkeys': False,
        'token_request_path': '/login',
        'create_read_only_secondary_token': True,
    }

    if mfa_code:
        login_payload['mfa_code'] = mfa_code

    url = login_url()
    
    # EXACT LOGIC FROM WORKING ORIGINAL - Handle 403 as valid response like original
    try:
        data = _make_request('POST', url, data=login_payload)
    except Exception as e:
        # Check if this is a 403 with verification workflow (like original handles)
        if hasattr(e, '__cause__') and hasattr(e.__cause__, 'response'):
            error_response = e.__cause__.response
            if error_response.status_code == 403:
                try:
                    data = error_response.json()
                    if 'verification_workflow' not in data:
                        print(f"403 error without verification workflow: {data}")
                        return None
                except:
                    print("403 error - could not parse response")
                    return None
            else:
                print(f"Login request failed: {e}")
                return None
        else:
            print(f"Login request failed: {e}")
            return None

    if data:
        try:
            if 'verification_workflow' in data:
                print("Verification required, handling challenge...")
                workflow_id = data['verification_workflow']['id']
                _validate_sheriff_id(device_token, workflow_id)

                # Reattempt login after verification - EXACT FROM ORIGINAL
                try:
                    data = _make_request('POST', url, data=login_payload)
                except Exception as e:
                    # Handle 403 as valid response during reattempt too
                    if hasattr(e, '__cause__') and hasattr(e.__cause__, 'response'):
                        error_response = e.__cause__.response
                        if error_response.status_code == 403:
                            try:
                                data = error_response.json()
                            except:
                                print("Reattempt: 403 error - could not parse response")
                                data = None
                        else:
                            print(f"Reattempt failed: {e}")
                            data = None
                    else:
                        print(f"Reattempt failed: {e}")
                        data = None

            if 'access_token' in data:
                print("LOGIN SUCCESS!")
                return data['access_token']  # Return just the token for stateless operation

        except Exception as e:
            print(f"Error during login verification: {e}")

    return None
"""
Utils to help call requests api
"""
import requests
from main.utils.env_loader import default_env


def call_api(module_name, actor_name, function_name, payload):
    """
    Sends a POST request to a specified module's API endpoint.

    This function constructs an API endpoint URL based on the provided module name,
    actor name, and function name. It retrieves the necessary environment variables
    for the module and constructs the complete URL. A POST request is then sent to
    the constructed URL with the given payload.

    Parameters:
    - module_name (str): The name of the module for which the API call is intended.
                         It's used to fetch the module-specific environment settings.
    - actor_name (str): The name of the actor within the module. This usually refers
                        to a specific set of functionalities or a sub-component of the module.
    - function_name (str): The specific function or endpoint within the module to which
                           the request is addressed.
    - payload (dict): The data to be sent with the POST request. It should be in JSON format.

    Returns:
    - response (requests.Response): The response object received from the API call.

    Raises:
    - ValueError: If the environment for the specified module is not found.

    Note:
    - The function requires that environment variables for the specified module are
      properly set up in the global scope, adhering to the naming convention used
      within the function.
    """
    module_env = globals().get(f"{module_name}_env")
    if not module_env:
        raise ValueError(f"Environment for app {module_env} not found")

    url = f"""http://{getattr(module_env, f'{module_name.upper()}_HOST_IP')}:""" \
          f"""{getattr(module_env, f'{module_name.upper()}_PORT')}/""" \
          f"""{default_env.API_ROOT}/""" \
          f"""{getattr(module_env, f'{module_name.upper()}_VERSION')}/""" \
          f"""{getattr(module_env, f'{module_name.upper()}_NAME')}/""" \
          f"""{actor_name}/{function_name}"""
    headers = {'Accept': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    return response

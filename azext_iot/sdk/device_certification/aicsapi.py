# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.service_client import SDKClient
from msrest import Configuration, Serializer, Deserializer
from .version import VERSION
from msrest.pipeline import ClientRawResponse
from msrest.exceptions import HttpOperationError
from . import models


class AICSAPIConfiguration(Configuration):
    """Configuration for AICSAPI
    Note that all parameters used to create this instance are saved as instance
    attributes.

    :param str base_url: Service URL
    """

    def __init__(
            self, base_url=None):

        if not base_url:
            base_url = 'http://localhost'

        super(AICSAPIConfiguration, self).__init__(base_url)

        self.add_user_agent('aicsapi/{}'.format(VERSION))


class AICSAPI(SDKClient):
    """AICSAPI

    :ivar config: Configuration for client.
    :vartype config: AICSAPIConfiguration

    :param str base_url: Service URL
    """

    def __init__(
            self, base_url=None):

        self.config = AICSAPIConfiguration(base_url)
        super(AICSAPI, self).__init__(None, self.config)

        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self.api_version = 'v1'
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)


    def get_device_certification_requirements(
            self, api_version, badge_type=None, custom_headers=None, raw=False, **operation_config):
        """Get certification requirements.

        :param api_version: Restful API version.
        :type api_version: str
        :param badge_type: Possible values include: 'IotDevice', 'Pnp',
         'IotEdgeCompatible'
        :type badge_type: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: object or ClientRawResponse if raw=true
        :rtype: object or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.get_device_certification_requirements.metadata['url']

        # Construct parameters
        query_parameters = {}
        if badge_type is not None:
            query_parameters['badgeType'] = self._serialize.query("badge_type", badge_type, 'str')
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters, header_parameters)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200, 400]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('[DeviceCertificationRequirement]', response)
        if response.status_code == 400:
            deserialized = self._deserialize('object', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    get_device_certification_requirements.metadata = {'url': '/certificationRequirements'}

    def create_device_test(
            self, api_version, generate_provisioning_configuration=None, body=None, custom_headers=None, raw=False, **operation_config):
        """Create a new Microsoft.Azure.IoT.TestKit.Models.DeviceTest.

        :param api_version: Restful API version.
        :type api_version: str
        :param generate_provisioning_configuration: Whether to generate
         ProvisioningConfiguration info from the server,
         it only applies to
         Microsoft.Azure.IoT.TestKit.Shared.Models.Provisioning.ProvisioningType.SymmetricKey
         and
         Microsoft.Azure.IoT.TestKit.Shared.Models.Provisioning.ProvisioningType.ConnectionString
         provisioning type.
        :type generate_provisioning_configuration: bool
        :param body:
        :type body: ~swagger.models.DeviceTest
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: object or ClientRawResponse if raw=true
        :rtype: object or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.create_device_test.metadata['url']

        # Construct parameters
        query_parameters = {}
        if generate_provisioning_configuration is not None:
            query_parameters['GenerateProvisioningConfiguration'] = self._serialize.query("generate_provisioning_configuration", generate_provisioning_configuration, 'bool')
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        header_parameters['Content-Type'] = 'application/json-patch+json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        if body is not None:
            body_content = self._serialize.body(body, 'DeviceTest')
        else:
            body_content = None

        # Construct and send request
        request = self._client.post(url, query_parameters, header_parameters, body_content)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200, 400]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('DeviceTest', response)
        if response.status_code == 400:
            deserialized = self._deserialize('object', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    create_device_test.metadata = {'url': '/deviceTests'}

    def get_device_test(
            self, device_test_id, api_version, custom_headers=None, raw=False, **operation_config):
        """Get a DeviceTest by Id.

        :param device_test_id: The Id of the
         Microsoft.Azure.IoT.TestKit.Models.DeviceTest to retrieve.
        :type device_test_id: str
        :param api_version: Restful API version.
        :type api_version: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: object or ClientRawResponse if raw=true
        :rtype: object or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.get_device_test.metadata['url']
        path_format_arguments = {
            'deviceTestId': self._serialize.url("device_test_id", device_test_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters, header_parameters)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200, 400]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('DeviceTest', response)
        if response.status_code == 400:
            deserialized = self._deserialize('object', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    get_device_test.metadata = {'url': '/deviceTests/{deviceTestId}'}

    def update_device_test(
            self, device_test_id, api_version, generate_provisioning_configuration=None, body=None, custom_headers=None, raw=False, **operation_config):
        """Update the DeviceTest with certain Id.

        :param device_test_id: The Id of the
         Microsoft.Azure.IoT.TestKit.Models.DeviceTest to retrieve.
        :type device_test_id: str
        :param api_version: Restful API version.
        :type api_version: str
        :param generate_provisioning_configuration: Whether to generate
         ProvisioningConfiguration info from the server,
         it only applies to
         Microsoft.Azure.IoT.TestKit.Shared.Models.Provisioning.ProvisioningType.SymmetricKey
         and
         Microsoft.Azure.IoT.TestKit.Shared.Models.Provisioning.ProvisioningType.ConnectionString
         provisioning type.
        :type generate_provisioning_configuration: bool
        :param body:
        :type body: ~swagger.models.DeviceTest
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: object or ClientRawResponse if raw=true
        :rtype: object or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.update_device_test.metadata['url']
        path_format_arguments = {
            'deviceTestId': self._serialize.url("device_test_id", device_test_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        if generate_provisioning_configuration is not None:
            query_parameters['GenerateProvisioningConfiguration'] = self._serialize.query("generate_provisioning_configuration", generate_provisioning_configuration, 'bool')
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        header_parameters['Content-Type'] = 'application/json-patch+json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        if body is not None:
            body_content = self._serialize.body(body, 'DeviceTest')
        else:
            body_content = None

        # Construct and send request
        request = self._client.put(url, query_parameters, header_parameters, body_content)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [204, 400]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 400:
            deserialized = self._deserialize('object', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    update_device_test.metadata = {'url': '/deviceTests/{deviceTestId}'}

    def search_device_test(
            self, api_version, body=None, custom_headers=None, raw=False, **operation_config):
        """Search DeviceTest.

        :param api_version: Restful API version.
        :type api_version: str
        :param body:
        :type body: ~swagger.models.DeviceTestSearchOptions
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: object or ClientRawResponse if raw=true
        :rtype: object or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.search_device_test.metadata['url']

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        header_parameters['Content-Type'] = 'application/json-patch+json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        if body is not None:
            body_content = self._serialize.body(body, 'DeviceTestSearchOptions')
        else:
            body_content = None

        # Construct and send request
        request = self._client.post(url, query_parameters, header_parameters, body_content)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200, 400]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('[DeviceTestSearchResult]', response)
        if response.status_code == 400:
            deserialized = self._deserialize('object', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    search_device_test.metadata = {'url': '/deviceTests/search'}

    def create_device_test_task(
            self, device_test_id, api_version, body=None, custom_headers=None, raw=False, **operation_config):
        """Queue a new async
        Microsoft.Azure.IoT.TestKit.Shared.Models.DeviceTestTaskType for a
        DeviceTest.
        The user can only have one running task for a DeviceTest.

        :param device_test_id: The Id of the
         Microsoft.Azure.IoT.TestKit.Models.DeviceTest to retrieve.
        :type device_test_id: str
        :param api_version: Restful API version.
        :type api_version: str
        :param body:
        :type body: ~swagger.models.NewTaskPayload
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: object or ClientRawResponse if raw=true
        :rtype: object or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.create_device_test_task.metadata['url']
        path_format_arguments = {
            'deviceTestId': self._serialize.url("device_test_id", device_test_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        header_parameters['Content-Type'] = 'application/json-patch+json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        if body is not None:
            body_content = self._serialize.body(body, 'NewTaskPayload')
        else:
            body_content = None

        # Construct and send request
        request = self._client.post(url, query_parameters, header_parameters, body_content)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [202, 400, 404, 409]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 202:
            deserialized = self._deserialize('DeviceTestTask', response)
        if response.status_code == 400:
            deserialized = self._deserialize('object', response)
        if response.status_code == 404:
            deserialized = self._deserialize('object', response)
        if response.status_code == 409:
            deserialized = self._deserialize('object', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    create_device_test_task.metadata = {'url': '/deviceTests/{deviceTestId}/tasks'}

    def cancel_device_test_task(
            self, task_id, device_test_id, api_version, custom_headers=None, raw=False, **operation_config):
        """Cancel the running tasks of a DeviceTest.

        :param task_id: The Id of the
         Microsoft.Azure.IoT.TestKit.Models.DeviceTestTask to retrieve.
        :type task_id: str
        :param device_test_id: The Id of the
         Microsoft.Azure.IoT.TestKit.Models.DeviceTest to retrieve.
        :type device_test_id: str
        :param api_version: Restful API version.
        :type api_version: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: object or ClientRawResponse if raw=true
        :rtype: object or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.cancel_device_test_task.metadata['url']
        path_format_arguments = {
            'taskId': self._serialize.url("task_id", task_id, 'str'),
            'deviceTestId': self._serialize.url("device_test_id", device_test_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.delete(url, query_parameters, header_parameters)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [202, 400, 404]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 400:
            deserialized = self._deserialize('object', response)
        if response.status_code == 404:
            deserialized = self._deserialize('object', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    cancel_device_test_task.metadata = {'url': '/deviceTests/{deviceTestId}/tasks/{taskId}'}

    def get_device_test_task(
            self, task_id, device_test_id, api_version, custom_headers=None, raw=False, **operation_config):
        """Get the task status of a DeviceTest.

        :param task_id: The Id of the
         Microsoft.Azure.IoT.TestKit.Models.DeviceTestTask to retrieve.
        :type task_id: str
        :param device_test_id: The Id of the
         Microsoft.Azure.IoT.TestKit.Models.DeviceTest to retrieve.
        :type device_test_id: str
        :param api_version: Restful API version.
        :type api_version: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: object or ClientRawResponse if raw=true
        :rtype: object or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.get_device_test_task.metadata['url']
        path_format_arguments = {
            'taskId': self._serialize.url("task_id", task_id, 'str'),
            'deviceTestId': self._serialize.url("device_test_id", device_test_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters, header_parameters)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200, 400, 404]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('DeviceTestTask', response)
        if response.status_code == 400:
            deserialized = self._deserialize('object', response)
        if response.status_code == 404:
            deserialized = self._deserialize('object', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    get_device_test_task.metadata = {'url': '/deviceTests/{deviceTestId}/tasks/{taskId}'}

    def get_running_device_test_tasks(
            self, device_test_id, api_version, custom_headers=None, raw=False, **operation_config):
        """Get the running tasks of a DeviceTest. Current implementation only
        allows one running task.

        :param device_test_id: The Id of the
         Microsoft.Azure.IoT.TestKit.Models.DeviceTest to retrieve.
        :type device_test_id: str
        :param api_version: Restful API version.
        :type api_version: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: object or ClientRawResponse if raw=true
        :rtype: object or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.get_running_device_test_tasks.metadata['url']
        path_format_arguments = {
            'deviceTestId': self._serialize.url("device_test_id", device_test_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters, header_parameters)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200, 400, 404]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('[DeviceTestTask]', response)
        if response.status_code == 400:
            deserialized = self._deserialize('object', response)
        if response.status_code == 404:
            deserialized = self._deserialize('object', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    get_running_device_test_tasks.metadata = {'url': '/deviceTests/{deviceTestId}/tasks/running'}

    def get_test_cases(
            self, device_test_id, api_version, custom_headers=None, raw=False, **operation_config):
        """Get the testcases of a DeviceTest. They are generated through
        Microsoft.Azure.IoT.TestKit.Shared.Models.DeviceTestTaskType.GenerateTestCases
        task.

        :param device_test_id: The Id of the
         Microsoft.Azure.IoT.TestKit.Models.DeviceTest to retrieve.
        :type device_test_id: str
        :param api_version: Restful API version.
        :type api_version: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: object or ClientRawResponse if raw=true
        :rtype: object or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.get_test_cases.metadata['url']
        path_format_arguments = {
            'deviceTestId': self._serialize.url("device_test_id", device_test_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters, header_parameters)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200, 400, 404]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('TestCases', response)
        if response.status_code == 400:
            deserialized = self._deserialize('object', response)
        if response.status_code == 404:
            deserialized = self._deserialize('object', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    get_test_cases.metadata = {'url': '/deviceTests/{deviceTestId}/TestCases'}

    def update_test_cases(
            self, device_test_id, api_version, body=None, custom_headers=None, raw=False, **operation_config):
        """Update the testcases settings of a DeviceTest. The test cases cannot be
        added or removed through this API.

        :param device_test_id: The Id of the
         Microsoft.Azure.IoT.TestKit.Models.DeviceTest to retrieve.
        :type device_test_id: str
        :param api_version: Restful API version.
        :type api_version: str
        :param body:
        :type body: ~swagger.models.TestCases
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: object or ClientRawResponse if raw=true
        :rtype: object or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.update_test_cases.metadata['url']
        path_format_arguments = {
            'deviceTestId': self._serialize.url("device_test_id", device_test_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        header_parameters['Content-Type'] = 'application/json-patch+json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        if body is not None:
            body_content = self._serialize.body(body, 'TestCases')
        else:
            body_content = None

        # Construct and send request
        request = self._client.patch(url, query_parameters, header_parameters, body_content)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [204, 400, 404]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 400:
            deserialized = self._deserialize('object', response)
        if response.status_code == 404:
            deserialized = self._deserialize('object', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    update_test_cases.metadata = {'url': '/deviceTests/{deviceTestId}/TestCases'}

    def get_latest_test_run(
            self, device_test_id, api_version, custom_headers=None, raw=False, **operation_config):
        """Get the latest test run of the DeviceTest with the deviceTestId.

        :param device_test_id: The Id of the
         Microsoft.Azure.IoT.TestKit.Models.DeviceTest to retrieve.
        :type device_test_id: str
        :param api_version: Restful API version.
        :type api_version: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: object or ClientRawResponse if raw=true
        :rtype: object or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.get_latest_test_run.metadata['url']
        path_format_arguments = {
            'deviceTestId': self._serialize.url("device_test_id", device_test_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters, header_parameters)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200, 400, 404]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('TestRun', response)
        if response.status_code == 400:
            deserialized = self._deserialize('object', response)
        if response.status_code == 404:
            deserialized = self._deserialize('object', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    get_latest_test_run.metadata = {'url': '/deviceTests/{deviceTestId}/testRuns/latest'}

    def get_test_run(
            self, test_run_id, device_test_id, api_version, custom_headers=None, raw=False, **operation_config):
        """Get the test run with testrunId of the DeviceTest with the
        deviceTestId.

        :param test_run_id: The Id of a
         Microsoft.Azure.IoT.TestKit.Models.TestRun.
        :type test_run_id: str
        :param device_test_id: The Id of the
         Microsoft.Azure.IoT.TestKit.Models.DeviceTest to retrieve.
        :type device_test_id: str
        :param api_version: Restful API version.
        :type api_version: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: object or ClientRawResponse if raw=true
        :rtype: object or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.get_test_run.metadata['url']
        path_format_arguments = {
            'testRunId': self._serialize.url("test_run_id", test_run_id, 'str'),
            'deviceTestId': self._serialize.url("device_test_id", device_test_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters, header_parameters)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200, 400, 404]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('TestRun', response)
        if response.status_code == 400:
            deserialized = self._deserialize('object', response)
        if response.status_code == 404:
            deserialized = self._deserialize('object', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    get_test_run.metadata = {'url': '/deviceTests/{deviceTestId}/testRuns/{testRunId}'}

    def submit_test_run(
            self, test_run_id, device_test_id, api_version, custom_headers=None, raw=False, **operation_config):
        """Submit TestRun to Partner/Product service.

        :param test_run_id: The Id of a
         Microsoft.Azure.IoT.TestKit.Models.TestRun.
        :type test_run_id: str
        :param device_test_id: The Id of the
         Microsoft.Azure.IoT.TestKit.Models.DeviceTest to retrieve.
        :type device_test_id: str
        :param api_version: Restful API version.
        :type api_version: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: object or ClientRawResponse if raw=true
        :rtype: object or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.submit_test_run.metadata['url']
        path_format_arguments = {
            'testRunId': self._serialize.url("test_run_id", test_run_id, 'str'),
            'deviceTestId': self._serialize.url("device_test_id", device_test_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.post(url, query_parameters, header_parameters)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [204, 400, 404, 500]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 400:
            deserialized = self._deserialize('object', response)
        if response.status_code == 404:
            deserialized = self._deserialize('object', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    submit_test_run.metadata = {'url': '/deviceTests/{deviceTestId}/testRuns/{testRunId}/submit'}

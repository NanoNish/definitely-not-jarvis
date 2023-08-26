from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2

from prompt import prompt

class ClarifaiService:
    def __init__(
        self,
        api_key: str,
        user_id: str,
        app_id: str,
        workflow_id: str,
    ):
        channel = ClarifaiChannel.get_grpc_channel()
        self.stub = service_pb2_grpc.V2Stub(channel)

        self.metadata = (('authorization', f'Key {api_key}'),)
        self.user_data = resources_pb2.UserAppIDSet(user_id=user_id, app_id=app_id)
        self.workflow_id = workflow_id

    def predict(
        self,
        user_input: str,
        faqs: list[tuple[str, str]],
        knowledge: list[str],
    ):
        raw_input = prompt(
            faqs=faqs,
            knowledge=knowledge,
            query=user_input,
        )

        print(raw_input)

        input_to_model = resources_pb2.Input(
            data=resources_pb2.Data(
                text=resources_pb2.Text(
                    raw=raw_input,
                ),
            ),
        )
        request = service_pb2.PostWorkflowResultsRequest(
            user_app_id=self.user_data,  
            workflow_id=self.workflow_id,
            inputs=[input_to_model],
        )

        response = self.stub.PostWorkflowResults(
            request,
            metadata=self.metadata,
        )

        if response.status.code != status_code_pb2.SUCCESS:
            print(response.status)
            raise Exception("Post workflow results failed, status: " 
                            + response.status.description)
        
        result = response.results[0].outputs[0]

        return result.data.text.raw
